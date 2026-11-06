<script setup lang="ts">
import { Clock, MapPin, Siren, Trophy } from "@lucide/vue";

const ITEMS = [
  { icon: Clock, text: "Lun – Ven : 08h–20h" },
  { icon: Clock, text: "Samedi : 08h–12h" },
  { icon: Siren, text: "Urgences 24h/24 · 7j/7" },
  { icon: MapPin, text: "Riviera Sideci, Cocody – Abidjan" },
  { icon: Trophy, text: "3ᵉ Prix national d'excellence médicale" },
];
</script>

<template>
  <!-- Endless marquee: the list is rendered twice and the track slides by
       exactly one copy. The copy is hidden from assistive tech. Pauses on
       hover/focus; static and wrapped under reduced motion. -->
  <section class="strip" aria-label="Informations pratiques">
    <div class="strip-track">
      <ul v-for="copy in 2" :key="copy" class="strip-group" :aria-hidden="copy === 2 ? 'true' : undefined">
        <li v-for="item in ITEMS" :key="item.text" class="strip-item">
          <component :is="item.icon" :size="16" aria-hidden="true" />
          {{ item.text }}
          <span class="strip-sep" aria-hidden="true">✚</span>
        </li>
      </ul>
    </div>
  </section>
</template>

<style scoped>
.strip {
  background: var(--brand-600);
  overflow: hidden;
  padding: 15px 0;
  mask-image: linear-gradient(90deg, transparent, black 6%, black 94%, transparent);
}
.strip-track {
  display: flex;
  width: max-content;
  animation: marquee 38s linear infinite;
}
.strip:hover .strip-track,
.strip:focus-within .strip-track {
  animation-play-state: paused;
}
.strip-group {
  display: flex;
  list-style: none;
  flex-shrink: 0;
}
.strip-item {
  display: flex;
  align-items: center;
  gap: 9px;
  color: rgba(255, 255, 255, 0.92);
  font-size: 0.84rem;
  white-space: nowrap;
  padding-left: 30px;
}
.strip-sep {
  margin-left: 30px;
  font-size: 0.6rem;
  opacity: 0.45;
}
@keyframes marquee {
  to {
    transform: translateX(-50%);
  }
}

/* Reduced motion: no movement, one copy, wrapped and centred. */
:root[data-motion="reduce"] .strip {
  mask-image: none;
  padding: 14px 5vw;
}
:root[data-motion="reduce"] .strip-track {
  animation: none;
  width: auto;
  justify-content: center;
}
:root[data-motion="reduce"] .strip-group {
  flex-wrap: wrap;
  flex-shrink: 1;
  width: 100%;
  justify-content: center;
  gap: 8px 28px;
}
:root[data-motion="reduce"] .strip-item {
  padding-left: 0;
  white-space: normal;
}
:root[data-motion="reduce"] .strip-group[aria-hidden="true"],
:root[data-motion="reduce"] .strip-sep {
  display: none;
}
</style>
