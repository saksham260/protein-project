import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  images: {
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
