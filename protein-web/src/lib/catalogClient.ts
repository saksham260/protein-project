import { ProductWithVariants } from "@/types/product";
import { applyFilters, QueryFilters } from "@/lib/catalog";
import { getAvailabilitySummaries, isReportedAvailable } from "@/lib/availability";

// The browser's view of the catalog: downloaded once, then filtered in memory.

const CATALOG_TTL_MS = 10 * 60 * 1000;

let cached: { loadedAt: number; products: Promise<ProductWithVariants[]> } | null = null;

export function fetchCatalog(): Promise<ProductWithVariants[]> {
  if (cached && Date.now() - cached.loadedAt < CATALOG_TTL_MS) return cached.products;

  const products = fetch("/api/catalog").then((response) => {
    if (!response.ok) throw new Error(`Catalog request failed: ${response.status}`);
    return response.json() as Promise<ProductWithVariants[]>;
  });
  cached = { loadedAt: Date.now(), products };
  // A failed download must not stick around for the next ten minutes.
  products.catch(() => {
    cached = null;
  });
  return products;
}

/** Variant ids reported available on any quick-commerce platform in the pincode's area. */
async function getVariantIdsAvailableNear(products: ProductWithVariants[], pincode: string): Promise<Set<string>> {
  const variantIds = products.flatMap((p) => p.variants.map((v) => v.id));
  const summaries = await getAvailabilitySummaries(variantIds, pincode);
  return new Set(summaries.filter(isReportedAvailable).map((s) => s.variant_id));
}

export async function getProducts(filters?: QueryFilters): Promise<ProductWithVariants[]> {
  const catalog = await fetchCatalog();
  const availableNearIds =
    filters?.nearMe && filters.pincode ? await getVariantIdsAvailableNear(catalog, filters.pincode) : undefined;
  return applyFilters(catalog, filters, availableNearIds);
}
