/**
 * Motion design tokens, shared by GSAP scenes. CSS-side equivalents live in
 * base.css (--ease-*, --dur-*). Keep both in sync when tuning the feel.
 *
 * Direction: calm and confident — long, soft decelerations, no bounce on
 * anything that carries medical information.
 */
export const DURATION = {
  fast: 0.25,
  base: 0.6,
  slow: 1.1,
  cinematic: 1.6,
} as const;

export const EASE = {
  /** Default entrance: fast start, long soft landing. */
  out: "expo.out",
  /** Gentle deceleration for small UI feedback. */
  soft: "power2.out",
  /** Symmetric movement (curtains, page transitions). */
  inOut: "power3.inOut",
  /** Scroll-linked (scrub) animations must stay linear to track the finger. */
  scrub: "none",
} as const;

export const STAGGER = {
  words: 0.045,
  items: 0.08,
  cards: 0.1,
} as const;

/** Vertical travel (px) for entrance animations. */
export const DISTANCE = {
  small: 16,
  base: 32,
  large: 64,
} as const;

/** Height (px) of the fixed chrome (nav 68 + jobs ticker 30) for scroll offsets. */
export const HEADER_OFFSET = 98;
