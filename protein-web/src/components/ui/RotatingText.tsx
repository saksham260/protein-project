// Text Carousel — Originkit
"use client";

import * as React from "react";
import { useEffect, useLayoutEffect, useMemo, useRef, useState } from "react";
import { gsap } from "gsap";

const useIsomorphicLayoutEffect =
  typeof window !== "undefined" ? useLayoutEffect : useEffect;

export type FontStyle = React.CSSProperties;

export type TransitionValue = {
  type?: string;
  duration?: number;
  delay?: number;
  ease?: string | number[];
  staggerChildren?: number;
};

export type StaggerFrom = "first" | "last" | "center" | "random";
export type SplitBy = "characters" | "words" | "lines";

export type WordPart = {
  characters: string[];
  needsSpace: boolean;
};

export type RotatingTextProps = {
  prefix?: string;
  texts?: string[];
  font?: FontStyle;
  color?: string;
  prefixColor?: string;
  badgeBackground?: string;
  badgeShadow?: string;
  badgePaddingX?: number;
  badgePaddingY?: number;
  badgeRadius?: number;
  gap?: number;

  splitBy?: SplitBy;
  staggerFrom?: StaggerFrom;

  auto?: boolean;

  transition?: TransitionValue;
  className?: string;
};

const ROTATION_INTERVAL_MS = 2000;

const mapEase = (ease: TransitionValue["ease"]): string => {
  if (typeof ease !== "string") return "power2.out";

  const easeMap: Record<string, string> = {
    linear: "none",
    easeIn: "power2.in",
    easeOut: "power2.out",
    easeInOut: "power2.inOut",
    circIn: "circ.in",
    circOut: "circ.out",
    circInOut: "circ.inOut",
    backIn: "back.in",
    backOut: "back.out(1.7)",
    backInOut: "back.inOut",
    anticipate: "back.out(1.7)",
  };

  return easeMap[ease] ?? ease;
};

const mapStaggerFrom = (
  staggerFrom: StaggerFrom
): "start" | "end" | "center" | "random" => {
  if (staggerFrom === "first") return "start";
  if (staggerFrom === "last") return "end";
  return staggerFrom;
};

const splitIntoCharacters = (text: string): string[] => {
  if (typeof Intl !== "undefined" && "Segmenter" in Intl) {
    const segmenter = new Intl.Segmenter("en", { granularity: "grapheme" });
    return Array.from(segmenter.segment(text), (part) => part.segment);
  }
  return Array.from(text);
};

const buildElements = (text: string, splitBy: SplitBy): WordPart[] => {
  if (splitBy === "characters") {
    const words = text.split(" ");
    return words.map((word, i) => ({
      characters: splitIntoCharacters(word),
      needsSpace: i !== words.length - 1,
    }));
  }

  if (splitBy === "words") {
    return text.split(" ").map((word, i, arr) => ({
      characters: [word],
      needsSpace: i !== arr.length - 1,
    }));
  }

  return text.split("\n").map((line, i, arr) => ({
    characters: [line],
    needsSpace: i !== arr.length - 1,
  }));
};

const DEFAULT_TEXTS = ["Products", "Powders", "Chips", "Drinks", "Bars", "Snacks"];
const DEFAULT_TRANSITION: TransitionValue = {
  type: "tween",
  duration: 0.45,
  delay: 0,
  ease: "easeOut",
  staggerChildren: 0.03,
};

export function RotatingText({
  prefix = "Protein",
  texts = DEFAULT_TEXTS,
  font = {
    fontFamily: "var(--font-inter), system-ui, -apple-system, sans-serif",
    fontSize: "clamp(2rem, 5.5vw, 4.5rem)",
    fontWeight: 900,
    letterSpacing: "-0.03em",
    lineHeight: "1.15em",
    textAlign: "center",
  },
  color = "#0A0A0B",
  prefixColor = "#FFFFFF",
  badgeBackground = "#D97706",
  badgeShadow = "none",
  badgePaddingX = 20,
  badgePaddingY = 6,
  badgeRadius = 18,
  gap = 14,

  splitBy = "characters",
  staggerFrom = "first",

  auto = true,

  transition = DEFAULT_TRANSITION,
  className = "",
}: RotatingTextProps) {
  const textsKey = (texts && texts.length > 0 ? texts : DEFAULT_TEXTS).join("|");
  const safeTexts = useMemo(
    () => (texts && texts.length > 0 ? texts : DEFAULT_TEXTS),
    [textsKey]
  );
  const [currentTextIndex, setCurrentTextIndex] = useState(0);
  const contentRef = useRef<HTMLSpanElement>(null);
  const badgeRef = useRef<HTMLSpanElement>(null);
  const isAnimating = useRef(false);
  const isFirstRender = useRef(true);
  const hasSizedBadge = useRef(false);

  const transitionRef = useRef(transition ?? DEFAULT_TRANSITION);
  transitionRef.current = transition ?? DEFAULT_TRANSITION;

  const staggerFromRef = useRef(staggerFrom);
  staggerFromRef.current = staggerFrom;

  const safeTextsRef = useRef(safeTexts);
  safeTextsRef.current = safeTexts;

  const currentWord = safeTexts[currentTextIndex] ?? "";
  const elements = useMemo(
    () => buildElements(currentWord, splitBy),
    [currentWord, splitBy]
  );

  useEffect(() => {
    if (currentTextIndex > safeTexts.length - 1) {
      setCurrentTextIndex(0);
    }
  }, [safeTexts.length, currentTextIndex]);

  // Persistent rotation ticker unaffected by external re-renders/scrolling
  useEffect(() => {
    if (!auto) return;

    const intervalId = window.setInterval(() => {
      if (isAnimating.current) return;

      const content = contentRef.current;
      const list = safeTextsRef.current;
      if (!content || list.length <= 1) return;

      const chars = content.querySelectorAll(".char");
      if (chars.length === 0) {
        setCurrentTextIndex((prev) => (prev + 1) % list.length);
        return;
      }

      const t = transitionRef.current;
      const duration = t.duration ?? 0.45;
      const staggerEach = t.staggerChildren ?? 0.03;
      const ease = mapEase(t.ease);

      isAnimating.current = true;
      gsap.killTweensOf(chars);

      gsap.to(chars, {
        yPercent: -120,
        opacity: 0,
        duration,
        stagger: {
          each: staggerEach,
          from: mapStaggerFrom(staggerFromRef.current),
        },
        ease,
        onComplete: () => {
          setCurrentTextIndex((prev) => (prev + 1) % list.length);
        },
      });
    }, ROTATION_INTERVAL_MS);

    return () => window.clearInterval(intervalId);
  }, [auto]);

  // Text entry animation (runs purely on currentTextIndex transition)
  useEffect(() => {
    const content = contentRef.current;
    if (!content) return;

    const chars = content.querySelectorAll(".char");
    if (chars.length === 0) {
      isAnimating.current = false;
      return;
    }

    gsap.killTweensOf(chars);

    const t = transitionRef.current;
    const duration = t.duration ?? 0.45;
    const delay = isFirstRender.current ? (t.delay ?? 0) : 0;
    const staggerEach = t.staggerChildren ?? 0.03;
    const ease = mapEase(t.ease);

    isFirstRender.current = false;
    isAnimating.current = true;

    gsap.fromTo(
      chars,
      { yPercent: 100, opacity: 0 },
      {
        yPercent: 0,
        opacity: 1,
        duration,
        delay,
        stagger: {
          each: staggerEach,
          from: mapStaggerFrom(staggerFromRef.current),
        },
        ease,
        onComplete: () => {
          isAnimating.current = false;
        },
      }
    );
  }, [currentTextIndex]);

  // Badge smooth width adjustment
  useIsomorphicLayoutEffect(() => {
    const badge = badgeRef.current;
    const content = contentRef.current;
    if (!badge || !content) return;

    const nextWidth = Math.ceil(content.scrollWidth + badgePaddingX * 2);
    const t = transitionRef.current;
    const duration = t.duration ?? 0.45;
    const ease = mapEase(t.ease);

    gsap.killTweensOf(badge);

    if (!hasSizedBadge.current) {
      hasSizedBadge.current = true;
      gsap.set(badge, { width: nextWidth });
      return;
    }

    gsap.to(badge, {
      width: nextWidth,
      duration,
      ease,
    });
  }, [currentTextIndex, badgePaddingX]);

  const textAlign =
    (font.textAlign as React.CSSProperties["textAlign"]) ?? "center";
  const justifyContent =
    textAlign === "center"
      ? "center"
      : textAlign === "right" || textAlign === "end"
        ? "flex-end"
        : "flex-start";

  return (
    <span
      className={className}
      style={{
        ...font,
        display: "inline-flex",
        width: prefix ? "100%" : "auto",
        alignItems: "center",
        justifyContent,
        flexWrap: "nowrap",
        gap,
        textAlign,
      }}
    >
      {prefix ? (
        <span style={{ color: prefixColor, whiteSpace: "pre" }}>
          {prefix}
        </span>
      ) : null}

      <span
        ref={badgeRef}
        style={{
          display: "inline-flex",
          alignItems: "center",
          justifyContent: "center",
          overflow: "hidden",
          verticalAlign: "middle",
          backgroundColor: badgeBackground,
          color,
          borderRadius: badgeRadius,
          paddingTop: badgePaddingY,
          paddingBottom: badgePaddingY,
          paddingLeft: badgePaddingX,
          paddingRight: badgePaddingX,
          boxSizing: "border-box",
          boxShadow: badgeShadow || "none",
        }}
      >
        <span
          style={{
            position: "absolute",
            width: 1,
            height: 1,
            padding: 0,
            margin: -1,
            overflow: "hidden",
            clip: "rect(0, 0, 0, 0)",
            whiteSpace: "nowrap",
            borderWidth: 0,
          }}
        >
          {prefix ? `${prefix} ` : ""}
          {safeTexts[currentTextIndex]}
        </span>

        <span
          ref={contentRef}
          aria-hidden="true"
          style={{
            display: "inline-flex",
            alignItems: "center",
            flexWrap: splitBy === "lines" ? "nowrap" : "wrap",
            flexDirection: splitBy === "lines" ? "column" : "row",
            whiteSpace: "nowrap",
            position: "relative",
          }}
        >
          {elements.map((wordObj, wordIndex) => (
            <span
              key={`${currentTextIndex}-${wordIndex}`}
              style={{ display: "inline-flex" }}
            >
              {wordObj.characters.map((char, charIndex) => (
                <span
                  key={`${currentTextIndex}-${wordIndex}-${charIndex}`}
                  className="char"
                  style={{
                    display: "inline-block",
                    willChange: "transform, opacity",
                  }}
                >
                  {char === " " ? "\u00A0" : char}
                </span>
              ))}
              {wordObj.needsSpace ? (
                <span style={{ whiteSpace: "pre" }}> </span>
              ) : null}
            </span>
          ))}
        </span>
      </span>
    </span>
  );
}

export default RotatingText;
