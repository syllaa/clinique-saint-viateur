import type Lenis from "lenis";

/**
 * Tiny shared registry between the smooth-scroll engine (Lenis) and GSAP's
 * ScrollTrigger, which load independently and lazily. Whichever arrives
 * second wires itself to the first, so ScrollTrigger always sees Lenis'
 * scroll position.
 */
export const motionBridge: {
  lenis: Lenis | null;
  scrollTriggerUpdate: (() => void) | null;
} = {
  lenis: null,
  scrollTriggerUpdate: null,
};

export function linkLenisToScrollTrigger(): void {
  const { lenis, scrollTriggerUpdate } = motionBridge;
  if (lenis && scrollTriggerUpdate) lenis.on("scroll", scrollTriggerUpdate);
}
