import React from "react";
import { AccountControls } from "@/components/account/AccountControls";
import { InfoPage, InfoSection } from "@/components/layout/InfoPage";
import { CONTACT_EMAIL, SITE_NAME } from "@/lib/site";

export const metadata = {
  title: `Privacy Policy — ${SITE_NAME}`,
  description: "What we collect, why we collect it, and how to clear your history or delete your account.",
  alternates: { canonical: "/privacy" },
};

export default function PrivacyPage() {
  return (
    <InfoPage title="Privacy Policy" updated="1 November 2026">
      <p>
        You can use most of this site without an account. This page explains what we store when you do sign in,
        and what stays in your own browser.
      </p>

      <InfoSection title="If you sign in with Google">
        <ul className="list-disc pl-5 flex flex-col gap-1.5">
          <li>Your name, email address and profile picture, sent to us by Google.</li>
          <li>Products you open and the stores you click through to, so we can show them again on the home page.</li>
          <li>What you type into the search bar, so we can show your recent searches.</li>
        </ul>
      </InfoSection>

      <InfoSection title="If you don't sign in">
        <ul className="list-disc pl-5 flex flex-col gap-1.5">
          <li>
            Your pincode and cart are saved in your own browser. When you look up reports for your area, the first
            three digits of your pincode are used for that search, and the search isn&apos;t saved.
          </li>
          <li>
            If you answer &quot;Was it available?&quot;, we store your answer with the product, the store and your
            pincode. It isn&apos;t linked to you, and other visitors only see totals for your postal district.
          </li>
          <li>We count clicks through to stores by product and store. These counts aren&apos;t linked to you.</li>
        </ul>
      </InfoSection>

      <InfoSection title="How we use it">
        <p>
          Only to run the features above. We don&apos;t sell your data, and we don&apos;t use advertising trackers.
          Your data is held by the companies that host our website and database, who process it on our behalf.
        </p>
      </InfoSection>

      <InfoSection title="Stores and commissions">
        <p>
          Store links take you to other companies&apos; websites, which have their own privacy policies. Some links
          let the store know the click came from us, so that we can earn a commission.
        </p>
      </InfoSection>

      <InfoSection id="your-data" title="Your choices">
        <p>
          Clearing your history removes your saved views, clicks and searches. Deleting your account removes these
          and your profile for good.
        </p>
        <AccountControls />
      </InfoSection>

      {CONTACT_EMAIL && (
        <InfoSection title="Contact">
          <p>
            Questions about your data: <a className="text-[#D97706] hover:underline" href={`mailto:${CONTACT_EMAIL}`}>{CONTACT_EMAIL}</a>
          </p>
        </InfoSection>
      )}
    </InfoPage>
  );
}
