"use client";

import React, { useEffect, useMemo, useState } from "react";
import Link from "next/link";
import { fetchCatalog } from "@/lib/catalogClient";
import { icmrReferenceGrams, ICMR_RDA_G_PER_KG, rankByDailyCost } from "@/lib/proteinCost";
import { formatPrice, splitProductName } from "@/lib/utils";
import type { ProductWithVariants } from "@/types/product";

const FIELD =
  "w-full px-3 py-2 rounded-xl bg-[#1C1916] border border-[#332D27] text-sm font-mono text-[#F5F2EB] focus:outline-none focus:border-[#D97706]";
const LABEL = "flex flex-col gap-1.5 text-xs font-mono text-[#968E85]";

const FORMS = [
  { value: "", label: "Any form" },
  { value: "protein-powders", label: "Protein powders" },
  { value: "protein-bars", label: "Protein bars" },
  { value: "rtd-drinks", label: "Ready-to-drink" },
  { value: "protein-spreads", label: "Peanut butter & spreads" },
];

const toPositiveNumber = (text: string) => {
  const value = Number(text);
  return Number.isFinite(value) && value > 0 ? value : null;
};

export function CostCalculator() {
  const [catalog, setCatalog] = useState<ProductWithVariants[] | null>(null);
  const [loadFailed, setLoadFailed] = useState(false);
  const [weight, setWeight] = useState("");
  const [grams, setGrams] = useState("25");
  const [categorySlug, setCategorySlug] = useState("");
  const [diet, setDiet] = useState<"" | "vegetarian" | "vegan">("");
  const [hideRedFlags, setHideRedFlags] = useState(true);

  useEffect(() => {
    let isMounted = true;
    fetchCatalog()
      .then((products) => {
        if (isMounted) setCatalog(products);
      })
      .catch(() => {
        if (isMounted) setLoadFailed(true);
      });
    return () => {
      isMounted = false;
    };
  }, []);

  const weightKg = toPositiveNumber(weight);
  const gramsPerDay = toPositiveNumber(grams);

  const results = useMemo(() => {
    if (!catalog || !gramsPerDay) return [];
    return rankByDailyCost(catalog, {
      gramsPerDay,
      categorySlug: categorySlug || undefined,
      diet: diet || undefined,
      hideRedFlags,
    });
  }, [catalog, gramsPerDay, categorySlug, diet, hideRedFlags]);

  return (
    <div className="flex flex-col gap-6">
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 p-5 rounded-2xl bg-[#141210] border border-[#332D27]">
        <label className={LABEL}>
          Protein from this product, per day (g)
          <input type="number" inputMode="numeric" min={1} max={300} value={grams} onChange={(e) => setGrams(e.target.value)} className={FIELD} />
        </label>
        <label className={LABEL}>
          Your weight in kg (optional)
          <input type="number" inputMode="numeric" min={1} max={300} value={weight} onChange={(e) => setWeight(e.target.value)} placeholder="e.g. 70" className={FIELD} />
        </label>
        <label className={LABEL}>
          Form
          <select value={categorySlug} onChange={(e) => setCategorySlug(e.target.value)} className={FIELD}>
            {FORMS.map((form) => (
              <option key={form.value} value={form.value}>
                {form.label}
              </option>
            ))}
          </select>
        </label>
        <label className={LABEL}>
          Diet
          <select value={diet} onChange={(e) => setDiet(e.target.value as typeof diet)} className={FIELD}>
            <option value="">Any</option>
            <option value="vegetarian">Vegetarian</option>
            <option value="vegan">Vegan</option>
          </select>
        </label>
        <label className="sm:col-span-2 flex items-center gap-2.5 text-xs font-mono text-[#F5F2EB] cursor-pointer">
          <input
            type="checkbox"
            checked={hideRedFlags}
            onChange={(e) => setHideRedFlags(e.target.checked)}
            className="accent-[#D97706]"
          />
          Hide products with label red flags
        </label>
      </div>

      {weightKg && (
        <p className="text-xs text-[#C9C3BA] leading-relaxed p-4 rounded-2xl bg-[#1C1916] border border-[#332D27]">
          For reference, ICMR-NIN&apos;s safe protein requirement for healthy Indian adults is {ICMR_RDA_G_PER_KG}g per kg of body
          weight a day, which is about <strong className="text-[#F5F2EB]">{icmrReferenceGrams(weightKg)}g a day</strong> at your
          weight, from all food combined.
        </p>
      )}

      {loadFailed && (
        <p role="alert" className="text-xs font-mono text-[#F87171]">
          Couldn&apos;t load the products. Please refresh the page.
        </p>
      )}

      {!catalog && !loadFailed && <div className="h-64 rounded-2xl bg-[#1C1916] border border-[#332D27] skeleton-shimmer" aria-hidden />}

      {catalog && !gramsPerDay && <p className="text-xs font-mono text-[#968E85]">Enter how much protein you want per day.</p>}

      {catalog && gramsPerDay && results.length === 0 && (
        <p className="text-xs font-mono text-[#968E85]">No products match these choices.</p>
      )}

      {results.length > 0 && (
        <div className="overflow-x-auto rounded-2xl border border-[#332D27] bg-[#1C1916]">
          <table className="w-full min-w-[560px] border-collapse text-xs">
            <caption className="sr-only">Cheapest products for {gramsPerDay}g of protein a day</caption>
            <thead>
              <tr className="border-b border-[#332D27] text-left font-mono text-[#968E85]">
                <th scope="col" className="p-3 font-medium">Product</th>
                <th scope="col" className="p-3 font-medium">Per day</th>
                <th scope="col" className="p-3 font-medium">Per 30 days</th>
                <th scope="col" className="p-3 font-medium">Packs in 30 days</th>
              </tr>
            </thead>
            <tbody>
              {results.map(({ product, variant, perDay, perMonth, packsPerMonth }) => {
                const { baseName, packInfo } = splitProductName(product.name, variant.variant_name);
                return (
                  <tr key={variant.id} className="border-b border-[#332D27]/60 last:border-b-0 font-mono text-[#F5F2EB]">
                    <td className="p-3">
                      <Link href={`/product/${product.slug}`} className="flex flex-col gap-0.5 hover:text-[#F59E0B]">
                        <span className="text-[11px] uppercase tracking-wider text-[#F59E0B] font-bold">{product.brand?.name}</span>
                        <span className="font-sans font-bold">{baseName}</span>
                        <span className="text-[11px] text-[#968E85]">{packInfo ?? variant.variant_name}</span>
                      </Link>
                    </td>
                    <td className="p-3 font-bold text-[#34D399]">{formatPrice(perDay)}</td>
                    <td className="p-3">{formatPrice(perMonth)}</td>
                    <td className="p-3">{packsPerMonth.toFixed(1)}</td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
