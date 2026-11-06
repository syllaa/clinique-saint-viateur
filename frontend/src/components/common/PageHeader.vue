<script setup lang="ts">
import Breadcrumbs from "@/components/common/Breadcrumbs.vue";

/**
 * Shared header of the public list pages: dark bordeaux band with slowly
 * drifting light, a heartbeat line drawing itself along the bottom, and the
 * page title rising word by word. `title` must be a static string (the
 * word-by-word reveal rewrites its text node).
 */
defineProps<{
  kicker: string;
  title: string;
  lead?: string;
  crumbs: { label: string; to?: string }[];
}>();
</script>

<template>
  <header class="page-header">
    <div class="ph-glow ph-glow-1" aria-hidden="true"></div>
    <div class="ph-glow ph-glow-2" aria-hidden="true"></div>
    <div class="ph-grid" aria-hidden="true"></div>
    <svg class="ph-ecg" viewBox="0 0 1200 60" preserveAspectRatio="none" aria-hidden="true">
      <path
        d="M0 40 H420 L440 40 L452 18 L466 56 L480 6 L494 48 L506 40 H780 L796 40 L806 26 L818 50 L830 40 H1200"
        pathLength="1"
      />
    </svg>
    <div class="ph-inner">
      <Breadcrumbs :items="crumbs" />
      <p v-reveal class="ph-kicker">{{ kicker }}</p>
      <h1 v-reveal="'words'" class="ph-title d1">{{ title }}</h1>
      <p v-if="lead" v-reveal class="ph-lead d2">{{ lead }}</p>
      <slot />
    </div>
  </header>
</template>

<style scoped>
.page-header {
  position: relative;
  overflow: hidden;
  padding: 150px 5vw 76px;
  background: linear-gradient(150deg, var(--brand-950) 0%, var(--brand-700) 70%, var(--brand-650) 100%);
  color: #fff;
  isolation: isolate;
}
.ph-glow {
  position: absolute;
  border-radius: 50%;
  filter: blur(70px);
  z-index: -1;
  pointer-events: none;
}
.ph-glow-1 {
  width: 520px;
  height: 520px;
  right: -120px;
  top: -180px;
  background: rgba(224, 71, 90, 0.35);
  animation: drift 16s ease-in-out infinite alternate;
}
.ph-glow-2 {
  width: 380px;
  height: 380px;
  left: 10%;
  bottom: -220px;
  background: rgba(200, 16, 46, 0.3);
  animation: drift 20s ease-in-out infinite alternate-reverse;
}
@keyframes drift {
  to {
    translate: -80px 60px;
    scale: 1.15;
  }
}
.ph-grid {
  position: absolute;
  inset: 0;
  z-index: -1;
  background-image:
    linear-gradient(rgba(255, 255, 255, 0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255, 255, 255, 0.03) 1px, transparent 1px);
  background-size: 55px 55px;
  mask-image: radial-gradient(ellipse 80% 90% at 70% 30%, black, transparent);
}
.ph-ecg {
  position: absolute;
  left: 0;
  right: 0;
  bottom: 14px;
  width: 100%;
  height: 60px;
  z-index: -1;
  fill: none;
  stroke: rgba(243, 170, 180, 0.45);
  stroke-width: 1.5;
  stroke-linejoin: round;
}
.ph-ecg path {
  stroke-dasharray: 1;
  stroke-dashoffset: 1;
  animation: ecgDraw 2.4s var(--ease-in-out) 0.4s forwards;
}
@keyframes ecgDraw {
  to {
    stroke-dashoffset: 0;
  }
}
.ph-inner {
  max-width: 1200px;
  margin: 0 auto;
}
.ph-inner :deep(.crumb-link),
.ph-inner :deep(.crumb-sep) {
  color: rgba(255, 255, 255, 0.6);
}
.ph-inner :deep(.crumb-current) {
  color: #fff;
}
.ph-kicker {
  font-size: 0.68rem;
  font-weight: 700;
  letter-spacing: 0.22em;
  text-transform: uppercase;
  color: var(--brand-200);
  margin-bottom: 12px;
}
.ph-title {
  font-size: clamp(2.2rem, 5vw, 3.8rem);
  line-height: 1.08;
  color: #fff;
  margin-bottom: 16px;
  max-width: 820px;
}
.ph-lead {
  max-width: 600px;
  font-size: 1rem;
  line-height: 1.8;
  color: rgba(255, 255, 255, 0.75);
}
@media (max-width: 640px) {
  .page-header {
    padding: 124px 16px 56px;
  }
}
</style>
