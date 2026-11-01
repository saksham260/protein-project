import React from "react";
import { InfoPage, InfoSection } from "@/components/layout/InfoPage";
import { SITE_NAME } from "@/lib/site";
import { CostCalculator } from "./CostCalculator";

const ICMR_NOTE_URL = "https://www.nin.res.in/rdabook/brief_note.pdf";
const GUIDELINES_NEWS_URL =
  "https://www.dtnext.in/lifestyle/wellbeing/why-do-icmr-nins-new-dietary-guidelines-advise-against-protein-supplements-784773";

export const metadata = {
  title: `Protein Cost Calculator — ${SITE_NAME}`,
  description: "See what a daily amount of protein costs per day and per month across protein products in India.",
  alternates: { canonical: "/protein-cost-calculator" },
};

export default function ProteinCostCalculatorPage() {
  return (
    <InfoPage title="Protein Cost Calculator">
      <p>
        Choose how much protein you want from a product each day, and see what it costs across the catalog. This is a sum
        about cost, not advice on how much protein you need.
      </p>

      <CostCalculator />

      <InfoSection title="Before you buy">
        <p>
          ICMR-NIN&apos;s{" "}
          <a href={ICMR_NOTE_URL} target="_blank" rel="noopener noreferrer" className="text-[#D97706] hover:underline">
            2020 requirements
          </a>{" "}
          set a safe protein intake of 0.83g per kg of body weight a day for healthy Indian adults, or 1g per kg for people on
          cereal-based diets with low-quality protein. Its{" "}
          <a href={GUIDELINES_NEWS_URL} target="_blank" rel="noopener noreferrer" className="text-[#D97706] hover:underline">
            2024 dietary guidelines
          </a>{" "}
          were reported as saying a balanced diet can meet these needs, and as advising healthy people against protein
          supplements. Food may be a cheaper way to get your protein.
        </p>
        <p>
          Talk to a doctor or dietitian first if you are pregnant, have a health condition such as kidney disease, or are
          buying for a child.
        </p>
      </InfoSection>

      <InfoSection title="How it works">
        <p>
          Cost per day is your daily grams multiplied by the product&apos;s cost per gram of protein. Each product shows its
          best-value in-stock pack. Prices are the lowest we know of, or MRP, and can change.
        </p>
      </InfoSection>
    </InfoPage>
  );
}
