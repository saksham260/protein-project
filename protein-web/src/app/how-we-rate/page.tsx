import React from "react";
import { InfoPage, InfoSection } from "@/components/layout/InfoPage";
import { SITE_NAME } from "@/lib/site";

export const metadata = {
  title: `How We Rate — ${SITE_NAME}`,
  description: "How cost per gram, protein density, tiers, red flags and Top Picks are worked out, and what we can't check.",
  alternates: { canonical: "/how-we-rate" },
};

export default function HowWeRatePage() {
  return (
    <InfoPage title="How We Rate" updated="1 November 2026">
      <InfoSection title="Where the data comes from">
        <p>
          Product labels and brand listings. <strong className="text-[#F5F2EB]">We don&apos;t test products in a lab</strong>,
          so we can&apos;t confirm that a label is accurate or that a product is free of contaminants. Everything below
          is calculated from what the label says.
        </p>
      </InfoSection>

      <InfoSection title="Cost per gram of protein (₹/g)">
        <p>
          Price divided by the total protein in the pack. We use the lowest store price we know of, or MRP if we don&apos;t
          have one. Lower is better value.
        </p>
      </InfoSection>

      <InfoSection title="Protein density">
        <p>The share of a product&apos;s calories that come from protein. Higher means leaner.</p>
      </InfoSection>

      <InfoSection title="Net carbs">
        <p>
          Total carbs minus fibre. We also subtract sweeteners the body barely absorbs, such as erythritol, but not
          maltitol and similar polyols, because they still raise blood sugar.
        </p>
      </InfoSection>

      <InfoSection title="Protein tiers">
        <p>
          A guide to the main protein source named on the label, from isolates (Tier 1) through concentrates (Tier 2)
          and plant proteins (Tier 3). Tier 4 covers incomplete proteins such as collagen, and products whose label
          lists added free-form amino acids. Added amino acids aren&apos;t always a bad sign: some are there to fortify a
          product. A tier says nothing about how a product was made or tested.
        </p>
      </InfoSection>

      <InfoSection title="Red flags">
        <p>
          An automated scan of the ingredient list for maltitol, added free-form amino acids, hydrogenated or palm
          fats, and hidden sugars. A flag means the ingredient is listed, not that the product is unsafe. If we have no
          ingredient list, we say so and don&apos;t count the product as flag-free.
        </p>
      </InfoSection>

      <InfoSection title="Top Picks">
        <p>
          Chosen by formula: the lowest cost per gram in each category, among in-stock products with an ingredient list
          and no red flags. They are the best value on paper, not personal recommendations or test winners.
        </p>
      </InfoSection>

      <InfoSection title="Best value lists">
        <p>
          Each list ranks products by cost per gram of protein, using each product&apos;s best-value in-stock pack. Only
          products with an ingredient list and no red flags can appear.
        </p>
      </InfoSection>

      <InfoSection title="Lab reports">
        <p>
          Where a test has been published, we link to it from the product page and say who published it. A report covers
          the batch tested, not every pack. Reports supplied by a brand are labelled as such. Most products have none, and
          that tells you nothing either way.
        </p>
      </InfoSection>

      <InfoSection title="Default product order">
        <p>
          &quot;Featured&quot; puts single items before multi-packs, then better-known brands, then lower cost per gram.
          It helps people find familiar products, so it does favour big brands. Pick another sort to change this.
        </p>
      </InfoSection>

      <InfoSection title="Commissions">
        <p>
          We may earn a commission from some store links. Commissions play no part in tiers, red flags, Top Picks or
          product order, and no brand can pay to change them.
        </p>
      </InfoSection>
    </InfoPage>
  );
}
