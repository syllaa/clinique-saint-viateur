<script setup lang="ts">
import { useId } from "vue";

/**
 * Clinic emblem: a white medical cross on a bordeaux disc.
 * The cross is a single stroked + filled path with pathLength="1" so the
 * motion system can "draw" it later (stroke-dashoffset 1 → 0).
 */
withDefaults(defineProps<{ size?: number; title?: string }>(), {
  size: 38,
  title: undefined,
});

const gradientId = `brand-grad-${useId()}`;
</script>

<template>
  <svg
    class="brand-mark"
    :width="size"
    :height="size"
    viewBox="0 0 64 64"
    :role="title ? 'img' : undefined"
    :aria-label="title"
    :aria-hidden="title ? undefined : 'true'"
    focusable="false"
  >
    <defs>
      <linearGradient :id="gradientId" x1="0" y1="0" x2="1" y2="1">
        <stop offset="0" stop-color="#c8102e" />
        <stop offset="1" stop-color="#e0475a" />
      </linearGradient>
    </defs>
    <circle class="brand-mark-disc" cx="32" cy="32" r="32" :fill="`url(#${gradientId})`" />
    <path
      class="brand-mark-cross"
      d="M27 16h10v11h11v10H37v11H27V37H16V27h11z"
      fill="#fff"
      stroke="#fff"
      stroke-width="2"
      stroke-linejoin="round"
      pathLength="1"
    />
  </svg>
</template>

<style scoped>
.brand-mark {
  display: block;
  flex-shrink: 0;
}
</style>
