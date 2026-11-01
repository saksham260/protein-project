import React from "react";
import Link from "next/link";
import { InfoPage, InfoSection } from "@/components/layout/InfoPage";
import { AMAZON_DISCLOSURE } from "@/lib/constants";
import { SITE_NAME } from "@/lib/site";

export const metadata = {
  title: `Terms of Use — ${SITE_NAME}`,
  description: "What this site is, what it isn't, and the limits of the information shown here.",
  alternates: { canonical: "/terms" },
};

export default function TermsPage() {
  return (
    <InfoPage title="Terms of Use" updated="1 November 2026">
      <InfoSection title="What this site is">
        <p>
          A comparison site for packaged protein products sold in India. We don&apos;t sell anything: store links take
          you to the seller, and your purchase is between you and that seller.
        </p>
      </InfoSection>

      <InfoSection title="Not medical advice">
        <p>
          Nothing here is medical or dietary advice. Talk to a doctor or dietitian before using these products,
          especially if you are pregnant, have a health condition, or are buying for a child.
        </p>
      </InfoSection>

      <InfoSection title="Check the pack">
        <p>
          Our information comes from product labels and brand listings. We don&apos;t test products, so it can be
          incomplete, out of date or wrong. <strong className="text-[#F5F2EB]">If you have an allergy, always read the
          pack before buying or eating a product.</strong> Don&apos;t rely on this site&apos;s filters alone.
        </p>
        <p>
          Red flags and tiers are automated readings of the label, not lab results or a verdict on a brand. See{" "}
          <Link href="/how-we-rate" className="text-[#D97706] hover:underline">
            how we rate
          </Link>
          .
        </p>
      </InfoSection>

      <InfoSection title="Prices and availability">
        <p>
          Prices and stock change often and can differ from what we show. The store&apos;s own page is always correct.
          Quick-commerce availability comes from shopper reports and can be wrong.
        </p>
      </InfoSection>

      <InfoSection title="Commissions">
        <p>We may earn a commission when you buy through a store link, at no extra cost to you.</p>
        <p>{AMAZON_DISCLOSURE}</p>
      </InfoSection>

      <InfoSection title="Fair use">
        <p>Please don&apos;t submit false availability reports, or try to overload or copy the site.</p>
      </InfoSection>
    </InfoPage>
  );
}
