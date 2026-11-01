import Link from "next/link";

export default function NotFound() {
  return (
    <div className="container max-w-xl mx-auto px-4 py-24 flex flex-col items-center text-center gap-4">
      <span className="text-5xl">🔎</span>
      <h1 className="text-2xl sm:text-3xl font-black text-[#F5F2EB] tracking-tight">Page not found</h1>
      <p className="text-sm text-[#968E85]">This product may have been removed, or the link may be wrong.</p>
      <Link
        href="/explore"
        className="mt-2 px-6 py-2.5 rounded-xl bg-[#D97706] hover:bg-[#B45309] text-white text-xs font-bold transition-colors"
      >
        Browse all products
      </Link>
    </div>
  );
}
