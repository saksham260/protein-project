"use client";

import React, { useState } from "react";
import { usePincode } from "@/hooks/usePincode";
import { PINCODE_PATTERN } from "@/lib/availability";
import { cn } from "@/lib/utils";

export interface PincodeInputProps {
  className?: string;
}

/** Compact pincode entry; shows the saved pincode with a "Change" link once set. */
export const PincodeInput: React.FC<PincodeInputProps> = ({ className }) => {
  const { pincode, setPincode } = usePincode();
  const [draft, setDraft] = useState("");
  const [editing, setEditing] = useState(false);
  const isValid = PINCODE_PATTERN.test(draft);

  if (pincode && !editing) {
    return (
      <div className={cn("flex items-center justify-between gap-3 text-xs font-mono", className)}>
        <span className="text-[#A1A1AA]">
          Delivering to <span className="text-white font-bold">{pincode}</span>
        </span>
        <button
          type="button"
          onClick={() => {
            setDraft(pincode);
            setEditing(true);
          }}
          className="text-[#34D399] hover:text-white transition-colors cursor-pointer"
        >
          Change
        </button>
      </div>
    );
  }

  return (
    <form
      className={cn("flex items-center gap-2", className)}
      onSubmit={(e) => {
        e.preventDefault();
        if (!isValid) return;
        setPincode(draft);
        setEditing(false);
      }}
    >
      <input
        type="text"
        inputMode="numeric"
        autoComplete="postal-code"
        maxLength={6}
        value={draft}
        onChange={(e) => setDraft(e.target.value.replace(/\D/g, ""))}
        placeholder="Your pincode"
        aria-label="Your pincode"
        className="w-full min-w-0 px-3 py-2 rounded-xl bg-[#27272A] border border-[#3F3F46] text-xs font-mono text-white placeholder:text-zinc-500 focus:outline-none focus:border-[#10B981]"
      />
      <button
        type="submit"
        disabled={!isValid}
        className="px-3 py-2 rounded-xl text-xs font-mono font-bold bg-[#10B981] text-black disabled:bg-[#27272A] disabled:text-zinc-500 transition-colors cursor-pointer disabled:cursor-not-allowed"
      >
        Save
      </button>
    </form>
  );
};
