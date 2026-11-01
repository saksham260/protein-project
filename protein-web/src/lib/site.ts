export const SITE_NAME = "The Protein Discovery Engine";

/** The site's public address. Set NEXT_PUBLIC_SITE_URL in production; Render also provides RENDER_EXTERNAL_URL. */
export function siteUrl(): string {
  const url = process.env.NEXT_PUBLIC_SITE_URL || process.env.RENDER_EXTERNAL_URL || "http://localhost:3000";
  return url.replace(/\/+$/, "");
}

/** Shown only when set, so the pages never print a made-up address. */
export const CONTACT_EMAIL = process.env.NEXT_PUBLIC_CONTACT_EMAIL || null;
