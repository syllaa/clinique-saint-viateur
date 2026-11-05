import { createPinia } from "pinia";
import { createApp } from "vue";

import App from "./App.vue";
import "./assets/base.css";
import "./assets/ui.css";
import { vCountUp } from "./directives/countUp";
import { vReveal } from "./directives/reveal";
// Imported for its side effect: sets <html data-motion> before the first render,
// so reveal animations never flash when reduced motion is on.
import { isReducedMotion } from "./motion/motionPreferences";
import router from "./router";

const app = createApp(App);

app.use(createPinia());
app.use(router);
app.directive("reveal", vReveal);
app.directive("count-up", vCountUp);

app.mount("#app");

// Preloader exit. On the first visit of a session to the home page, it plays
// the short brand intro (logo draw + curtain, ~1.9s, CSS in index.html) and
// the hero's own entrance waits for it (--intro-delay). Otherwise it fades.
const preloader = document.getElementById("preloader");
if (preloader) {
  let playIntro = false;
  try {
    // Desktop only: on phones (slower CPU and network) the curtain delayed the
    // first readable content by ~2 s (measured), too much for a clinic site
    // people may open in an emergency.
    const desktop = window.matchMedia?.("(hover: hover) and (pointer: fine) and (min-width: 981px)").matches;
    playIntro = desktop && location.pathname === "/" && !isReducedMotion() && !sessionStorage.getItem("sv_intro");
    sessionStorage.setItem("sv_intro", "1");
  } catch {
    playIntro = false;
  }
  const done = () => {
    preloader.remove();
    document.documentElement.removeAttribute("data-intro");
  };
  if (playIntro) {
    document.documentElement.setAttribute("data-intro", "");
    preloader.classList.add("pl-intro");
    preloader.addEventListener("animationend", (e) => e.animationName === "plCurtain" && done());
    setTimeout(done, 3000); // safety net if animationend never fires
  } else {
    preloader.classList.add("pl-hide");
    preloader.addEventListener("transitionend", done, { once: true });
    setTimeout(done, 1000);
  }
}
