import type { Metadata } from "next";
import { Inter, Outfit } from "next/font/google";
import { Navbar } from "@/components/layout/Navbar";
import { Footer } from "@/components/layout/Footer";
import "./globals.css";

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-inter",
  display: "swap",
});

const outfit = Outfit({
  subsets: ["latin"],
  variable: "--font-outfit",
  display: "swap",
});

export const metadata: Metadata = {
  title: "The Protein Discovery Engine — India's Independent Protein Transparency Platform",
  description:
    "Discover verified protein products in India. Real cost-per-gram (₹/g), protein density %, red-flag ingredient scans (maltitol, amino spiking), and 4-tier protein quality ratings.",
  keywords: [
    "protein powder India",
    "best protein bar",
    "whey protein price per gram",
    "cheapest protein India",
    "clean protein bars without maltitol",
  ],
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className={`${inter.variable} ${outfit.variable} dark`}>
      <body className="min-h-screen flex flex-col bg-[#0a0a0f] text-[#f8fafc]">
        <Navbar />
        <main className="flex-1 w-full">{children}</main>
        <Footer />
      </body>
    </html>
  );
}
