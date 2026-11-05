<script setup lang="ts">
import { Navigation, Phone } from "@lucide/vue";
import { ref } from "vue";

import AmbientVideo from "@/components/common/AmbientVideo.vue";
import { magnetic } from "@/motion/animations";
import { useScrollScene } from "@/motion/useScrollScene";

const bannerRef = ref<HTMLElement | null>(null);
useScrollScene(bannerRef, (kit, banner) => {
  const call = banner.querySelector<HTMLElement>(".em-call");
  return call ? magnetic(kit, call, 0.2) : undefined;
});
</script>

<template>
  <section ref="bannerRef" class="emergency" aria-labelledby="emergency-title">
    <!-- Optional film (src/assets/media/urgences.*). Without it, the ECG
         trace and gradient carry the section on their own. -->
    <AmbientVideo class="em-video" media="urgences" />
    <svg class="em-ecg" viewBox="0 0 1200 120" preserveAspectRatio="none" aria-hidden="true">
      <path
        d="M0 70 H220 L240 70 L252 40 L266 100 L280 12 L294 92 L306 70 H520 L536 70 L546 52 L558 84 L570 70 H760 L780 70 L792 40 L806 100 L820 12 L834 92 L846 70 H1060 L1076 70 L1086 52 L1098 84 L1110 70 H1200"
        pathLength="1"
      />
    </svg>

    <div class="em-inner">
      <p v-reveal class="em-kicker"><span class="em-dot" aria-hidden="true"></span> Urgences & réanimation</p>
      <h2 id="emergency-title" v-reveal="'words'" class="em-title d1">Une équipe mobilisée 24h/24, 7j/7</h2>
      <p v-reveal class="em-text d2">
        Les urgences et la réanimation sont disponibles 24 heures sur 24, 7 jours sur 7, sans interruption. Appelez
        avant de venir : l'équipe se prépare à votre arrivée.
      </p>
      <div v-reveal class="em-actions d3">
        <a href="tel:+2252722590417" class="em-call">
          <Phone :size="22" aria-hidden="true" />
          <span><small>Ligne d'urgence</small>27 22 59 04 17</span>
        </a>
        <a
          href="https://maps.google.com/?q=Clinique+Medicale+Saint+Viateur+Cocody+Abidjan"
          class="btn-outline-light"
          target="_blank"
          rel="noopener"
        >
          <Navigation :size="16" aria-hidden="true" /> Itinéraire
          <span class="sr-only">(s'ouvre dans un nouvel onglet)</span>
        </a>
      </div>
      <p v-reveal class="em-lines d4">
        Autres lignes :
        <a href="tel:+2250101466576">01 01 46 65 76</a> ·
        <a href="tel:+2250707095549">07 07 09 55 49</a> ·
        <a href="tel:+2252247264700">22 47 26 47</a>
      </p>
    </div>
  </section>
</template>

<style scoped>
.emergency {
  position: relative;
  overflow: hidden;
  isolation: isolate;
  padding: 104px 5vw;
  color: #fff;
  background:
    radial-gradient(ellipse 50% 60% at 80% 30%, rgba(224, 71, 90, 0.35), transparent 70%),
    linear-gradient(160deg, var(--brand-950), var(--brand-800));
}
.em-video {
  position: absolute;
  inset: 0;
  z-index: -2;
  opacity: 0.3;
  filter: saturate(0.6);
}
.em-ecg {
  position: absolute;
  left: 0;
  right: 0;
  /* Sits in the bottom padding, never behind the number or the text. */
  bottom: 4px;
  width: 100%;
  height: 70px;
  z-index: -1;
  fill: none;
  stroke: rgba(243, 170, 180, 0.35);
  stroke-width: 2;
  stroke-linejoin: round;
}
/* A brighter pulse travels along the trace, like a monitor. */
.em-ecg path {
  stroke-dasharray: 0.22 0.78;
  animation: emSweep 4s linear infinite;
}
@keyframes emSweep {
  from {
    stroke-dashoffset: 1;
  }
  to {
    stroke-dashoffset: 0;
  }
}
.em-inner {
  max-width: 1200px;
  margin: 0 auto;
}
.em-kicker {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  font-size: 0.72rem;
  font-weight: 700;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  color: var(--brand-200);
  margin-bottom: 16px;
}
.em-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: #4ade80;
  animation: emPulse 1.6s infinite;
}
@keyframes emPulse {
  0% {
    box-shadow: 0 0 0 0 rgba(74, 222, 128, 0.6);
  }
  70% {
    box-shadow: 0 0 0 12px rgba(74, 222, 128, 0);
  }
  100% {
    box-shadow: 0 0 0 0 rgba(74, 222, 128, 0);
  }
}
.em-title {
  font-size: clamp(2.2rem, 5vw, 4rem);
  line-height: 1.05;
  max-width: 760px;
  margin-bottom: 18px;
  text-wrap: balance;
}
.em-text {
  max-width: 560px;
  font-size: 1rem;
  line-height: 1.8;
  color: rgba(255, 255, 255, 0.78);
  margin-bottom: 34px;
}
.em-actions {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 16px;
}
.em-call {
  display: inline-flex;
  align-items: center;
  gap: 14px;
  padding: 16px 28px;
  border-radius: var(--radius-lg);
  background: #fff;
  color: var(--brand-700);
  text-decoration: none;
  box-shadow: 0 18px 50px rgba(0, 0, 0, 0.3);
}
.em-call span {
  display: flex;
  flex-direction: column;
  font-family: "Cormorant Garamond", serif;
  font-size: 1.8rem;
  font-weight: 700;
  line-height: 1.05;
}
.em-call small {
  font-family: "DM Sans", sans-serif;
  font-size: 0.62rem;
  font-weight: 700;
  letter-spacing: 0.16em;
  text-transform: uppercase;
  color: var(--brand-600);
}
.em-lines {
  margin-top: 22px;
  font-size: 0.85rem;
  color: rgba(255, 255, 255, 0.7);
}
.em-lines a {
  color: #fff;
  text-decoration: none;
  font-weight: 600;
}
.em-lines a:hover {
  text-decoration: underline;
  text-underline-offset: 3px;
}
@media (max-width: 640px) {
  .emergency {
    padding: 80px 16px;
  }
  .em-call {
    width: 100%;
    justify-content: center;
  }
}
</style>
