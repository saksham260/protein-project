import type { Metadata, Viewport } from "next";
import { Plus_Jakarta_Sans, JetBrains_Mono } from "next/font/google";
import { Navbar } from "@/components/layout/Navbar";
import { Footer } from "@/components/layout/Footer";
import { AuthProvider } from "@/context/AuthContext";
import { CartProvider } from "@/context/CartContext";
import { CategoryProvider } from "@/context/CategoryContext";
import { CartDrawer } from "@/components/cart/CartDrawer";
import { SITE_NAME, siteUrl } from "@/lib/site";
import "./globals.css";

const plusJakartaSans = Plus_Jakarta_Sans({
  subsets: ["latin"],
  variable: "--font-inter",
  display: "swap",
});

const jetbrainsMono = JetBrains_Mono({
  subsets: ["latin"],
  variable: "--font-mono-code",
  display: "swap",
});

export const viewport: Viewport = {
  width: "device-width",
  initialScale: 1,
  maximumScale: 5,
};

const SITE_TITLE = `${SITE_NAME} — Compare Protein Products in India`;
const SITE_DESCRIPTION =
  "Compare packaged protein products in India by true cost per gram (₹/g), protein density, label red flags (maltitol, added amino acids) and protein source.";

export const metadata: Metadata = {
  metadataBase: new URL(siteUrl()),
  title: SITE_TITLE,
  description: SITE_DESCRIPTION,
  openGraph: { title: SITE_TITLE, description: SITE_DESCRIPTION, siteName: SITE_NAME, locale: "en_IN", type: "website" },
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
    <html lang="en" className={`${plusJakartaSans.variable} ${jetbrainsMono.variable}`}>
      <body className="min-h-screen flex flex-col bg-[var(--bg-primary)] text-[var(--text-primary)] font-sans antialiased selection:bg-[var(--color-primary)] selection:text-white relative">
        <AuthProvider>
          <CartProvider>
            <CategoryProvider>
              <div className="relative z-10 flex flex-col min-h-screen">
                <Navbar />
                <main className="flex-1 w-full">{children}</main>
                <Footer />
              </div>
              <CartDrawer />
            </CategoryProvider>
          </CartProvider>
        </AuthProvider>
      </body>
    </html>
  );
}
