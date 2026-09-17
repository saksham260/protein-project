import type { Metadata } from "next";
import { Inter, JetBrains_Mono } from "next/font/google";
import BackgroundShader from "@/components/ui/BackgroundShader";
import { Navbar } from "@/components/layout/Navbar";
import { Footer } from "@/components/layout/Footer";
import { CartProvider } from "@/context/CartContext";
import { CartDrawer } from "@/components/cart/CartDrawer";
import "./globals.css";

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-inter",
  display: "swap",
});

const jetbrainsMono = JetBrains_Mono({
  subsets: ["latin"],
  variable: "--font-mono-code",
  display: "swap",
});

export const metadata: Metadata = {
  title: "The Protein Discovery Engine — Independent Protein Transparency",
  description:
    "Deconstruct packaged protein mathematically and scientifically. True cost-per-gram (₹/g), protein density %, red-flag scans (maltitol, amino spiking), and 4-tier ratings.",
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
    <html lang="en" className={`${inter.variable} ${jetbrainsMono.variable} dark`}>
      <body className="min-h-screen flex flex-col bg-[#0A0A0B] text-[#E4E4E7] font-sans antialiased selection:bg-[#10B981] selection:text-[#0A0A0B] relative">
        <CartProvider>
          <BackgroundShader />
          <div className="relative z-10 flex flex-col min-h-screen">
            <Navbar />
            <main className="flex-1 w-full">{children}</main>
            <Footer />
          </div>
          <CartDrawer />
        </CartProvider>
      </body>
    </html>
  );
}
