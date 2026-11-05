<script setup lang="ts">
import { Mail, MapPin, Phone } from "@lucide/vue";
import { ref } from "vue";

import IconFacebook from "@/components/brand/IconFacebook.vue";
import HeroCanvas from "@/components/hero/HeroCanvas.vue";
import heroPhoto960 from "@/assets/images/hero/hero-ambulance-facade-960.webp";
import heroPhoto from "@/assets/images/hero/hero-ambulance-facade.webp";
import { useClinicHours } from "@/composables/useClinicHours";
import { magnetic } from "@/motion/animations";
import { useScrollScene } from "@/motion/useScrollScene";

const { statusLabel, consultationsOpen } = useClinicHours();

// Click feedback on the emergency number: a ring ripples out from the card.
const rippling = ref(false);
function ripple() {
  rippling.value = false;
  requestAnimationFrame(() => (rippling.value = true));
}

const heroRef = ref<HTMLElement | null>(null);
useScrollScene(heroRef, (kit, hero) => {
  const { gsap } = kit;
  const cleanups = Array.from(hero.querySelectorAll<HTMLElement>(".hero-btns a")).map((btn) => magnetic(kit, btn, 0.22));

  // Depth on scroll: photo drifts slower than the content, content fades away.
  const scroll = { trigger: hero, start: "top top", end: "bottom top", scrub: true };
  gsap.to(hero.querySelector(".hero-photo-wrap"), { yPercent: 12, scale: 1.08, ease: "none", scrollTrigger: scroll });
  gsap.to(hero.querySelector(".hero-inner"), { yPercent: -10, autoAlpha: 0.25, ease: "none", scrollTrigger: scroll });
  gsap.to(hero.querySelector(".scroll-hint"), { autoAlpha: 0, ease: "none", scrollTrigger: { ...scroll, end: "15% top" } });

  return () => cleanups.forEach((fn) => fn());
});
</script>

<template>
  <section id="hero" ref="heroRef" aria-labelledby="hero-title">
    <!-- GSAP moves the wrapper (parallax); CSS zooms the image inside it. -->
    <div class="hero-photo-wrap">
      <img
        class="hero-photo"
        :src="heroPhoto"
        :srcset="`${heroPhoto960} 960w, ${heroPhoto} 1920w`"
        sizes="100vw"
        alt=""
        width="1920"
        height="1080"
        fetchpriority="high"
        decoding="async"
      />
    </div>
    <HeroCanvas />
    <div class="hero-grad"></div>
    <div class="hero-grid"></div>
    <div class="ring ring-1"></div>
    <div class="ring ring-2"></div>
    <div class="ring ring-3"></div>
    <div class="hero-bottom-fade"></div>

    <div class="hero-inner">
      <div>
        <p v-reveal class="hero-badge" role="status">
          <span class="live-dot" :class="{ closed: !consultationsOpen }" aria-hidden="true"></span>
          Urgences 24h/24 · {{ statusLabel }}
        </p>
        <h1 id="hero-title" v-reveal="'words'" class="hero-title d1">
          Des soins de qualité,<br />au cœur de la <em>Riviera</em><br />Sideci.
        </h1>
        <!-- No entrance animation on purpose: this paragraph is the page's
             Largest Contentful Paint, it must be visible at first render. -->
        <p class="hero-sub">
          Établissement médical privé de référence à Cocody, Abidjan. Une équipe de professionnels expérimentés, des
          équipements modernes et une prise en charge complète pour toute la famille.
        </p>
        <div v-reveal class="hero-btns d3">
          <a href="tel:+2252722590417" class="btn-primary"><Phone :size="16" aria-hidden="true" /> Prendre rendez-vous</a>
          <a href="#services" class="btn-outline-light">Nos services →</a>
        </div>
        <div v-reveal class="hero-stats d4">
          <div class="hstat"><div class="hstat-n" v-count-up="{ target: 79, suffix: 'K+' }">0K+</div><div class="hstat-l">Patients fidèles</div></div>
          <div class="hstat"><div class="hstat-n" v-count-up="{ target: 10, suffix: '+' }">0+</div><div class="hstat-l">Spécialités</div></div>
          <div class="hstat"><div class="hstat-n">24/7</div><div class="hstat-l">Urgences & soins</div></div>
        </div>
      </div>

      <div class="hero-right">
        <!-- The wrapper carries the entrance; the card keeps its own
             "breathing" animation (one element can't run both). -->
        <div v-reveal="'scale'" class="d2">
        <a
          href="tel:+2252722590417"
          class="urgence-box"
          :class="{ rippling }"
          @click="ripple"
          @animationend="rippling = false"
        >
          <span class="urgence-label"><span class="pulse-ring" aria-hidden="true"></span> Urgences disponibles maintenant</span>
          <span class="urgence-phone">27 22 59 04 17</span>
          <span class="urgence-sub">Ligne principale · 24h/24 · 7j/7 · Touchez pour appeler</span>
        </a>
        </div>
        <ul class="info-stack">
          <li v-reveal="'right'" class="icard d2">
            <span class="icard-icon"><MapPin :size="18" aria-hidden="true" /></span>
            <p><strong>Adresse</strong>Route Akouédo, Riviera Sideci – Cocody<br />22 BP 289, Abidjan 22</p>
          </li>
          <li v-reveal="'right'" class="icard d3">
            <span class="icard-icon"><Phone :size="18" aria-hidden="true" /></span>
            <p>
              <strong>Autres lignes</strong>
              <a href="tel:+2250101466576">01 01 46 65 76</a> ·
              <a href="tel:+2250707095549">07 07 09 55 49</a> ·
              <a href="tel:+2252247264700">22 47 26 47</a>
            </p>
          </li>
          <li v-reveal="'right'" class="icard d3">
            <span class="icard-icon"><Mail :size="18" aria-hidden="true" /></span>
            <p><strong>Email</strong><a href="mailto:cliniquestviateur@aviso.ci">cliniquestviateur@aviso.ci</a></p>
          </li>
          <li v-reveal="'right'" class="icard d4">
            <span class="icard-icon"><IconFacebook :size="18" /></span>
            <p>
              <strong>Facebook</strong>
              <a href="https://www.facebook.com/CliniqueMedicaleSaintViateur/" target="_blank" rel="noopener">
                CliniqueMedicaleSaintViateur<span class="sr-only"> (s'ouvre dans un nouvel onglet)</span>
              </a>
            </p>
          </li>
        </ul>
      </div>
    </div>

    <a href="#services" class="scroll-hint" aria-label="Défiler vers nos spécialités">
      <span class="scroll-mouse" aria-hidden="true"><span class="scroll-wheel"></span></span>
      <span aria-hidden="true">Défiler</span>
    </a>
  </section>
</template>

<style scoped>
#hero {
  min-height: 100vh;
  min-height: 100svh;
  position: relative;
  overflow: hidden;
  display: flex;
  align-items: center;
  padding: 120px 5vw 96px;
  background: var(--brand-950);
}
.hero-photo-wrap {
  position: absolute;
  inset: -6% 0 auto;
  height: 112%;
  overflow: hidden;
}
.hero-photo {
  display: block;
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center 60%;
  opacity: 0.28;
  filter: saturate(0.7) contrast(1.05);
  transform-origin: center 30%;
  animation: heroZoom 24s ease-out both;
}
@keyframes heroZoom {
  from {
    transform: scale(1.12);
  }
  to {
    transform: scale(1);
  }
}
.hero-grad {
  position: absolute;
  inset: 0;
  z-index: 1;
  pointer-events: none;
  background:
    radial-gradient(ellipse 60% 70% at 78% 40%, rgba(200, 16, 46, 0.28), transparent 70%),
    linear-gradient(155deg, rgba(24, 8, 9, 0.95) 0%, rgba(122, 15, 26, 0.86) 55%, rgba(143, 22, 32, 0.78) 100%);
}
.hero-grid {
  position: absolute;
  inset: 0;
  z-index: 1;
  pointer-events: none;
  background-image:
    linear-gradient(rgba(255, 255, 255, 0.025) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255, 255, 255, 0.025) 1px, transparent 1px);
  background-size: 55px 55px;
  mask-image: radial-gradient(ellipse 70% 80% at 40% 50%, black 0%, transparent 100%);
}
.hero-bottom-fade {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 130px;
  z-index: 2;
  pointer-events: none;
  background: linear-gradient(to top, var(--bg) 0%, transparent 75%);
}
.ring {
  position: absolute;
  border-radius: 50%;
  border: 1px solid rgba(200, 16, 46, 0.12);
  pointer-events: none;
  z-index: 1;
  top: 50%;
  left: 72%;
  translate: -50% -50%;
  animation: ringBreath 9s ease-in-out infinite;
}
.ring-1 {
  width: 550px;
  height: 550px;
}
.ring-2 {
  width: 780px;
  height: 780px;
  animation-delay: -3s;
}
.ring-3 {
  width: 1050px;
  height: 1050px;
  animation-delay: -6s;
}
@keyframes ringBreath {
  0%,
  100% {
    scale: 1;
    opacity: 0.7;
  }
  50% {
    scale: 1.04;
    opacity: 1;
  }
}
.hero-inner {
  max-width: 1200px;
  margin: 0 auto;
  width: 100%;
  display: grid;
  grid-template-columns: 1.1fr 0.9fr;
  gap: 56px;
  align-items: center;
  position: relative;
  z-index: 5;
}
.hero-badge {
  display: inline-flex;
  align-items: center;
  gap: 9px;
  background: rgba(255, 255, 255, 0.06);
  border: 1px solid rgba(243, 170, 180, 0.3);
  color: var(--brand-200);
  font-size: 0.7rem;
  font-weight: 600;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  padding: 7px 15px;
  border-radius: var(--radius-pill);
  margin-bottom: 24px;
  backdrop-filter: blur(6px);
}
.live-dot,
.pulse-ring {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #4ade80;
  flex-shrink: 0;
  animation: livePulse 2.2s infinite;
}
.live-dot.closed {
  background: #fbbf24;
}
@keyframes livePulse {
  0% {
    box-shadow: 0 0 0 0 rgba(74, 222, 128, 0.55);
  }
  70% {
    box-shadow: 0 0 0 9px rgba(74, 222, 128, 0);
  }
  100% {
    box-shadow: 0 0 0 0 rgba(74, 222, 128, 0);
  }
}
.hero-title {
  font-size: clamp(2.6rem, 5.2vw, 4.6rem);
  font-weight: 600;
  color: #fff;
  line-height: 1.04;
  letter-spacing: -0.01em;
  margin-bottom: 22px;
}
/* The gradient sits on the word spans created by v-reveal="'words'" (each
   is its own compositing layer while it animates, so a gradient clipped on
   the <em> itself would leave the word transparent). Plain colour fallback
   on the <em> for browsers without background-clip: text. */
.hero-title em {
  font-style: italic;
  color: var(--brand-200);
}
@supports (background-clip: text) or (-webkit-background-clip: text) {
  .hero-title em :deep(.rv-wi) {
    background: linear-gradient(100deg, var(--brand-200), #fff 45%, var(--brand-400));
    background-size: 220% 100%;
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
    animation: shimmerText 7s ease-in-out infinite alternate;
    padding-right: 0.08em;
  }
}
@keyframes shimmerText {
  from {
    background-position: 0% 50%;
  }
  to {
    background-position: 100% 50%;
  }
}
.hero-sub {
  color: rgba(255, 255, 255, 0.7);
  font-size: 1rem;
  max-width: 480px;
  line-height: 1.8;
  margin-bottom: 34px;
}
.hero-btns {
  display: flex;
  gap: 14px;
  flex-wrap: wrap;
}
.hero-stats {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
  margin-top: 44px;
  max-width: 520px;
}
.hstat {
  background: rgba(24, 8, 9, 0.5);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.12);
  border-radius: 12px;
  padding: 16px;
  text-align: center;
}
.hstat-n {
  font-family: "Cormorant Garamond", serif;
  font-size: 2.1rem;
  color: var(--brand-200);
  line-height: 1;
}
.hstat-l {
  font-size: 0.68rem;
  color: rgba(255, 255, 255, 0.75);
  margin-top: 5px;
  letter-spacing: 0.05em;
}
.hero-right {
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.urgence-box {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
  background: linear-gradient(135deg, var(--brand-600), var(--brand-800));
  border-radius: 16px;
  padding: 24px 26px;
  color: #fff;
  text-align: center;
  text-decoration: none;
  box-shadow: 0 18px 50px rgba(200, 16, 46, 0.35);
  animation: breathe 4.5s ease-in-out infinite;
  transition: transform var(--dur-fast) var(--ease-out);
}
.urgence-box:hover {
  transform: translateY(-3px);
}
/* Gentle "breathing" glow: the most important element of the page. */
@keyframes breathe {
  0%,
  100% {
    box-shadow: 0 18px 50px rgba(200, 16, 46, 0.3);
  }
  50% {
    box-shadow: 0 18px 64px rgba(224, 71, 90, 0.55);
  }
}
.urgence-box::after {
  content: "";
  position: absolute;
  inset: 0;
  border-radius: inherit;
  border: 2px solid rgba(255, 255, 255, 0.7);
  opacity: 0;
  pointer-events: none;
}
.urgence-box.rippling::after {
  animation: rippleOut 0.9s var(--ease-out);
}
@keyframes rippleOut {
  from {
    opacity: 0.9;
    transform: scale(1);
  }
  to {
    opacity: 0;
    transform: scale(1.12, 1.35);
  }
}
.urgence-label {
  font-size: 0.66rem;
  letter-spacing: 0.16em;
  text-transform: uppercase;
  opacity: 0.85;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}
.urgence-phone {
  font-family: "Cormorant Garamond", serif;
  font-size: clamp(1.9rem, 3vw, 2.4rem);
  font-weight: 700;
  letter-spacing: 0.02em;
  line-height: 1.1;
}
.urgence-sub {
  font-size: 0.73rem;
  opacity: 0.75;
}
.info-stack {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 9px;
}
.icard {
  display: flex;
  align-items: center;
  gap: 13px;
  background: rgba(24, 8, 9, 0.5);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.12);
  border-radius: 12px;
  padding: 13px 16px;
  color: #fff;
  transition:
    border-color var(--dur-fast),
    background var(--dur-fast);
}
.icard:hover {
  border-color: rgba(243, 170, 180, 0.35);
  background: rgba(24, 8, 9, 0.65);
}
.icard-icon {
  display: flex;
  justify-content: center;
  flex-shrink: 0;
  width: 24px;
  color: var(--brand-200);
}
.icard p {
  font-size: 0.8rem;
  line-height: 1.5;
  opacity: 0.92;
}
.icard a {
  color: inherit;
  text-decoration: none;
}
.icard a:hover {
  text-decoration: underline;
  text-underline-offset: 3px;
}
.icard p strong {
  display: block;
  font-size: 0.62rem;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  opacity: 0.6;
  margin-bottom: 2px;
  font-weight: 500;
}
.scroll-hint {
  position: absolute;
  bottom: 28px;
  left: 50%;
  translate: -50% 0;
  z-index: 5;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  color: rgba(255, 255, 255, 0.45);
  font-size: 0.65rem;
  letter-spacing: 0.13em;
  text-transform: uppercase;
  text-decoration: none;
}
.scroll-mouse {
  width: 21px;
  height: 34px;
  border: 1.5px solid rgba(255, 255, 255, 0.3);
  border-radius: 11px;
  display: flex;
  justify-content: center;
  padding-top: 5px;
}
.scroll-wheel {
  width: 2.5px;
  height: 6px;
  background: rgba(255, 255, 255, 0.6);
  border-radius: 2px;
  animation: wheel 1.8s ease-in-out infinite;
}
@keyframes wheel {
  0% {
    transform: translateY(0);
    opacity: 1;
  }
  70% {
    transform: translateY(10px);
    opacity: 0;
  }
  100% {
    transform: translateY(0);
    opacity: 0;
  }
}

@media (max-width: 980px) {
  .hero-inner {
    grid-template-columns: 1fr;
  }
  .ring {
    left: 50%;
  }
}
@media (max-width: 640px) {
  /* Phones: drop the costliest effects (backdrop blur on 8 cards, three
     animated 500–1000 px rings). Solid tints look nearly identical. */
  .hstat,
  .icard,
  .hero-badge {
    backdrop-filter: none;
    -webkit-backdrop-filter: none;
    background: rgba(24, 8, 9, 0.72);
  }
  .ring {
    animation: none;
  }
  .ring-3 {
    display: none;
  }
  #hero {
    padding: 112px 16px 88px;
  }
  .hero-stats {
    gap: 8px;
  }
  .hstat {
    padding: 12px 6px;
  }
  .hstat-n {
    font-size: 1.6rem;
  }
  .hstat-l {
    font-size: 0.62rem;
    letter-spacing: 0.02em;
  }
  .scroll-hint {
    display: none;
  }
}
</style>
