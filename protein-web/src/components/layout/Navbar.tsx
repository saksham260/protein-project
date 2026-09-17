"use client";

import React, { useState, useEffect, useRef } from "react";
import Link from "next/link";
import { NavbarSearch } from "@/components/search/NavbarSearch";
import { CartButton } from "@/components/cart/CartButton";
import { LoginButton } from "@/components/auth/LoginButton";
import { cn } from "@/lib/utils";

// --- Originkit Light Glass Engine Constants & Utilities ---
const BLUR = 20;
const TINT = 0.55;
const STROKE_BRIGHTNESS = 140;
const LIGHT_FADE = 0.6;
const AIM_BLEND = 0.18;

const LIGHT_FALLOFF: Array<[number, number]> = [
  [0, 1],
  [0.08, 0.95],
  [0.18, 0.85],
  [0.3, 0.7],
  [0.42, 0.54],
  [0.55, 0.38],
  [0.68, 0.24],
  [0.8, 0.13],
  [0.9, 0.06],
  [0.96, 0.02],
  [1, 0],
];

const lightRadius = (w: number, h: number, pct: number) =>
  Math.max(w, h) * (Math.max(0, Math.min(100, pct)) / 100);

function supportsBackdrop(): boolean {
  if (typeof window === "undefined" || typeof CSS === "undefined" || !CSS.supports)
    return true;
  return (
    CSS.supports("backdrop-filter", "blur(2px)") ||
    CSS.supports("-webkit-backdrop-filter", "blur(2px)")
  );
}

type RGBA = { r: number; g: number; b: number; a: number };
const WHITE: RGBA = { r: 255, g: 255, b: 255, a: 1 };

function parseColor(input?: string): RGBA {
  if (!input) return WHITE;
  let c = String(input).trim();

  const token = c.match(/^var\([^,]+,\s*(.+)\)$/i);
  if (token) c = token[1].trim();

  if (c[0] === "#") {
    let h = c.slice(1);
    if (h.length === 3 || h.length === 4)
      h = h
        .split("")
        .map((ch) => ch + ch)
        .join("");
    if (h.length !== 6 && h.length !== 8) return WHITE;
    const n = parseInt(h, 16);
    if (Number.isNaN(n)) return WHITE;
    return h.length === 6
      ? { r: (n >> 16) & 255, g: (n >> 8) & 255, b: n & 255, a: 1 }
      : {
          r: (n >>> 24) & 255,
          g: (n >>> 16) & 255,
          b: (n >>> 8) & 255,
          a: (n & 255) / 255,
        };
  }

  const fn = c.match(/rgba?\(([^)]+)\)/i);
  if (fn) {
    const p = fn[1]
      .split(/[,\s/]+/)
      .filter(Boolean)
      .map(Number);
    if (p.length >= 3 && p.slice(0, 3).every((v) => !Number.isNaN(v)))
      return {
        r: p[0],
        g: p[1],
        b: p[2],
        a: p.length > 3 && !Number.isNaN(p[3]) ? p[3] : 1,
      };
  }
  return WHITE;
}

const rgba = (c: RGBA, a: number) =>
  `rgba(${Math.round(c.r)}, ${Math.round(c.g)}, ${Math.round(c.b)}, ${Math.max(0, Math.min(1, a))})`;

const clamp01 = (v: number) => (v < 0 ? 0 : v > 1 ? 1 : v);

const RING_MASK: React.CSSProperties = {
  maskImage: "linear-gradient(#000 0 0), linear-gradient(#000 0 0)",
  maskClip: "border-box, content-box",
  maskComposite: "exclude",
  WebkitMaskImage: "linear-gradient(#000 0 0), linear-gradient(#000 0 0)",
  WebkitMaskClip: "border-box, content-box",
  WebkitMaskComposite: "xor",
} as React.CSSProperties;

export const Navbar: React.FC = () => {
  const [isScrolled, setIsScrolled] = useState(false);
  const [isSearchOpen, setIsSearchOpen] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      const top = window.scrollY || document.documentElement.scrollTop || 0;
      setIsScrolled(top > 10);
    };
    handleScroll();
    window.addEventListener("scroll", handleScroll, { passive: true });
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  // Glass tracking state and refs
  const scope = useRef<HTMLElement>(null);
  const glassRef = useRef<HTMLElement>(null);
  const lightRef = useRef<HTMLSpanElement>(null);
  const strokeRef = useRef<HTMLSpanElement>(null);

  const [glassy, setGlassy] = useState(true);
  useEffect(() => setGlassy(supportsBackdrop()), []);

  const smoothness = 65;
  const lightIntensity = 100;
  const lightSize = 35;

  const tgt = useRef({ x: 0.5, y: 0.5, on: 0 });
  const cur = useRef({ x: 0.5, y: 0.5, on: 0 });
  const raf = useRef<number | null>(null);
  const last = useRef(0);
  const live = useRef({ smoothness, lightIntensity, lightSize });
  live.current = { smoothness, lightIntensity, lightSize };
  const box = useRef({ w: 0, h: 0 });

  useEffect(() => {
    const stop = () => {
      if (raf.current != null) cancelAnimationFrame(raf.current);
      raf.current = null;
    };
    return stop;
  }, []);

  useEffect(() => {
    const el = glassRef.current;
    const root = scope.current;
    if (!el || !root) return;
    const write = () => {
      const r = el.getBoundingClientRect();
      box.current = { w: r.width, h: r.height };
      const R = lightRadius(r.width, r.height, live.current.lightSize);
      root.style.setProperty("--lr", `${R.toFixed(1)}px`);
    };
    write();
    if (typeof ResizeObserver === "undefined") return;
    const ro = new ResizeObserver(write);
    ro.observe(el);
    return () => ro.disconnect();
  }, [lightSize]);

  const paint = () => {
    const root = scope.current;
    const c = cur.current;
    if (root) {
      root.style.setProperty("--mx", `${(c.x * 100).toFixed(2)}%`);
      root.style.setProperty("--my", `${(c.y * 100).toFixed(2)}%`);
    }
    const amt = Math.max(0, Math.min(100, live.current.lightIntensity)) / 100;
    if (lightRef.current)
      lightRef.current.style.opacity = (c.on * amt).toFixed(3);

    const el = strokeRef.current;
    if (el) {
      const w = box.current.w;
      const h = box.current.h;

      const d = clamp01(
        Math.max(Math.abs(c.x - 0.5), Math.abs(c.y - 0.5)) * 2
      );

      let ang = 0;
      let half = 30;
      if (w > 0 && h > 0) {
        const px = c.x * w;
        const py = c.y * h;
        const s = Math.max(1, Math.min(w, h) * AIM_BLEND);
        const sides: Array<[number, number, number]> = [
          [px, 0, py],
          [w - px, w, py],
          [py, px, 0],
          [h - py, px, h],
        ];
        const near = Math.min(...sides.map((v) => v[0]));
        let wt = 0;
        let ax = 0;
        let ay = 0;
        for (const [dist, sx, sy] of sides) {
          const k = Math.exp(-(dist - near) / s);
          wt += k;
          ax += k * sx;
          ay += k * sy;
        }
        const ex = ax / wt - w / 2;
        const ey = ay / wt - h / 2;

        ang = (Math.atan2(ey, ex) * 180) / Math.PI + 90;

        const L = Math.max(1, Math.hypot(ex, ey));
        const reach =
          lightRadius(w, h, live.current.lightSize) * LIGHT_FADE;
        half = (Math.atan(reach / L) * 180) / Math.PI;
      }

      el.style.setProperty("--la", ang.toFixed(1));
      el.style.setProperty(
        "--lw",
        Math.max(3, Math.min(70, half)).toFixed(1)
      );
      el.style.opacity = clamp01(c.on * d * d * amt).toFixed(3);
    }
  };

  const tick = (t: number) => {
    const c = cur.current;
    const g = tgt.current;

    const dt = last.current
      ? Math.min(0.05, (t - last.current) / 1000)
      : 1 / 60;
    last.current = t;
    const s = Math.max(0, Math.min(100, live.current.smoothness)) / 100;
    const per = 0.5 - s * 0.46;
    const k = 1 - Math.pow(1 - per, dt * 60);

    c.x += (g.x - c.x) * k;
    c.y += (g.y - c.y) * k;
    c.on += (g.on - c.on) * k;
    paint();

    const settled =
      Math.abs(g.x - c.x) < 0.001 &&
      Math.abs(g.y - c.y) < 0.001 &&
      Math.abs(g.on - c.on) < 0.002;
    if (settled && g.on === 0) {
      c.x = g.x;
      c.y = g.y;
      c.on = 0;
      paint();
      raf.current = null;
      last.current = 0;
      return;
    }
    raf.current = requestAnimationFrame(tick);
  };

  const kick = () => {
    if (raf.current == null) {
      last.current = 0;
      raf.current = requestAnimationFrame(tick);
    }
  };

  const trackPointer = (e: React.PointerEvent) => {
    const el = glassRef.current;
    if (!el) return;
    const r = el.getBoundingClientRect();
    if (!r.width || !r.height) return;
    tgt.current.x = (e.clientX - r.left) / r.width;
    tgt.current.y = (e.clientY - r.top) / r.height;
    kick();
  };

  const onEnter = (e: React.PointerEvent) => {
    const el = glassRef.current;
    if (el) {
      const r = el.getBoundingClientRect();
      if (r.width && r.height) {
        const x = (e.clientX - r.left) / r.width;
        const y = (e.clientY - r.top) / r.height;
        tgt.current.x = x;
        tgt.current.y = y;
        if (cur.current.on === 0) {
          cur.current.x = x;
          cur.current.y = y;
        }
      }
    }
    tgt.current.on = 1;
    kick();
  };

  const onLeave = (e: React.PointerEvent) => {
    trackPointer(e);
    tgt.current.on = 0;
    kick();
  };

  // Glass backdrop & gradients
  const backdrop = glassy
    ? `blur(${BLUR}px) saturate(180%) brightness(108%)`
    : "none";

  const lightRGB = parseColor("rgba(255, 255, 255, 0.45)");
  const lightClear = rgba(lightRGB, 0);
  const softStops = (peak: number) =>
    LIGHT_FALLOFF.map(
      ([at, k]) => `${rgba(lightRGB, peak * k)} ${Math.round(at * 100)}%`
    ).join(", ");
  const lightGradient = [
    `radial-gradient(circle var(--lr, 0px) at var(--mx) var(--my), ${softStops(lightRGB.a)})`,
    `radial-gradient(circle calc(var(--lr, 0px) * 1.9) at var(--mx) var(--my), ${softStops(lightRGB.a * 0.34)})`,
  ].join(", ");

  const strokePx = 1;
  const lightOpaque = rgba(lightRGB, 1);
  const strokeLightGradient = `conic-gradient(from calc((var(--la, 0) - var(--lw, 30)) * 1deg), ${lightClear} 0deg, ${lightOpaque} calc(var(--lw, 30) * 1deg), ${lightClear} calc(var(--lw, 30) * 2deg))`;

  return (
    <>
      <header
        ref={(el) => {
          (scope as any).current = el;
          (glassRef as any).current = el;
        }}
        onPointerMove={trackPointer}
        onPointerEnter={onEnter}
        onPointerLeave={onLeave}
        style={{
          position: "sticky",
          top: 0,
          zIndex: 50,
          width: "100%",
          boxSizing: "border-box",
          background: isScrolled ? "rgba(10, 10, 11, 0.75)" : "transparent",
          backdropFilter: isScrolled && glassy ? backdrop : "none",
          WebkitBackdropFilter: isScrolled && glassy ? backdrop : "none",
          borderBottom: isScrolled
            ? "1px solid rgba(39, 39, 42, 0.7)"
            : "1px solid transparent",
          boxShadow: isScrolled
            ? "0 8px 32px rgba(0, 0, 0, 0.5)"
            : "none",
          ["--mx" as any]: "50%",
          ["--my" as any]: "50%",
        }}
        className="sticky top-0 z-50 w-full transition-all duration-300 select-none"
      >
        {/* Dynamic Light Spotlight */}
        <span
          ref={lightRef}
          aria-hidden
          style={{
            position: "absolute",
            inset: 0,
            zIndex: 1,
            opacity: 0,
            pointerEvents: "none",
            background: lightGradient,
            mixBlendMode: "screen",
            display: isScrolled ? "block" : "none",
          }}
        />

        {/* Dynamic Edge Stroke Highlight */}
        {strokePx > 0 && (
          <span
            ref={strokeRef}
            aria-hidden
            style={{
              position: "absolute",
              inset: -strokePx,
              padding: strokePx,
              background: strokeLightGradient,
              opacity: 0,
              mixBlendMode: "screen",
              pointerEvents: "none",
              zIndex: 2,
              ["--la" as any]: "0",
              ["--lw" as any]: "30",
              display: isScrolled ? "block" : "none",
              ...RING_MASK,
            }}
          />
        )}

        <div className="container max-w-7xl mx-auto px-3 sm:px-6 lg:px-8 h-16 flex items-center justify-between gap-2 sm:gap-4 relative z-10">
          {/* Logo & Brand Title */}
          <Link
            href="/"
            className="flex items-center gap-2 sm:gap-2.5 group shrink-0"
          >
            <span className="w-8 h-8 rounded-xl bg-[#10B981] flex items-center justify-center text-black font-black text-sm shadow-[0_0_16px_rgba(16,185,129,0.35)] group-hover:scale-105 transition-transform shrink-0">
              ⚡
            </span>
            <div
              className={cn(
                "flex flex-col overflow-hidden origin-left md:transition-none md:max-w-[200px] md:opacity-100 md:ml-0",
                isScrolled || isSearchOpen
                  ? "max-md:max-w-0 max-md:opacity-0 max-md:pointer-events-none max-md:-ml-2.5 max-w-[200px] opacity-100 transition-[max-width,opacity,margin] duration-300 ease-out"
                  : "max-w-[200px] opacity-100 transition-[max-width,opacity,margin] duration-300 ease-out"
              )}
            >
              <span className="text-sm sm:text-base font-black tracking-tight text-white leading-none whitespace-nowrap">
                Protein Engine
              </span>
              <span className="text-[9px] font-mono tracking-widest text-[#34D399] uppercase mt-0.5 whitespace-nowrap">
                Independent Platform
              </span>
            </div>
          </Link>

          {/* Search Bar (Fixed on desktop, dynamic expand on mobile) */}
          <NavbarSearch
            isScrolled={isScrolled}
            isSearchOpen={isSearchOpen}
            onSearchOpenChange={setIsSearchOpen}
            className={cn(
              "md:flex-1 md:max-w-xl md:mx-4 md:ml-0 md:transition-none",
              isScrolled || isSearchOpen
                ? "flex-1 max-w-xl mx-1 sm:mx-4 transition-[flex,margin,width,max-width] duration-300 ease-out"
                : "ml-auto transition-[flex,margin,width,max-width] duration-300 ease-out"
            )}
          />

          {/* User Actions: Login & Shortlist Cart */}
          <div className="flex items-center gap-2 sm:gap-3 shrink-0">
            <LoginButton />
            <CartButton />
          </div>
        </div>
      </header>
    </>
  );
};
