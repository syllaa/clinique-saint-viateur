import type { gsap as GsapCore } from "gsap";
import type { Flip as FlipPlugin } from "gsap/Flip";
import type { ScrollTrigger as ScrollTriggerPlugin } from "gsap/ScrollTrigger";
import type { SplitText as SplitTextPlugin } from "gsap/SplitText";

import { linkLenisToScrollTrigger, motionBridge } from "@/motion/bridge";

export interface GsapKit {
  gsap: typeof GsapCore;
  ScrollTrigger: typeof ScrollTriggerPlugin;
  Flip: typeof FlipPlugin;
  SplitText: typeof SplitTextPlugin;
}

let kit: Promise<GsapKit> | null = null;

/**
 * Loads GSAP and its plugins on first use only. Pages without scroll scenes
 * (and the whole admin) never download it.
 */
export function loadGsap(): Promise<GsapKit> {
  kit ??= Promise.all([
    import("gsap"),
    import("gsap/ScrollTrigger"),
    import("gsap/Flip"),
    import("gsap/SplitText"),
  ]).then(([core, st, flip, split]) => {
    const { gsap } = core;
    gsap.registerPlugin(st.ScrollTrigger, flip.Flip, split.SplitText);
    // Mobile address-bar show/hide must not re-trigger pinned layouts.
    st.ScrollTrigger.config({ ignoreMobileResize: true });

    motionBridge.scrollTriggerUpdate = () => st.ScrollTrigger.update();
    linkLenisToScrollTrigger();

    return { gsap, ScrollTrigger: st.ScrollTrigger, Flip: flip.Flip, SplitText: split.SplitText };
  });
  return kit;
}
