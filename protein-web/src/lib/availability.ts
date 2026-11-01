import { AvailabilitySummary, QuickCommercePlatform } from "@/types/product";
import { createClient, isSupabaseConfigured } from "@/lib/supabase/client";

export const PINCODE_PATTERN = /^[1-9][0-9]{5}$/;

/** Postal district = first 3 pincode digits; reports are grouped at this level. */
export function areaCode(pincode: string): string {
  return pincode.slice(0, 3);
}

/** Crowd-sourced availability for the given variants in the user's area (last 30 days). */
export async function getAvailabilitySummaries(
  variantIds: string[],
  pincode: string
): Promise<AvailabilitySummary[]> {
  if (!isSupabaseConfigured() || variantIds.length === 0 || !PINCODE_PATTERN.test(pincode)) return [];
  const { data, error } = await createClient()
    .from("availability_summary")
    .select("*")
    .in("variant_id", variantIds)
    .eq("area_code", areaCode(pincode));
  return error || !data ? [] : (data as AvailabilitySummary[]);
}

/** Record a "was it available?" answer. Returns false when the database is not connected. */
export async function reportAvailability(
  variantId: string,
  platform: QuickCommercePlatform,
  pincode: string,
  isAvailable: boolean
): Promise<boolean> {
  if (!isSupabaseConfigured() || !PINCODE_PATTERN.test(pincode)) return false;
  const { error } = await createClient()
    .from("availability_reports")
    .insert({ variant_id: variantId, platform, pincode, is_available: isAvailable });
  return !error;
}

/** One person's report isn't enough to tell other shoppers something is in stock. */
export const MIN_REPORTS_TO_TRUST = 2;

/** Reported available when at least two people said yes, and more said yes than no. */
export function isReportedAvailable(s: Pick<AvailabilitySummary, "yes_count" | "no_count">): boolean {
  return s.yes_count >= MIN_REPORTS_TO_TRUST && s.yes_count > s.no_count;
}
