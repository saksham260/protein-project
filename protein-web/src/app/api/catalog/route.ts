import { getProducts, toListProduct } from "@/lib/data";

export const dynamic = "force-static";
export const revalidate = 3600; // 1 hour; /api/revalidate refreshes it sooner after a price update

/** The whole catalog for the browser's in-memory search and filters. */
export async function GET() {
  const products = await getProducts();
  return Response.json(products.map(toListProduct));
}
