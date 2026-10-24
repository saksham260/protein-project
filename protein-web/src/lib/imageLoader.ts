/**
 * Image URLs for next/image. We don't let our own server resize images (Render's small servers are far
 * too slow at it, and some brand CDNs refuse server-side downloads). Instead the CDNs that can resize
 * (Shopify, Unsplash) do it for us, and every other image is used as-is straight from the brand's site.
 */
export default function imageLoader({ src, width, quality }: { src: string; width: number; quality?: number }): string {
  try {
    const url = new URL(src);
    if (url.hostname === "cdn.shopify.com") {
      url.searchParams.set("width", String(width));
      return url.toString();
    }
    if (url.hostname === "images.unsplash.com") {
      url.searchParams.set("w", String(width));
      url.searchParams.set("q", String(quality ?? 75));
      url.searchParams.set("auto", "format");
      return url.toString();
    }
  } catch {
    // Not an absolute URL (e.g. a local /public image): use it unchanged.
  }
  return src;
}
