import { createBrowserClient } from "@supabase/ssr";

export function createClient() {
  const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL;
  const supabaseKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;

  if (!supabaseUrl || !supabaseKey) {
    throw new Error("Missing NEXT_PUBLIC_SUPABASE_URL or NEXT_PUBLIC_SUPABASE_ANON_KEY");
  }

  return createBrowserClient(supabaseUrl, supabaseKey);
}

/** True when real (non-placeholder, non-example) Supabase credentials are configured. */
export function isSupabaseConfigured(): boolean {
  const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL?.trim();
  const supabaseKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY?.trim();

  if (!supabaseUrl || !supabaseKey) return false;

  const isInvalidUrl =
    supabaseUrl.includes("placeholder") ||
    supabaseUrl.includes("your-project") ||
    !supabaseUrl.startsWith("https://");

  const isInvalidKey =
    supabaseKey.includes("placeholder") ||
    supabaseKey.includes("your-anon-key") ||
    supabaseKey.length < 20;

  return !isInvalidUrl && !isInvalidKey;
}

