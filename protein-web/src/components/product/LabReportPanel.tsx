import React from "react";
import type { ProductVariant, TestReport } from "@/types/product";
import { costPerTestedGram } from "@/lib/metrics";
import { formatPricePerGram } from "@/lib/utils";

const RESULT_LABELS: Record<TestReport["result"], string> = {
  pass: "Pass",
  partial: "Partly met",
  fail: "Did not meet",
};

const dateFormat = new Intl.DateTimeFormat("en-IN", { month: "short", year: "numeric", timeZone: "Asia/Kolkata" });

export interface LabReportPanelProps {
  reports: TestReport[];
  variant: ProductVariant;
}

/** Published test results for this product, or a plain statement that we have none. */
export const LabReportPanel: React.FC<LabReportPanelProps> = ({ reports, variant }) => {
  const relevant = reports.filter((report) => !report.variant_id || report.variant_id === variant.id);

  return (
    <div className="flex flex-col gap-3 p-6 rounded-3xl bg-[#18181B] border border-[#27272A] shadow-[0_12px_40px_rgba(0,0,0,0.6)]">
      <h3 className="text-xs font-mono uppercase tracking-widest text-[#A1A1AA] font-bold">Lab Reports</h3>

      {relevant.length === 0 ? (
        <p className="text-xs text-[#A1A1AA] leading-relaxed">
          We have no lab report on file for this product. That doesn&apos;t tell you anything either way. Everything else on
          this page comes from the label.
        </p>
      ) : (
        <>
          <ul className="flex flex-col gap-3">
            {relevant.map((report) => {
              const testedCost =
                report.tested_protein_g_per_100g != null
                  ? costPerTestedGram(variant, report.tested_protein_g_per_100g)
                  : null;

              return (
                <li key={report.id} className="flex flex-col gap-1.5 p-4 rounded-2xl bg-[#27272A]/60 border border-[#27272A]">
                  <div className="flex flex-wrap items-center justify-between gap-2">
                    <span className="text-sm font-bold text-white">{report.source_name}</span>
                    <span className="text-[10px] font-mono uppercase px-2 py-0.5 rounded-full bg-[#27272A] text-[#E4E4E7] border border-[#3F3F46]">
                      {report.source_type === "independent" ? "Independent test" : "Supplied by the brand"}
                    </span>
                  </div>
                  <p className="text-xs font-mono text-[#E4E4E7]">Report&apos;s result: {RESULT_LABELS[report.result]}</p>
                  <p className="text-xs font-mono text-[#A1A1AA]">
                    Tested {dateFormat.format(new Date(report.tested_on))}
                    {report.batch_number && ` · Batch ${report.batch_number}`}
                    {report.lab_name && ` · ${report.lab_name}`}
                  </p>
                  {report.tested_protein_g_per_100g != null && (
                    <p className="text-xs font-mono text-[#E4E4E7]">
                      Tested protein: {Number(report.tested_protein_g_per_100g)}g per 100g
                      {testedCost !== null && ` · ${formatPricePerGram(testedCost)} on tested protein`}
                    </p>
                  )}
                  <a
                    href={report.report_url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-xs font-mono font-bold text-[#D97706] hover:underline w-fit"
                  >
                    View the report ↗
                  </a>
                </li>
              );
            })}
          </ul>
          <p className="text-[11px] text-[#A1A1AA] leading-relaxed">
            A test covers the batch tested, not every pack. Your pack may differ.
          </p>
        </>
      )}
    </div>
  );
};
