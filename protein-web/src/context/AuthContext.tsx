"use client";

import React, { createContext, useCallback, useContext, useEffect, useMemo, useState } from "react";
import type { User } from "@supabase/supabase-js";
import { createClient, isSupabaseConfigured } from "@/lib/supabase/client";

interface AuthContextType {
  user: User | null;
  /** False until the first session check finishes, so the UI doesn't flash "Login" for signed-in users. */
  isReady: boolean;
  /** False when no Supabase keys are set (e.g. local demo mode): sign-in can't work. */
  isAvailable: boolean;
  signInWithGoogle: () => Promise<void>;
  signOut: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const isAvailable = isSupabaseConfigured();
  const [user, setUser] = useState<User | null>(null);
  const [isReady, setIsReady] = useState(!isAvailable);

  useEffect(() => {
    if (!isAvailable) return;
    const supabase = createClient();
    supabase.auth.getUser().then(({ data }) => {
      setUser(data.user);
      setIsReady(true);
    });
    const { data } = supabase.auth.onAuthStateChange((_event, session) => {
      setUser(session?.user ?? null);
    });
    return () => data.subscription.unsubscribe();
  }, [isAvailable]);

  const signInWithGoogle = useCallback(async () => {
    if (!isAvailable) return;
    const next = window.location.pathname + window.location.search;
    await createClient().auth.signInWithOAuth({
      provider: "google",
      options: { redirectTo: `${window.location.origin}/auth/callback?next=${encodeURIComponent(next)}` },
    });
  }, [isAvailable]);

  const signOut = useCallback(async () => {
    if (!isAvailable) return;
    await createClient().auth.signOut();
    setUser(null);
  }, [isAvailable]);

  const value = useMemo(
    () => ({ user, isReady, isAvailable, signInWithGoogle, signOut }),
    [user, isReady, isAvailable, signInWithGoogle, signOut]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export function useAuth(): AuthContextType {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used inside <AuthProvider>");
  return ctx;
}
