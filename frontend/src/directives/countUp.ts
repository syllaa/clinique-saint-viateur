import type { Directive } from "vue";

export interface CountUpValue {
  target: number;
  suffix?: string;
  duration?: number;
}

function animate(el: HTMLElement, target: number, suffix: string, duration: number) {
  const start = performance.now();
  function tick(now: number) {
    const p = Math.min((now - start) / duration, 1);
    const eased = 1 - Math.pow(1 - p, 3);
    el.textContent = `${Math.round(target * eased)}${suffix}`;
    if (p < 1) requestAnimationFrame(tick);
  }
  requestAnimationFrame(tick);
}

const reducedMotion =
  typeof window !== "undefined" && window.matchMedia?.("(prefers-reduced-motion: reduce)").matches;

const observer =
  typeof IntersectionObserver !== "undefined"
    ? new IntersectionObserver((entries, obs) => {
        entries.forEach((entry) => {
          if (!entry.isIntersecting) return;
          const el = entry.target as HTMLElement & { __countUp?: CountUpValue };
          const data = el.__countUp;
          if (data) animate(el, data.target, data.suffix ?? "", data.duration ?? 1400);
          obs.unobserve(el);
        });
      }, { threshold: 0.4 })
    : null;

/** v-count-up="{ target: 79, suffix: 'K+' }": animates the element's text from 0 to
 * target once it scrolls into view. Skips straight to the final value under
 * prefers-reduced-motion or when IntersectionObserver isn't available. */
export const vCountUp: Directive<HTMLElement & { __countUp?: CountUpValue }, CountUpValue> = {
  mounted(el, binding) {
    if (reducedMotion) {
      el.textContent = `${binding.value.target}${binding.value.suffix ?? ""}`;
      return;
    }
    el.textContent = `0${binding.value.suffix ?? ""}`;
    if (!observer) {
      animate(el, binding.value.target, binding.value.suffix ?? "", binding.value.duration ?? 1400);
      return;
    }
    el.__countUp = binding.value;
    observer.observe(el);
  },
  unmounted(el) {
    observer?.unobserve(el);
  },
};
