export function formatPrice(price: number | null | undefined): string {
  if (price === null || price === undefined || isNaN(price)) return "—";
  return new Intl.NumberFormat("en-IN", {
    style: "currency",
    currency: "INR",
    maximumFractionDigits: 0,
  }).format(price);
}

export function formatPricePerGram(pricePerGram: number | null | undefined): string {
  if (pricePerGram === null || pricePerGram === undefined || isNaN(pricePerGram)) return "—";
  return `₹${pricePerGram.toFixed(2)}/g`;
}

export function formatPercentage(pct: number | null | undefined): string {
  if (pct === null || pct === undefined || isNaN(pct)) return "—";
  return `${pct.toFixed(1)}%`;
}

export function formatWeight(grams: number | null | undefined): string {
  if (!grams) return "—";
  if (grams >= 1000) {
    const kg = grams / 1000;
    return `${Number.isInteger(kg) ? kg : kg.toFixed(1)}kg`;
  }
  return `${grams}g`;
}

export function computePer100g(value: number, netWeightG: number): number {
  if (!netWeightG || netWeightG <= 0) return 0;
  return Number(((value / netWeightG) * 100).toFixed(2));
}

export function cn(...classes: (string | boolean | undefined | null | number | false)[]): string {
  return classes.filter(Boolean).join(" ");
}

/** "just now", "5 min ago", "3 h ago", "2 days ago". */
export function formatTimeAgo(iso: string | null | undefined, now: number = Date.now()): string {
  if (!iso) return "—";
  const minutes = Math.max(0, Math.round((now - new Date(iso).getTime()) / 60000));
  if (minutes < 1) return "just now";
  if (minutes < 60) return `${minutes} min ago`;
  const hours = Math.round(minutes / 60);
  if (hours < 48) return `${hours} h ago`;
  return `${Math.round(hours / 24)} days ago`;
}
