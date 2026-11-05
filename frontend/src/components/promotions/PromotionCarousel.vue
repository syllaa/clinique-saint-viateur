<script setup lang="ts">
import { ref } from "vue";

import PromotionCard from "@/components/promotions/PromotionCard.vue";
import type { PromotionListItem } from "@/services/promotionService";

defineProps<{ items: PromotionListItem[] }>();

const trackRef = ref<HTMLElement | null>(null);

function scrollByCard(direction: 1 | -1) {
  const track = trackRef.value;
  if (!track) return;
  const card = track.querySelector<HTMLElement>(".promo-slide");
  const amount = (card?.offsetWidth ?? 300) + 20;
  track.scrollBy({ left: amount * direction, behavior: "smooth" });
}
</script>

<template>
  <div class="promo-carousel">
    <button
      type="button"
      class="promo-nav prev"
      aria-label="Offres précédentes"
      @click="scrollByCard(-1)"
    >
      ←
    </button>
    <div ref="trackRef" class="promo-track">
      <div v-for="p in items" :key="p.id" class="promo-slide">
        <PromotionCard :promotion="p" />
      </div>
    </div>
    <button type="button" class="promo-nav next" aria-label="Offres suivantes" @click="scrollByCard(1)">→</button>
  </div>
</template>

<style scoped>
.promo-carousel {
  position: relative;
  display: flex;
  align-items: center;
  gap: 12px;
}
.promo-track {
  display: flex;
  gap: 20px;
  overflow-x: auto;
  scroll-snap-type: x mandatory;
  scroll-padding: 0 4px;
  padding: 6px 4px 6px;
  scrollbar-width: none;
  -ms-overflow-style: none;
}
.promo-track::-webkit-scrollbar {
  display: none;
}
.promo-slide {
  flex: 0 0 300px;
  scroll-snap-align: start;
}
.promo-nav {
  flex-shrink: 0;
  width: 44px;
  height: 44px;
  border-radius: 50%;
  background: var(--surface);
  border: 1px solid var(--border-soft);
  color: var(--heading);
  font-size: 1.1rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition:
    background 0.2s,
    border-color 0.2s,
    transform 0.15s;
}
.promo-nav:hover {
  border-color: var(--blue);
  color: var(--blue);
}
.promo-nav:active {
  transform: scale(0.92);
}

@media (max-width: 640px) {
  .promo-nav {
    display: none;
  }
  .promo-slide {
    flex-basis: 82vw;
  }
}
</style>
