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
let postKeyboardTimer: ReturnType<typeof setTimeout> | null = null;

/**
 * Resets mobile viewport zoom back to 1.0 (original scale) across Android and iOS browsers.
 * When the searchbar is active, mobile browsers zoom in for easier typing.
 * Once searching completes or the input blurs (becomes inactive), this function:
 * 1. Blurs any active element to trigger virtual keyboard dismissal.
 * 2. Horizontally re-centers the viewport (window.scrollX to 0).
 * 3. Enforces initial-scale=1.0, maximum-scale=1.0, user-scalable=no immediately and again
 *    after keyboard dismissal (~200ms) to force rendering engines (WebKit and Blink) to snap back to 1.0.
 * 4. Triggers a CSS layout reflow.
 * 5. Restores user-scalable pinch-to-zoom after 450ms.
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
    /iPhone|iPad|iPod|Android/i.test(navigator.userAgent) ||
    (typeof window.visualViewport !== "undefined" && (window.visualViewport?.scale ?? 1) > 1);

  if (!isMobile) return;

  const applyZoomReset = () => {
    // Reset any horizontal scroll offset that auto-zoom introduced
    if (window.scrollX !== 0) {
      window.scrollTo({ left: 0, top: window.scrollY });
    }

    let viewport = document.querySelector<HTMLMetaElement>('meta[name="viewport"]');
    if (!viewport) {
      viewport = document.createElement("meta");
      viewport.name = "viewport";
      document.head.appendChild(viewport);
    }

    // Force viewport to snap back to 1.0
    viewport.setAttribute(
      "content",
      "width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no"
    );

    // CSS zoom reflow trick: triggers a rendering engine layout refresh
    try {
      const prevZoom = document.body.style.zoom;
      document.body.style.zoom = "0.9999";
      requestAnimationFrame(() => {
        document.body.style.zoom = prevZoom || "1";
      });
    } catch {
      // Ignore if browser doesn't support body.zoom
    }
  };

  // Run immediately
  applyZoomReset();

  if (postKeyboardTimer) clearTimeout(postKeyboardTimer);
  if (restoreViewportTimer) clearTimeout(restoreViewportTimer);

  // Re-run once the virtual keyboard is mid-to-fully dismissed (200ms)
  postKeyboardTimer = setTimeout(() => {
    applyZoomReset();
  }, 200);

  // Restore scalable viewport after the browser finishes rescaling so pinch-zoom is preserved
  restoreViewportTimer = setTimeout(() => {
    const viewport = document.querySelector<HTMLMetaElement>('meta[name="viewport"]');
    if (viewport) {
      viewport.setAttribute(
        "content",
        "width=device-width, initial-scale=1.0, maximum-scale=5.0, user-scalable=yes"
      );
    }
    restoreViewportTimer = null;
    postKeyboardTimer = null;
  }, 450);
}

