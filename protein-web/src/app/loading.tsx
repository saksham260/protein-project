export default function Loading() {
  return (
    <div className="container max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3 sm:gap-6" aria-hidden>
        {[1, 2, 3, 4, 5, 6, 7, 8].map((i) => (
          <div key={i} className="h-72 rounded-2xl bg-[#1C1916] border border-[#332D27] skeleton-shimmer" />
        ))}
      </div>
    </div>
  );
}
