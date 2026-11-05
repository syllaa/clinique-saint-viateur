import { createPinia } from "pinia";
import { createApp } from "vue";

import App from "./App.vue";
import "./assets/base.css";
import { vCountUp } from "./directives/countUp";
import { vReveal } from "./directives/reveal";
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
