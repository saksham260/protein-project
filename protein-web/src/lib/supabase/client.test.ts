import { describe, it, expect, beforeEach, afterEach } from "vitest";
import { isSupabaseConfigured } from "./client";

describe("Suite: Supabase Client Configuration Guard", () => {
  const originalUrl = process.env.NEXT_PUBLIC_SUPABASE_URL;
  const originalKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;

  afterEach(() => {
    process.env.NEXT_PUBLIC_SUPABASE_URL = originalUrl;
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY = originalKey;
  });

  it("returns false when env variables are empty or missing", () => {
    delete process.env.NEXT_PUBLIC_SUPABASE_URL;
    delete process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;
    expect(isSupabaseConfigured()).toBe(false);
  });

  it("returns false when using placeholder URL or key", () => {
    process.env.NEXT_PUBLIC_SUPABASE_URL = "https://placeholder-project.supabase.co";
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY = "placeholder-anon-key";
    expect(isSupabaseConfigured()).toBe(false);
  });

  it("returns false when using template example URL or key", () => {
    process.env.NEXT_PUBLIC_SUPABASE_URL = "https://your-project.supabase.co";
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY = "your-anon-key-here";
    expect(isSupabaseConfigured()).toBe(false);
  });

  it("returns false when URL does not start with https://", () => {
    process.env.NEXT_PUBLIC_SUPABASE_URL = "http://my-project.supabase.co";
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY = "sb_publishable_validkeylength_1234567890";
    expect(isSupabaseConfigured()).toBe(false);
  });

  it("returns false when key is too short", () => {
    process.env.NEXT_PUBLIC_SUPABASE_URL = "https://validproject.supabase.co";
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY = "short-key";
    expect(isSupabaseConfigured()).toBe(false);
  });

  it("returns true when valid Supabase URL and key are provided", () => {
    process.env.NEXT_PUBLIC_SUPABASE_URL = "https://xyzcompany.supabase.co";
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY = "sb_publishable_valid_long_key_abcdef1234567890";
    expect(isSupabaseConfigured()).toBe(true);
  });

  it("returns true for legacy JWT anon keys", () => {
    process.env.NEXT_PUBLIC_SUPABASE_URL = "https://xyzcompany.supabase.co";
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.validpayload.signature";
    expect(isSupabaseConfigured()).toBe(true);
  });
});
