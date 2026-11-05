<script setup lang="ts">
import { Phone } from "@lucide/vue";
import { onMounted } from "vue";

import { setMeta, setTitle } from "@/composables/useHead";

onMounted(() => {
  setTitle("Page introuvable – Clinique Saint Viateur");
  // Keep error pages out of search results (the next page resets it).
  setMeta("robots", "noindex");
});
</script>

<template>
  <section class="nf-section" aria-labelledby="nf-title">
    <!-- Heart-monitor trace: a bright pulse sweeps along a line that beats on
         the sides and goes flat in the middle, under the "404". -->
    <svg class="nf-ecg" viewBox="0 0 1200 160" preserveAspectRatio="none" aria-hidden="true">
      <path
        class="nf-ecg-base"
        d="M0 90 H140 L160 90 L172 60 L186 120 L200 30 L214 110 L226 90 H330 L346 90 L356 72 L368 102 L380 90 H520 H680 H820 L836 90 L846 72 L858 102 L870 90 H974 L994 90 L1006 60 L1020 120 L1034 30 L1048 110 L1060 90 H1200"
        pathLength="1"
      />
      <path
        class="nf-ecg-pulse"
        d="M0 90 H140 L160 90 L172 60 L186 120 L200 30 L214 110 L226 90 H330 L346 90 L356 72 L368 102 L380 90 H520 H680 H820 L836 90 L846 72 L858 102 L870 90 H974 L994 90 L1006 60 L1020 120 L1034 30 L1048 110 L1060 90 H1200"
        pathLength="1"
      />
    </svg>

    <div class="nf-inner">
      <p v-reveal="'scale'" class="nf-code" aria-hidden="true">404</p>
      <h1 id="nf-title" v-reveal class="d1">Page introuvable</h1>
      <p v-reveal class="nf-text d2">
        La page que vous cherchez n'existe pas ou a été déplacée. Pas d'inquiétude : nos équipes, elles, sont bien là.
      </p>
      <div v-reveal class="nf-actions d3">
        <RouterLink to="/" class="btn-primary">← Retour à l'accueil</RouterLink>
        <RouterLink to="/specialites" class="btn-outline">Voir nos spécialités</RouterLink>
      </div>
      <a v-reveal href="tel:+2252722590417" class="nf-urgent d4">
        <Phone :size="15" aria-hidden="true" /> Une urgence ? Appelez le 27 22 59 04 17
      </a>
    </div>
  </section>
</template>

<style scoped>
.nf-section {
  position: relative;
  overflow: hidden;
  min-height: 86vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 140px 5vw 70px;
  background:
    radial-gradient(ellipse 60% 50% at 50% 45%, rgba(224, 71, 90, 0.1), transparent 70%),
    var(--bg-alt);
}
.nf-ecg {
  position: absolute;
  left: 0;
  right: 0;
  /* Runs behind the big "404", never across the readable text below it. */
  top: calc(50% - 110px);
  width: 100%;
  height: 160px;
  translate: 0 -50%;
  fill: none;
  stroke-linejoin: round;
  stroke-linecap: round;
  pointer-events: none;
}
.nf-ecg-base {
  stroke: rgba(200, 16, 46, 0.12);
  stroke-width: 2;
}
.nf-ecg-pulse {
  stroke: var(--brand-600);
  stroke-width: 2.5;
  stroke-dasharray: 0.16 0.84;
  stroke-dashoffset: 1;
  filter: drop-shadow(0 0 6px rgba(200, 16, 46, 0.55));
  animation: sweep 3.2s linear infinite;
}
@keyframes sweep {
  to {
    stroke-dashoffset: 0;
  }
}
.nf-inner {
  position: relative;
  text-align: center;
  max-width: 520px;
}
.nf-code {
  font-family: "Cormorant Garamond", serif;
  font-size: clamp(6rem, 18vw, 10rem);
  font-weight: 600;
  line-height: 0.9;
  margin-bottom: 6px;
  background: linear-gradient(180deg, var(--brand-600), var(--brand-400));
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
}
.nf-inner h1 {
  font-size: clamp(1.5rem, 3vw, 2rem);
  color: var(--heading);
  margin-bottom: 12px;
}
.nf-text {
  color: var(--muted);
  font-size: 0.96rem;
  line-height: 1.7;
  margin-bottom: 28px;
}
.nf-actions {
  display: flex;
  gap: 14px;
  justify-content: center;
  flex-wrap: wrap;
}
.nf-urgent {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  margin-top: 28px;
  font-size: 0.85rem;
  font-weight: 600;
  color: var(--blue);
  text-decoration: none;
}
.nf-urgent:hover {
  text-decoration: underline;
  text-underline-offset: 3px;
}
</style>
