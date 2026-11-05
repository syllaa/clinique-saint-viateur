import { createPinia } from "pinia";
import { createApp } from "vue";

import App from "./App.vue";
import "./assets/base.css";
import "./assets/ui.css";
import { vCountUp } from "./directives/countUp";
import { vReveal } from "./directives/reveal";
// Imported for its side effect: sets <html data-motion> before the first render,
// so reveal animations never flash when reduced motion is on.
import "./motion/motionPreferences";
import router from "./router";

const app = createApp(App);

app.use(createPinia());
app.use(router);
app.directive("reveal", vReveal);
app.directive("count-up", vCountUp);

app.mount("#app");

const preloader = document.getElementById("preloader");
if (preloader) {
  preloader.classList.add("pl-hide");
  preloader.addEventListener("transitionend", () => preloader.remove(), { once: true });
}
