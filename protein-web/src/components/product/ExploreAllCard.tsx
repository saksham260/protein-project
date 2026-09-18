"use client";

import React, { useRef, useLayoutEffect, useEffect } from "react";
import Link from "next/link";
import { useAnimate, useReducedMotion, type Transition } from "motion/react";
import { cn } from "@/lib/utils";

export interface ExploreAllCardProps {
  href: string;
  variant?: "emerald" | "dark";
  className?: string;
  // Legacy props accepted to prevent breakages, but no extra text is rendered
  title?: string;
  subtitle?: string;
  icon?: string;
  imageUrl?: string;
  badgeLabel?: string;
  totalCount?: number;
}

const useIsoLayoutEffect =
  typeof window !== "undefined" ? useLayoutEffect : useEffect;

export const ExploreAllCard: React.FC<ExploreAllCardProps> = ({
  href,
  variant = "emerald",
  className,
}) => {
  const [scope, animate] = useAnimate();
  const cardRef = useRef<HTMLAnchorElement>(null);
  const badgeRef = useRef<HTMLDivElement>(null);
  const arrowRef = useRef<HTMLDivElement>(null);
  const textRef = useRef<HTMLSpanElement>(null);
  const slotRef = useRef<HTMLDivElement>(null);
  const hovered = useRef(false);
  const metrics = useRef({ hoverScale: 1 });
  const reducedMotion = useReducedMotion();

  const isEmerald = variant === "emerald";

  // Emerald variant: starts vibrant emerald #10B981, expands black #0A0A0B circle on hover
  // Dark variant: starts #18181B dark, expands emerald #10B981 circle on hover
  const baseBg = isEmerald ? "#10B981" : "#18181B";
  const badgeBg = isEmerald ? "#0A0A0B" : "#10B981";
  const restTextColor = isEmerald ? "#0A0A0B" : "#FFFFFF";
  const hoverTextColor = isEmerald ? "#FFFFFF" : "#0A0A0B";
  const restArrowColor = isEmerald ? "#10B981" : "#0A0A0B";
  const hoverArrowColor = isEmerald ? "#10B981" : "#0A0A0B";
  const baseBorder = isEmerald ? "rgba(16, 185, 129, 0.4)" : "#27272A";
  const hoverBorder = "#10B981";

  const transition: Transition = {
    ease: [0.44, 0, 0.56, 1],
    type: "tween",
    delay: 0,
    duration: 0.46,
  };

  const opts = () => (reducedMotion ? { duration: 0 } : transition);

  useIsoLayoutEffect(() => {
    const card = cardRef.current;
    const badge = badgeRef.current;
    const arrow = arrowRef.current;
    const slot = slotRef.current;
    if (!card || !badge || !arrow || !slot) return;

    const measure = () => {
      const w = card.offsetWidth;
      const h = card.offsetHeight;
      if (!w || !h) return;

      const badgeSize = slot.offsetWidth || 48;
      const rb = badgeSize / 2;

      const cx = slot.offsetLeft + slot.offsetWidth / 2;
      const cy = slot.offsetTop + slot.offsetHeight / 2;

      // Distance to furthest corner
      const far = Math.hypot(Math.max(cx, w - cx), Math.max(cy, h - cy));
      const coverD = Math.ceil(2 * far * 1.05);

      metrics.current = {
        hoverScale: badgeSize > 0 ? coverD / badgeSize : 1,
      };

      badge.style.width = `${badgeSize}px`;
      badge.style.height = `${badgeSize}px`;
      badge.style.left = `${cx}px`;
      badge.style.top = `${cy}px`;
      badge.style.marginLeft = `${-rb}px`;
      badge.style.marginTop = `${-rb}px`;

      arrow.style.width = `${badgeSize}px`;
      arrow.style.height = `${badgeSize}px`;
      arrow.style.left = `${cx}px`;
      arrow.style.top = `${cy}px`;
      arrow.style.marginLeft = `${-rb}px`;
      arrow.style.marginTop = `${-rb}px`;

      if (!hovered.current) {
        animate(badge, { scale: 1 }, { duration: 0 });
        animate(arrow, { rotate: 0, x: 0, y: 0 }, { duration: 0 });
      }
    };

    measure();

    const ro = new ResizeObserver(measure);
    ro.observe(card);
    ro.observe(slot);
    return () => ro.disconnect();
  }, [animate]);

  const pressTo = (s: number) => {
    if (cardRef.current) {
      animate(
        cardRef.current,
        { scale: s } as any,
        { duration: 0.14, ease: [0.25, 1, 0.5, 1] } as any
      );
    }
  };

  const onEnter = () => {
    hovered.current = true;
    if (badgeRef.current) {
      animate(
        badgeRef.current,
        { scale: metrics.current.hoverScale } as any,
        opts() as any
      );
    }
    if (arrowRef.current) {
      animate(
        arrowRef.current,
        { rotate: 45, x: 2, y: -2 } as any,
        opts() as any
      );
    }
    if (textRef.current) {
      animate(
        textRef.current,
        { color: hoverTextColor, x: 3 } as any,
        opts() as any
      );
    }
    if (cardRef.current) {
      animate(
        cardRef.current,
        { borderColor: hoverBorder } as any,
        opts() as any
      );
    }
  };

  const onLeave = () => {
    hovered.current = false;
    if (badgeRef.current) {
      animate(badgeRef.current, { scale: 1 } as any, opts() as any);
    }
    if (arrowRef.current) {
      animate(arrowRef.current, { rotate: 0, x: 0, y: 0 } as any, opts() as any);
    }
    if (textRef.current) {
      animate(textRef.current, { color: restTextColor, x: 0 } as any, opts() as any);
    }
    if (cardRef.current) {
      animate(
        cardRef.current,
        { borderColor: baseBorder } as any,
        opts() as any
      );
    }
    pressTo(1);
  };

  return (
    <div ref={scope} className={cn("h-full w-full", className)}>
      <Link
        ref={cardRef}
        href={href}
        onPointerEnter={onEnter}
        onPointerLeave={onLeave}
        onPointerDown={() => pressTo(0.97)}
        onPointerUp={() => pressTo(1)}
        onTouchStart={onEnter}
        onTouchEnd={onLeave}
        style={{
          backgroundColor: baseBg,
          borderColor: baseBorder,
        }}
        className={cn(
          "group flex flex-col justify-between h-full min-h-[250px] sm:min-h-[320px] rounded-2xl overflow-hidden relative select-none cursor-pointer border p-4 sm:p-7 shadow-[0_4px_20px_rgba(0,0,0,0.4)] transition-shadow duration-300 hover:shadow-[0_20px_50px_rgba(16,185,129,0.25)] touch-manipulation"
        )}
      >
        {/* Top: Circular Arrow Slot & Indicator */}
        <div className="flex items-center justify-between w-full">
          <div
            ref={slotRef}
            aria-hidden
            className="w-10 h-10 sm:w-14 sm:h-14 rounded-full flex items-center justify-center shrink-0"
          />
        </div>

        {/* The Expanding Circular Fill Badge (Scales up to cover the entire card on hover/click) */}
        <div
          ref={badgeRef}
          aria-hidden
          style={{
            position: "absolute",
            zIndex: 1,
            width: 0,
            height: 0,
            borderRadius: "50%",
            backgroundColor: badgeBg,
            transformOrigin: "center",
            pointerEvents: "none",
          }}
        />

        {/* The Arrow Glyph (Transforms & Rotates on hover) */}
        <div
          ref={arrowRef}
          aria-hidden
          style={{
            position: "absolute",
            zIndex: 3,
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            pointerEvents: "none",
            color: restArrowColor,
          }}
        >
          <svg
            className="w-5 h-5 sm:w-6 sm:h-6"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="3"
            strokeLinecap="round"
            strokeLinejoin="round"
          >
            <path d="M5 12h14M12 5l7 7-7 7" />
          </svg>
        </div>

        {/* Center: "Explore All" text centered in the card */}
        <div className="absolute inset-0 flex items-center justify-center pointer-events-none z-10 p-4 sm:p-7 text-center">
          <span
            ref={textRef}
            style={{
              color: restTextColor,
            }}
            className="text-xl sm:text-3xl font-black tracking-tight leading-tight select-none inline-block text-center"
          >
            Explore All
          </span>
        </div>
      </Link>
    </div>
  );
};

export default ExploreAllCard;
