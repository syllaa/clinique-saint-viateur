import type { Directive } from "vue";

import { isReducedMotion } from "@/motion/motionPreferences";

/**
 * v-tilt: the card leans towards the cursor in 3D and a soft light follows
 * it. Only exposes CSS variables (--tilt-x, --tilt-y, --glare-x, --glare-y,
 * --tilt-active); the component's CSS decides how to use them.
 *
 * Desktop (fine pointer) only; no-op under reduced motion. Updates are
 * batched in requestAnimationFrame.
 */
type TiltEl = HTMLElement & { __tiltCleanup?: () => void };

const MAX_DEG = 6;

export const vTilt: Directive<TiltEl, number | undefined> = {
  mounted(el, binding) {
    if (!window.matchMedia?.("(hover: hover) and (pointer: fine)").matches) return;
    const max = binding.value ?? MAX_DEG;
    let frame = 0;

    const onMove = (e: PointerEvent) => {
      if (isReducedMotion()) return;
      cancelAnimationFrame(frame);
      frame = requestAnimationFrame(() => {
        const r = el.getBoundingClientRect();
        const px = (e.clientX - r.left) / r.width;
        const py = (e.clientY - r.top) / r.height;
        el.style.setProperty("--tilt-x", `${((0.5 - py) * max * 2).toFixed(2)}deg`);
        el.style.setProperty("--tilt-y", `${((px - 0.5) * max * 2).toFixed(2)}deg`);
        el.style.setProperty("--glare-x", `${(px * 100).toFixed(1)}%`);
        el.style.setProperty("--glare-y", `${(py * 100).toFixed(1)}%`);
        el.style.setProperty("--tilt-active", "1");
      });
    };
    const onLeave = () => {
      cancelAnimationFrame(frame);
      el.style.setProperty("--tilt-x", "0deg");
      el.style.setProperty("--tilt-y", "0deg");
      el.style.setProperty("--tilt-active", "0");
    };

    el.addEventListener("pointermove", onMove);
    el.addEventListener("pointerleave", onLeave);
    el.__tiltCleanup = () => {
      cancelAnimationFrame(frame);
      el.removeEventListener("pointermove", onMove);
      el.removeEventListener("pointerleave", onLeave);
    };
  },
  unmounted(el) {
    el.__tiltCleanup?.();
  },
};
