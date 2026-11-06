import { onBeforeUnmount, onMounted, watch, type Ref } from "vue";

import { loadGsap, type GsapKit } from "@/motion/gsap";
import { reducedMotion } from "@/motion/motionPreferences";

const isDesktop = () => typeof window !== "undefined" && !!window.matchMedia?.("(min-width: 981px)").matches;

/**
 * Runs a GSAP "scene" scoped to a component's root element.
 *
 * - GSAP is loaded lazily on first use.
 * - Every tween/ScrollTrigger created inside `setup` is recorded in a
 *   gsap.context and reverted automatically on unmount (no leaks between
 *   pages), or as soon as the visitor turns reduced motion on.
 * - Nothing runs under reduced motion: the markup must already be readable
 *   in its final state without the scene.
 * - Desktop only (≥ 981 px): measured on a mid-range phone, loading and
 *   running GSAP/ScrollTrigger cost ~1.5 s of CPU for effects barely
 *   visible on a small screen. Phones keep the lightweight CSS reveals.
 *
 * `setup` may return a cleanup function for non-GSAP side effects
 * (event listeners, observers).
 */
export function useScrollScene(
  root: Ref<HTMLElement | null | undefined>,
  setup: (kit: GsapKit, root: HTMLElement) => void | (() => void),
): void {
  let ctx: ReturnType<GsapKit["gsap"]["context"]> | null = null;
  let cleanup: (() => void) | void;
  let disposed = false;

  async function build() {
    if (ctx || reducedMotion.value || !root.value || !isDesktop()) return;
    const kit = await loadGsap();
    const el = root.value;
    if (disposed || ctx || reducedMotion.value || !el) return;
    ctx = kit.gsap.context(() => {
      cleanup = setup(kit, el);
    }, el);
    // Layout may have changed while GSAP was loading (images, API data).
    kit.ScrollTrigger.refresh();
  }

  function teardown() {
    cleanup?.();
    cleanup = undefined;
    ctx?.revert();
    ctx = null;
  }

  onMounted(build);
  const stopWatch = watch(reducedMotion, (reduced) => (reduced ? teardown() : build()));
  onBeforeUnmount(() => {
    disposed = true;
    stopWatch();
    teardown();
  });
}
