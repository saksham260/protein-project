import { createClient, isSupabaseConfigured } from "@/lib/supabase/client";

export const MAX_RECENT_SHOWN = 8;
const MIN_QUERY_LENGTH = 2;
const MAX_QUERY_LENGTH = 80;

export interface RecentSearch {
  query: string;
  /** Lower-cased, single-spaced form used to tell "Whey" and "whey " apart from other searches. */
  key: string;
}

/** Clean up what was typed. Returns null when it is too short to be worth remembering. */
export function toRecentSearch(raw: string): RecentSearch | null {
  const query = raw.trim().replace(/\s+/g, " ").slice(0, MAX_QUERY_LENGTH);
  if (query.length < MIN_QUERY_LENGTH) return null;
  return { query, key: query.toLowerCase() };
}

/** Put a search at the top of the list (no duplicates) and keep the list short. */
export function withSearchFirst(list: RecentSearch[], search: RecentSearch, limit = MAX_RECENT_SHOWN): RecentSearch[] {
  return [search, ...list.filter((s) => s.key !== search.key)].slice(0, limit);
}

/** Save a search for the signed-in user; searching the same thing again just refreshes its time. Fails quietly. */
export async function saveSearch(userId: string, search: RecentSearch): Promise<boolean> {
  if (!isSupabaseConfigured()) return false;
  const { error } = await createClient()
    .from("user_searches")
    .upsert(
      { user_id: userId, query: search.query, query_key: search.key, created_at: new Date().toISOString() },
      { onConflict: "user_id,query_key" }
    );
  return !error;
}

/** The signed-in user's latest searches, newest first. */
export async function getRecentSearches(userId: string, limit = MAX_RECENT_SHOWN): Promise<RecentSearch[]> {
  if (!isSupabaseConfigured()) return [];
  const { data, error } = await createClient()
    .from("user_searches")
    .select("query, query_key")
    .eq("user_id", userId)
    .order("created_at", { ascending: false })
    .limit(limit);
  if (error || !data) return [];
  return data.map((row: { query: string; query_key: string }) => ({ query: row.query, key: row.query_key }));
}

export async function deleteSearch(userId: string, key: string): Promise<boolean> {
  if (!isSupabaseConfigured()) return false;
  const { error } = await createClient().from("user_searches").delete().eq("user_id", userId).eq("query_key", key);
  return !error;
}

export async function clearSearches(userId: string): Promise<boolean> {
  if (!isSupabaseConfigured()) return false;
  const { error } = await createClient().from("user_searches").delete().eq("user_id", userId);
  return !error;
}
