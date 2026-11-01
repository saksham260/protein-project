import type { NextConfig } from "next";

const securityHeaders = [
  { key: "Strict-Transport-Security", value: "max-age=31536000" },
  { key: "X-Content-Type-Options", value: "nosniff" },
  { key: "X-Frame-Options", value: "DENY" },
  { key: "Referrer-Policy", value: "strict-origin-when-cross-origin" },
  { key: "Permissions-Policy", value: "camera=(), microphone=(), geolocation=()" },
  // Only the rules that can't break scripts or the many brand image hosts.
  { key: "Content-Security-Policy", value: "frame-ancestors 'none'; base-uri 'self'; object-src 'none'; form-action 'self'" },
];

const nextConfig: NextConfig = {
  async headers() {
    return [{ source: "/(.*)", headers: securityHeaders }];
  },
  images: {
    // Resize at the image's own CDN instead of on our server (see src/lib/imageLoader.ts)
    loader: "custom",
    loaderFile: "./src/lib/imageLoader.ts",
    remotePatterns: [
      {
        protocol: "https",
        hostname: "**.supabase.co",
      },
      {
        protocol: "https",
        hostname: "**.amazon.com",
      },
      {
        protocol: "https",
        hostname: "**.amazon.in",
      },
      {
        protocol: "https",
        hostname: "images.unsplash.com",
      },
      {
        protocol: "https",
        hostname: "cdn.shopify.com",
      },
      {
        protocol: "https",
        hostname: "shop.amul.com",
      },
      {
        protocol: "https",
        hostname: "epigamiastore.com",
      },
      {
        protocol: "https",
        hostname: "media.thewholetruthfoods.com",
      },
      {
        protocol: "https",
        hostname: "cdn.grofers.com",
      },
      {
        protocol: "https",
        hostname: "**.flixcart.com",
      },
      {
        protocol: "https",
        hostname: "**.bbassets.com",
      },
      {
        protocol: "https",
        hostname: "**.bigcommerce.com",
      },
      {
        protocol: "https",
        hostname: "**.nutrabay.com",
      },
      {
        protocol: "https",
        hostname: "**.b-cdn.net",
      },
      {
        protocol: "https",
        hostname: "**.hkrtcdn.com",
      },
      {
        protocol: "https",
        hostname: "**.farziengineer.co",
      },
      {
        protocol: "https",
        hostname: "**.avvatarindia.com",
      },
    ],
  },
};

export default nextConfig;
