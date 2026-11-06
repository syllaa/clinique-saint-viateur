<script setup lang="ts">
import { onBeforeUnmount, ref } from "vue";
import { useRouter } from "vue-router";

/**
 * Thin progress bar at the very top of the window while a page is loading
 * (route chunks are lazy-loaded). Only appears if loading takes more than
 * 120 ms, so instant navigations stay clean.
 */
const router = useRouter();
const width = ref(0);
const visible = ref(false);
let showTimer: ReturnType<typeof setTimeout> | undefined;
let trickle: ReturnType<typeof setInterval> | undefined;
let hideTimer: ReturnType<typeof setTimeout> | undefined;

function start() {
  clearTimeout(hideTimer);
  clearTimeout(showTimer);
  showTimer = setTimeout(() => {
    visible.value = true;
    width.value = 12;
    clearInterval(trickle);
    trickle = setInterval(() => {
      width.value = Math.min(width.value + (90 - width.value) * 0.12, 90);
    }, 200);
  }, 120);
}

function done() {
  clearTimeout(showTimer);
  clearInterval(trickle);
  if (!visible.value) return;
  width.value = 100;
  hideTimer = setTimeout(() => {
    visible.value = false;
    width.value = 0;
  }, 350);
}

const removeBefore = router.beforeEach((to, from) => {
  if (to.path !== from.path) start();
});
const removeAfter = router.afterEach(done);
const removeError = router.onError(done);

onBeforeUnmount(() => {
  removeBefore();
  removeAfter();
  removeError();
  clearTimeout(showTimer);
  clearTimeout(hideTimer);
  clearInterval(trickle);
});
</script>

<template>
  <div class="nav-progress" :class="{ visible }" aria-hidden="true">
    <div class="nav-progress-bar" :style="{ width: `${width}%` }"></div>
  </div>
</template>

<style scoped>
.nav-progress {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  z-index: calc(var(--z-nav) + 20);
  pointer-events: none;
  opacity: 0;
  transition: opacity 0.3s;
}
.nav-progress.visible {
  opacity: 1;
}
.nav-progress-bar {
  height: 100%;
  background: linear-gradient(90deg, var(--brand-400), var(--brand-200));
  box-shadow: 0 0 10px rgba(243, 170, 180, 0.7);
  transition: width 0.3s var(--ease-out);
}
</style>
