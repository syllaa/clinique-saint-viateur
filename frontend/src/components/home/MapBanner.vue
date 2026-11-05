<script setup lang="ts">
import { MapPin, Navigation } from "@lucide/vue";
import { ref } from "vue";

import { magnetic } from "@/motion/animations";
import { useScrollScene } from "@/motion/useScrollScene";

const bannerRef = ref<HTMLElement | null>(null);
useScrollScene(bannerRef, (kit, banner) => {
  const btn = banner.querySelector<HTMLElement>(".btn-white");
  return btn ? magnetic(kit, btn, 0.3) : undefined;
});
</script>

<template>
  <section ref="bannerRef" class="map-banner" aria-labelledby="map-title">
    <!-- Decorative: a pin drops onto concentric "radar" waves. -->
    <div class="map-pin" aria-hidden="true">
      <span class="wave"></span>
      <span class="wave"></span>
      <span class="wave"></span>
      <MapPin class="pin" :size="38" :stroke-width="1.6" />
    </div>
    <div class="map-content">
      <h2 id="map-title" v-reveal="'words'">Venez nous rendre visite</h2>
      <p v-reveal class="d1">Route Akouédo, Riviera Sideci – Cocody, Abidjan · Proche Riviera 3 et Lycée Blaise-Pascal</p>
      <a
        v-reveal
        class="d2 btn-white"
        href="https://maps.google.com/?q=Clinique+Medicale+Saint+Viateur+Cocody+Abidjan"
        target="_blank"
        rel="noopener"
      >
        <Navigation :size="16" aria-hidden="true" /> Itinéraire Google Maps
        <span class="sr-only">(s'ouvre dans un nouvel onglet)</span>
      </a>
    </div>
  </section>
</template>

<style scoped>
.map-banner {
  position: relative;
  overflow: hidden;
  background:
    radial-gradient(circle at 50% 35%, rgba(224, 71, 90, 0.25), transparent 55%),
    linear-gradient(135deg, var(--brand-700), var(--brand-800));
  padding: 84px 5vw 76px;
  text-align: center;
  color: #fff;
}
.map-content {
  position: relative;
  z-index: 1;
}
.map-banner h2 {
  font-size: clamp(1.9rem, 3.4vw, 2.7rem);
  margin-bottom: 12px;
}
.map-banner p {
  opacity: 0.78;
  margin-bottom: 28px;
  font-size: 0.95rem;
}
.map-pin {
  position: relative;
  width: 64px;
  height: 64px;
  margin: 0 auto 18px;
  display: grid;
  place-items: center;
}
.pin {
  position: relative;
  color: #fff;
  animation: pinDrop 2.8s var(--ease-out) infinite;
}
.wave {
  position: absolute;
  left: 50%;
  top: 72%;
  width: 18px;
  height: 7px;
  border-radius: 50%;
  border: 1.5px solid rgba(255, 255, 255, 0.6);
  translate: -50% -50%;
  animation: wave 2.8s ease-out infinite;
  opacity: 0;
}
.wave:nth-child(2) {
  animation-delay: 0.35s;
}
.wave:nth-child(3) {
  animation-delay: 0.7s;
}
@keyframes pinDrop {
  0% {
    transform: translateY(-26px);
    opacity: 0;
  }
  22% {
    transform: translateY(0);
    opacity: 1;
  }
  30% {
    transform: translateY(-5px);
  }
  38%,
  100% {
    transform: translateY(0);
  }
}
@keyframes wave {
  20% {
    opacity: 0;
    scale: 1;
  }
  25% {
    opacity: 0.8;
  }
  100% {
    opacity: 0;
    scale: 7;
  }
}
</style>
