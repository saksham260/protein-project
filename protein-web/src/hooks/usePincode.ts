"use client";

import { useCallback, useSyncExternalStore } from "react";
import { PINCODE_PATTERN } from "@/lib/availability";

const STORAGE_KEY = "protein-engine-pincode";
const CHANGE_EVENT = "protein-engine-pincode-change";

function read(): string {
  try {
    const value = window.localStorage.getItem(STORAGE_KEY) || "";
    return PINCODE_PATTERN.test(value) ? value : "";
  } catch {
    return "";
  }
}

function subscribe(onChange: () => void): () => void {
  window.addEventListener(CHANGE_EVENT, onChange);
  window.addEventListener("storage", onChange);
  return () => {
    window.removeEventListener(CHANGE_EVENT, onChange);
    window.removeEventListener("storage", onChange);
  };
}

/** The viewer's pincode, kept in this browser only and shared by every component using the hook. */
export function usePincode() {
  const pincode = useSyncExternalStore(subscribe, read, () => "");

  const setPincode = useCallback((value: string) => {
    try {
      if (value) window.localStorage.setItem(STORAGE_KEY, value);
      else window.localStorage.removeItem(STORAGE_KEY);
    } catch {
      // Storage blocked (private mode): the pincode just won't persist.
    }
    window.dispatchEvent(new Event(CHANGE_EVENT));
  }, []);

  return { pincode, setPincode };
}
