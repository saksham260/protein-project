"use client";

import React, { useState } from "react";
import { useAuth } from "@/context/AuthContext";
import { clearActivity } from "@/lib/activity";
import { clearSearches } from "@/lib/searchHistory";
import { createClient } from "@/lib/supabase/client";

const BUTTON = "px-4 py-2.5 rounded-xl text-xs font-mono font-bold border transition-colors cursor-pointer disabled:opacity-50";

/** Lets a signed-in person wipe their history or their whole account. */
export const AccountControls: React.FC = () => {
  const { user, isReady, signOut } = useAuth();
  const [message, setMessage] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);

  if (!isReady) return null;
  if (!user) {
    return <p className="text-xs font-mono text-[#968E85]">Sign in to clear your history or delete your account.</p>;
  }

  const forgetLocally = () => {
    try {
      localStorage.removeItem(`suggested:v1:${user.id}`);
    } catch {
      // Storage blocked: nothing was saved here anyway.
    }
  };

  const clearHistory = async () => {
    setBusy(true);
    const [activityCleared, searchesCleared] = await Promise.all([clearActivity(user.id), clearSearches(user.id)]);
    forgetLocally();
    setBusy(false);
    setMessage(activityCleared && searchesCleared ? "Your history has been cleared." : "Part of your history couldn't be cleared. Please try again.");
  };

  const deleteAccount = async () => {
    if (!window.confirm("Delete your account and all saved history? This can't be undone.")) return;
    setBusy(true);
    const { error } = await createClient().rpc("delete_my_account");
    if (error) {
      setBusy(false);
      setMessage("Your account couldn't be deleted. Please try again.");
      return;
    }
    forgetLocally();
    await signOut();
    setBusy(false);
    setMessage("Your account has been deleted.");
  };

  return (
    <div className="flex flex-col gap-3 p-4 rounded-2xl bg-[#1C1916] border border-[#332D27]">
      <div className="flex flex-wrap gap-2">
        <button
          type="button"
          disabled={busy}
          onClick={clearHistory}
          className={`${BUTTON} bg-[#26221E] text-[#F5F2EB] border-[#332D27] hover:border-[#D97706]/60`}
        >
          Clear my history
        </button>
        <button
          type="button"
          disabled={busy}
          onClick={deleteAccount}
          className={`${BUTTON} bg-[#DC2626]/15 text-[#F87171] border-[#EF4444]/40 hover:bg-[#DC2626]/25`}
        >
          Delete my account
        </button>
      </div>
      {message && (
        <p role="status" className="text-xs font-mono text-[#34D399]">
          {message}
        </p>
      )}
    </div>
  );
};
