<script setup lang="ts">
import { onBeforeUnmount, onMounted, ref } from "vue";

/**
 * Reading progress for long content: a thin bar under the fixed header that
 * fills as the visitor reads through `target`. Exposed to assistive tech as
 * a progressbar (percentage).
 */
const props = defineProps<{ target: HTMLElement | null }>();

const progress = ref(0);
let frame = 0;

function measure() {
  cancelAnimationFrame(frame);
  frame = requestAnimationFrame(() => {
    const el = props.target;
    if (!el) return;
    const rect = el.getBoundingClientRect();
    const total = rect.height - window.innerHeight * 0.6;
    const read = -rect.top + window.innerHeight * 0.25;
    progress.value = Math.round(Math.min(Math.max(read / Math.max(total, 1), 0), 1) * 100);
  });
}

onMounted(() => {
  window.addEventListener("scroll", measure, { passive: true });
  window.addEventListener("resize", measure, { passive: true });
  measure();
});
onBeforeUnmount(() => {
  cancelAnimationFrame(frame);
  window.removeEventListener("scroll", measure);
  window.removeEventListener("resize", measure);
});
</script>

<template>
  <div
    class="reading-progress"
    role="progressbar"
    aria-label="Progression de la lecture"
    aria-valuemin="0"
    aria-valuemax="100"
    :aria-valuenow="progress"
  >
    <div class="reading-progress-bar" :style="{ transform: `scaleX(${progress / 100})` }"></div>
  </div>
</template>

<style scoped>
.reading-progress {
  position: fixed;
  top: 68px;
  left: 0;
  right: 0;
  height: 3px;
  z-index: calc(var(--z-nav) - 1);
  background: rgba(200, 16, 46, 0.12);
}
.reading-progress-bar {
  height: 100%;
  background: linear-gradient(90deg, var(--brand-600), var(--brand-400));
  transform-origin: left center;
  transition: transform 0.12s linear;
}
</style>
