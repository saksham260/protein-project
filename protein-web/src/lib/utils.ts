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

export interface ProductNameParts {
  baseName: string;
  packInfo: string | null;
}

const PACK_REGEX = /\s*[\(\[]?\b((?:Pack|Box)\s+of\s+[^)\]]+)\b[\)\]]?/i;

/**
 * Splits a product name into base product name and pack specification.
 * e.g. "Millionaire Brownie 20g Protein Bar (Pack of 8)" -> { baseName: "Millionaire Brownie 20g Protein Bar", packInfo: "Pack of 8" }
 */
export function splitProductName(name: string, variantName?: string): ProductNameParts {
  if (!name) return { baseName: "", packInfo: null };

  const match = name.match(PACK_REGEX);
  if (match) {
    const packInfo = match[1].trim();
    const baseName = name.replace(match[0], "").replace(/[\s\-,]+$/, "").trim();
    return {
      baseName: baseName || name,
      packInfo,
    };
  }

  if (variantName) {
    const vMatch = variantName.match(PACK_REGEX);
    if (vMatch) {
      return {
        baseName: name.trim(),
        packInfo: vMatch[1].trim(),
      };
    }
  }

  return { baseName: name.trim(), packInfo: null };
}

let restoreViewportTimer: ReturnType<typeof setTimeout> | null = null;

/**
 * Resets mobile viewport zoom back to 1.0 (default unzoomed state).
 * On mobile browsers (especially iOS Safari and mobile Chrome), focusing inputs triggers an auto-zoom
 * that persists even after submission or blur. By temporarily enforcing maximum-scale=1,
 * the browser resets its viewport scale back to 1.0, after which standard scalable viewport
 * is restored so user pinch-to-zoom remains fully supported.
 */
export function resetMobileZoom(): void {
  if (typeof window === "undefined" || typeof document === "undefined") return;

  // 1. Blur any active input element to close virtual keyboard
  if (document.activeElement instanceof HTMLElement) {
    document.activeElement.blur();
  }

  // 2. Only run zoom reset logic on mobile devices/screens
  const isMobile =
    window.innerWidth <= 768 ||
    /iPhone|iPad|iPod|Android/i.test(navigator.userAgent);
  if (!isMobile) return;

  // 3. Reset any horizontal scroll offset that auto-zoom introduced
  if (window.scrollX !== 0) {
    window.scrollTo({ left: 0, top: window.scrollY });
  }

  // 4. Force viewport scale to 1.0 via viewport meta tag
  let viewport = document.querySelector<HTMLMetaElement>('meta[name="viewport"]');
  if (!viewport) {
    viewport = document.createElement("meta");
    viewport.name = "viewport";
    document.head.appendChild(viewport);
  }

  if (restoreViewportTimer) {
    clearTimeout(restoreViewportTimer);
  }

  // Setting maximum-scale=1 forces iOS Safari / mobile WebKit to immediately scale back to 1.0
  viewport.setAttribute("content", "width=device-width, initial-scale=1, maximum-scale=1");

  // Restore scalable viewport after the browser finishes rescaling so pinch-zoom is preserved
  restoreViewportTimer = setTimeout(() => {
    if (viewport) {
      viewport.setAttribute("content", "width=device-width, initial-scale=1");
    }
    restoreViewportTimer = null;
  }, 300);
}

