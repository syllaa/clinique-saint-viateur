import "lenis/dist/lenis.css";

import type Lenis from "lenis";

import { linkLenisToScrollTrigger, motionBridge } from "@/motion/bridge";
import { HEADER_OFFSET } from "@/motion/tokens";

/**
 * Smooth (inertial) scrolling for the public site, desktop only in practice:
 * touch devices keep their native scrolling (syncTouch stays off), which is
 * both faster and what mobile users expect.
 *
 * Never started on the admin, nor when reduced motion is on.
 */
let starting: Promise<void> | null = null;

export function getLenis(): Lenis | null {
  return motionBridge.lenis;
}

export function startLenis(): Promise<void> {
  if (motionBridge.lenis) return Promise.resolve();
  starting ??= import("lenis")
    .then(({ default: LenisCtor }) => {
      motionBridge.lenis = new LenisCtor({
        autoRaf: true,
        lerp: 0.1,
        wheelMultiplier: 1,
        // In-page anchors are handled by the router (see scrollToHash).
        anchors: false,
      });
      linkLenisToScrollTrigger();
    })
    .finally(() => {
      starting = null;
    });
  return starting;
}

export function stopLenis(): void {
  motionBridge.lenis?.destroy();
  motionBridge.lenis = null;
}

/** Temporarily freezes smooth scrolling (open menus, modals). */
export function lockScroll(locked: boolean): void {
  if (locked) motionBridge.lenis?.stop();
  else motionBridge.lenis?.start();
}

/**
 * Scrolls to an in-page anchor once it exists (content often arrives after
 * the API responds), offset by the fixed header. Uses Lenis when active.
 */
export function scrollToHash(hash: string, timeoutMs = 2000): void {
  const started = performance.now();
  const tick = () => {
    let el: Element | null = null;
    try {
      el = document.querySelector(hash);
    } catch {
      return; // not a valid selector: ignore
    }
    if (el) {
      const lenis = motionBridge.lenis;
      if (lenis) lenis.scrollTo(el as HTMLElement, { offset: -HEADER_OFFSET });
      else {
        const top = el.getBoundingClientRect().top + window.scrollY - HEADER_OFFSET;
        window.scrollTo({ top, behavior: document.documentElement.dataset.motion === "reduce" ? "auto" : "smooth" });
      }
      return;
    }
    if (performance.now() - started < timeoutMs) requestAnimationFrame(tick);
  };
  requestAnimationFrame(tick);
}

/** Jumps to the top instantly (route changes). */
export function scrollToTop(): void {
  const lenis = motionBridge.lenis;
  if (lenis) lenis.scrollTo(0, { immediate: true, force: true });
  window.scrollTo(0, 0);
}
