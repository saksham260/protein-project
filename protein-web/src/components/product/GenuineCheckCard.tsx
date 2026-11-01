import React from "react";

const FOSCOS_URL = "https://foscos.fssai.gov.in/";

export interface GenuineCheckCardProps {
  brandName: string;
  /** The brand's own product page, when we have one. */
  brandStoreUrl?: string;
}

/** General steps for spotting a fake. We don't check sellers or batches, so this never rules on a pack. */
export const GenuineCheckCard: React.FC<GenuineCheckCardProps> = ({ brandName, brandStoreUrl }) => (
  <details className="group/genuine rounded-3xl bg-[#18181B] border border-[#27272A] shadow-[0_12px_40px_rgba(0,0,0,0.6)]">
    <summary className="flex items-center justify-between gap-3 p-5 cursor-pointer select-none list-none">
      <span className="text-sm font-bold text-white tracking-tight">🔎 How to check your pack is genuine</span>
      <span className="text-xs font-mono text-[#A1A1AA] group-open/genuine:rotate-180 transition-transform">▾</span>
    </summary>

    <div className="flex flex-col gap-3 px-5 pb-5">
      <ol className="list-decimal pl-5 flex flex-col gap-2 text-xs text-[#E4E4E7] leading-relaxed">
        <li>
          Buy from a seller you can trust.{" "}
          {brandStoreUrl ? (
            <a href={brandStoreUrl} target="_blank" rel="noopener noreferrer" className="text-[#D97706] hover:underline">
              {brandName}&apos;s own store ↗
            </a>
          ) : (
            `${brandName}'s own store`
          )}{" "}
          is the safest. On marketplaces, check who is selling it.
        </li>
        <li>
          Find the 14-digit FSSAI licence number on the pack and look it up with FBO Search on{" "}
          <a href={FOSCOS_URL} target="_blank" rel="noopener noreferrer" className="text-[#D97706] hover:underline">
            FSSAI&apos;s FoSCoS site ↗
          </a>
          . The name should match the company on the label.
        </li>
        <li>Check the seal, batch number, expiry date and MRP are printed clearly and match on the box and tub.</li>
        <li>If the pack has a QR, scratch or SMS code, use it, and only through the brand&apos;s official site or app.</li>
        <li>Be careful with prices far below every other store. Counterfeit protein has been seized in India.</li>
      </ol>
      <p className="text-[11px] text-[#A1A1AA] leading-relaxed">
        These are general tips. We don&apos;t check individual sellers or batches. If you think a product is fake, tell the
        seller and FSSAI.
      </p>
    </div>
  </details>
);
