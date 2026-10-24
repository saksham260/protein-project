/**
 * Where to send the user after sign-in. Only same-site paths are allowed, so a crafted
 * `?next=https://evil.com` or `?next=//evil.com` link can't bounce people to another site.
 */
export function safeNextPath(next: string | null | undefined, fallback = "/"): string {
  if (!next || !next.startsWith("/") || next.startsWith("//") || next.includes("\\")) return fallback;
  return next;
}

/**
 * The public address of the site as the visitor sees it. Behind Render's proxy the request URL
 * can show an internal host, so prefer the forwarded headers.
 */
export function publicOrigin(requestUrl: string, headers: Headers): string {
  const host = headers.get("x-forwarded-host");
  if (!host) return new URL(requestUrl).origin;
  const proto = headers.get("x-forwarded-proto") ?? "https";
  return `${proto}://${host}`;
}
