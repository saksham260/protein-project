import { NextResponse } from "next/server";
import { createClient } from "@/lib/supabase/server";
import { isSupabaseConfigured } from "@/lib/supabase/client";
import { publicOrigin, safeNextPath } from "@/lib/auth";

/** Google sends the visitor back here (via Supabase) with a one-time `code`; swap it for a session cookie. */
export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const origin = publicOrigin(request.url, request.headers);
  const code = searchParams.get("code");
  const next = safeNextPath(searchParams.get("next"));

  if (code && isSupabaseConfigured()) {
    const supabase = await createClient();
    const { error } = await supabase.auth.exchangeCodeForSession(code);
    if (!error) return NextResponse.redirect(`${origin}${next}`);
  }

  return NextResponse.redirect(`${origin}/?auth_error=1`);
}
