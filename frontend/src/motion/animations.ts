/**
 * Reusable GSAP presets. Call them from inside a `useScrollScene` setup
 * function, so they are recorded in its gsap.context and cleaned up
 * automatically. Each preset leaves the element readable if GSAP never runs.
 */
import type { GsapKit } from "@/motion/gsap";
import { DISTANCE, DURATION, EASE, STAGGER } from "@/motion/tokens";

type Targets = string | Element | Element[] | NodeListOf<Element>;

const finePointer = () =>
  typeof window !== "undefined" && window.matchMedia?.("(hover: hover) and (pointer: fine)").matches;

/** Moves an element slower/faster than the page while it crosses the viewport. */
export function parallax({ gsap }: GsapKit, el: Element, speed = 0.15): void {
  gsap.fromTo(
    el,
    { yPercent: -speed * 50 },
    {
      yPercent: speed * 50,
      ease: EASE.scrub,
      scrollTrigger: { trigger: el.parentElement ?? el, start: "top bottom", end: "bottom top", scrub: true },
    },
  );
}

/** Slow zoom-out of an image as its frame scrolls into view ("Ken Burns" on scroll). */
export function scrollZoom({ gsap }: GsapKit, img: Element, from = 1.18): void {
  gsap.fromTo(
    img,
    { scale: from },
    {
      scale: 1,
      ease: EASE.scrub,
      scrollTrigger: { trigger: img.parentElement ?? img, start: "top bottom", end: "bottom center", scrub: true },
    },
  );
}

/** Fades + lifts a group of elements in sequence when the first one enters the viewport. */
export function staggerIn({ gsap }: GsapKit, targets: Targets, opts: { y?: number; stagger?: number; start?: string } = {}): void {
  const list = gsap.utils.toArray<Element>(targets);
  if (!list.length) return;
  gsap.from(list, {
    autoAlpha: 0,
    y: opts.y ?? DISTANCE.base,
    duration: DURATION.slow,
    ease: EASE.out,
    stagger: opts.stagger ?? STAGGER.cards,
    scrollTrigger: { trigger: list[0], start: opts.start ?? "top 85%", once: true },
  });
}

/**
 * Reveals a heading line by line from behind a mask. Lines are recomputed on
 * resize (autoSplit), so wrapping stays correct on every screen width.
 */
export function revealLines({ gsap, SplitText }: GsapKit, el: Element, opts: { delay?: number; scroll?: boolean } = {}): void {
  SplitText.create(el, {
    type: "lines",
    mask: "lines",
    autoSplit: true,
    onSplit(self) {
      return gsap.from(self.lines, {
        yPercent: 110,
        duration: DURATION.slow,
        ease: EASE.out,
        stagger: 0.12,
        delay: opts.delay ?? 0,
        ...(opts.scroll ? { scrollTrigger: { trigger: el, start: "top 85%", once: true } } : {}),
      });
    },
  });
}

/** "Draws" an SVG stroke: on load, or tied to scroll progress when `scrub` is set. */
export function drawPath(
  { gsap }: GsapKit,
  path: SVGGeometryElement,
  opts: { duration?: number; delay?: number; scrub?: boolean | number; trigger?: Element; start?: string; end?: string } = {},
): void {
  // Tweens a plain value and writes the style itself: GSAP's CSS plugin can
  // drop stroke-dashoffset on SVG paths (notably with pathLength).
  const length = path.hasAttribute("pathLength") ? Number(path.getAttribute("pathLength")) : path.getTotalLength();
  const draw = { offset: length };
  path.style.strokeDasharray = String(length);
  path.style.strokeDashoffset = String(length);
  gsap.to(draw, {
    offset: 0,
    onUpdate: () => {
      path.style.strokeDashoffset = draw.offset.toFixed(3);
    },
    ease: opts.scrub ? EASE.scrub : EASE.inOut,
    duration: opts.duration ?? DURATION.cinematic,
    delay: opts.delay ?? 0,
    ...(opts.scrub || opts.trigger
      ? {
          scrollTrigger: {
            trigger: opts.trigger ?? path,
            start: opts.start ?? "top 80%",
            end: opts.end ?? "bottom 20%",
            scrub: opts.scrub ?? false,
            once: !opts.scrub,
          },
        }
      : {}),
  });
}

/**
 * Element gently follows the cursor while hovered (desktop only). Returns a
 * cleanup function for the listeners — return it from the scene setup.
 */
export function magnetic({ gsap }: GsapKit, el: HTMLElement, strength = 0.25): () => void {
  if (!finePointer()) return () => undefined;
  // CSS transitions on transform would fight GSAP's per-frame updates.
  el.classList.add("is-magnetic");
  const xTo = gsap.quickTo(el, "x", { duration: 0.6, ease: "elastic.out(1, 0.5)" });
  const yTo = gsap.quickTo(el, "y", { duration: 0.6, ease: "elastic.out(1, 0.5)" });
  const onMove = (e: PointerEvent) => {
    const r = el.getBoundingClientRect();
    xTo((e.clientX - (r.left + r.width / 2)) * strength);
    yTo((e.clientY - (r.top + r.height / 2)) * strength);
  };
  const onLeave = () => {
    xTo(0);
    yTo(0);
  };
  el.addEventListener("pointermove", onMove);
  el.addEventListener("pointerleave", onLeave);
  return () => {
    el.removeEventListener("pointermove", onMove);
    el.removeEventListener("pointerleave", onLeave);
    el.classList.remove("is-magnetic");
  };
}

/** Counts a number up when it scrolls into view (keeps any suffix such as "K+"). */
export function countTo({ gsap }: GsapKit, el: HTMLElement, target: number, suffix = ""): void {
  const state = { v: 0 };
  el.textContent = `0${suffix}`;
  gsap.to(state, {
    v: target,
    duration: DURATION.cinematic,
    ease: "power2.out",
    scrollTrigger: { trigger: el, start: "top 90%", once: true },
    onUpdate: () => {
      el.textContent = `${Math.round(state.v)}${suffix}`;
    },
  });
}
