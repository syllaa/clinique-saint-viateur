<script setup lang="ts">
import { Clock, Mail, MapPin, Pause, Phone, Play } from "@lucide/vue";

import BrandMark from "@/components/brand/BrandMark.vue";
import IconFacebook from "@/components/brand/IconFacebook.vue";
import { useMotionPreference } from "@/motion/motionPreferences";

const year = new Date().getFullYear();
const { reducedMotion, toggle: toggleMotion } = useMotionPreference();
</script>

<template>
  <footer class="site-footer">
    <div class="footer-grid">
      <div class="footer-col footer-about">
        <RouterLink to="/" class="footer-brand">
          <BrandMark :size="40" />
          <span>Clinique Médicale<br />Saint Viateur</span>
        </RouterLink>
        <p class="footer-tagline">
          Établissement médical privé à Cocody, Abidjan. Urgences et réanimation disponibles 24h/24, 7j/7.
        </p>
        <a href="tel:+2252722590417" class="footer-emergency">
          <Phone :size="16" aria-hidden="true" />
          <span><small>Urgences 24h/24</small>27 22 59 04 17</span>
        </a>
      </div>

      <nav class="footer-col" aria-label="Plan du site">
        <h2 class="footer-heading">La clinique</h2>
        <ul class="footer-list">
          <li><RouterLink to="/specialites">Nos spécialités</RouterLink></li>
          <li><RouterLink to="/#about">Notre histoire</RouterLink></li>
          <li><RouterLink to="/promotions">Offres du moment</RouterLink></li>
          <li><RouterLink to="/blog">Actualités & conseils</RouterLink></li>
          <li><RouterLink to="/#temoignages">Avis patients</RouterLink></li>
          <li><RouterLink to="/nous-rejoindre">Nous rejoindre</RouterLink></li>
        </ul>
      </nav>

      <div class="footer-col">
        <h2 class="footer-heading">Contact</h2>
        <ul class="footer-list footer-contact">
          <li>
            <MapPin :size="15" aria-hidden="true" />
            <span>Route Akouédo, Riviera Sideci – Cocody<br />22 BP 289, Abidjan 22</span>
          </li>
          <li>
            <Phone :size="15" aria-hidden="true" />
            <span>
              <a href="tel:+2252722590417">27 22 59 04 17</a> ·
              <a href="tel:+2250707095549">07 07 09 55 49</a>
            </span>
          </li>
          <li>
            <Mail :size="15" aria-hidden="true" />
            <a href="mailto:cliniquestviateur@aviso.ci">cliniquestviateur@aviso.ci</a>
          </li>
          <li>
            <IconFacebook :size="15" />
            <a href="https://www.facebook.com/CliniqueMedicaleSaintViateur/" target="_blank" rel="noopener">
              CliniqueMedicaleSaintViateur<span class="sr-only"> (s'ouvre dans un nouvel onglet)</span>
            </a>
          </li>
        </ul>
      </div>

      <div class="footer-col">
        <h2 class="footer-heading">Horaires</h2>
        <ul class="footer-list footer-hours">
          <li><Clock :size="15" aria-hidden="true" /><span>Lun – Ven : 08h – 20h</span></li>
          <li><Clock :size="15" aria-hidden="true" /><span>Samedi : 08h – 12h</span></li>
          <li class="footer-hours-urgent"><span class="live-dot" aria-hidden="true"></span><span>Urgences : 24h/24 · 7j/7</span></li>
        </ul>
      </div>
    </div>

    <div class="footer-bottom">
      <p>© {{ year }} Clinique Médicale Saint Viateur · Tous droits réservés</p>
      <button type="button" class="motion-toggle" :aria-pressed="reducedMotion" @click="toggleMotion">
        <Play v-if="reducedMotion" :size="14" aria-hidden="true" />
        <Pause v-else :size="14" aria-hidden="true" />
        {{ reducedMotion ? "Réactiver les animations" : "Réduire les animations" }}
      </button>
    </div>
  </footer>
</template>

<style scoped>
.site-footer {
  background: var(--brand-950);
  color: rgba(255, 255, 255, 0.72);
  padding: var(--space-8) 5vw var(--space-5);
}
.footer-grid {
  max-width: 1200px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: 1.4fr 1fr 1.3fr 1fr;
  gap: var(--space-7) var(--space-6);
}
.footer-brand {
  display: inline-flex;
  align-items: center;
  gap: var(--space-3);
  text-decoration: none;
  color: #fff;
  font-family: var(--font-serif);
  font-size: 1.15rem;
  line-height: 1.15;
}
.footer-tagline {
  margin: var(--space-4) 0 var(--space-5);
  font-size: 0.85rem;
  line-height: 1.7;
  max-width: 320px;
}
.footer-emergency {
  display: inline-flex;
  align-items: center;
  gap: var(--space-3);
  padding: 12px 18px;
  border-radius: var(--radius-md);
  background: var(--brand-600);
  color: #fff;
  text-decoration: none;
  font-weight: 600;
  font-size: 1.05rem;
  transition:
    background var(--dur-fast),
    transform var(--dur-fast) var(--ease-out);
}
.footer-emergency:hover {
  background: var(--brand-400);
  transform: translateY(-2px);
}
.footer-emergency span {
  display: flex;
  flex-direction: column;
  line-height: 1.2;
}
.footer-emergency small {
  font-size: 0.62rem;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  font-weight: 600;
  opacity: 0.85;
}
.footer-heading {
  font-family: var(--font-sans);
  font-size: 0.7rem;
  font-weight: 700;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  color: var(--brand-200);
  margin-bottom: var(--space-4);
}
.footer-list {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 10px;
  font-size: 0.86rem;
}
.footer-list a {
  color: rgba(255, 255, 255, 0.78);
  text-decoration: none;
  transition: color var(--dur-fast);
}
.footer-list a:hover {
  color: #fff;
  text-decoration: underline;
  text-underline-offset: 3px;
}
.footer-contact li,
.footer-hours li {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  line-height: 1.5;
}
.footer-contact svg,
.footer-hours svg {
  margin-top: 3px;
  flex-shrink: 0;
  color: var(--brand-200);
}
.footer-hours-urgent {
  align-items: center !important;
  color: #fff;
  font-weight: 600;
}
.live-dot {
  width: 9px;
  height: 9px;
  margin: 0 3px;
  border-radius: 50%;
  background: #4ade80;
  box-shadow: 0 0 0 0 rgba(74, 222, 128, 0.6);
  animation: footer-pulse 2s infinite;
  flex-shrink: 0;
}
@keyframes footer-pulse {
  70% {
    box-shadow: 0 0 0 8px rgba(74, 222, 128, 0);
  }
  100% {
    box-shadow: 0 0 0 0 rgba(74, 222, 128, 0);
  }
}
.footer-bottom {
  max-width: 1200px;
  margin: var(--space-7) auto 0;
  padding-top: var(--space-5);
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  font-size: 0.78rem;
  color: rgba(255, 255, 255, 0.62);
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;
  gap: var(--space-3);
}
.motion-toggle {
  display: inline-flex;
  align-items: center;
  gap: 7px;
  padding: 7px 14px;
  border-radius: var(--radius-pill);
  border: 1px solid rgba(255, 255, 255, 0.2);
  background: transparent;
  color: rgba(255, 255, 255, 0.78);
  font-size: 0.76rem;
  cursor: pointer;
  transition:
    border-color var(--dur-fast),
    color var(--dur-fast);
}
.motion-toggle:hover {
  border-color: rgba(255, 255, 255, 0.5);
  color: #fff;
}

@media (max-width: 980px) {
  .footer-grid {
    grid-template-columns: 1fr 1fr;
  }
}
@media (max-width: 560px) {
  .site-footer {
    padding-top: var(--space-7);
  }
  .footer-grid {
    grid-template-columns: 1fr;
    gap: var(--space-6);
  }
}
@media (prefers-reduced-motion: reduce) {
  .live-dot {
    animation: none;
  }
}
</style>
