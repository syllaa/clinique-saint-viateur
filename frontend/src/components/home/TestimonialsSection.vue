<script setup lang="ts">
import { Quote } from "@lucide/vue";

import { TESTIMONIALS as testimonials } from "@/constants/testimonials";

const starCount = (stars: string) => [...stars].filter((c) => c === "★").length;
</script>

<template>
  <section id="temoignages" class="section" aria-labelledby="testi-title">
    <div class="section-inner">
      <p v-reveal class="section-kicker">Avis de nos patients</p>
      <h2 id="testi-title" v-reveal="'words'" class="section-title d1">Ils nous font confiance</h2>
      <p v-reveal class="section-lead d2">
        La satisfaction de nos patients est notre première récompense. Voici quelques témoignages partagés par nos
        patients sur Facebook et lors de leur passage.
      </p>
      <ul class="testi-grid">
        <li
          v-for="(t, i) in testimonials"
          :key="t.author"
          v-reveal="{ type: 'up', delay: (i % 4) * 90 }"
          class="testi-card"
        >
          <Quote class="quote-mark" :size="44" aria-hidden="true" />
          <!-- Stars fill one by one once the card is revealed. -->
          <p class="testi-stars" role="img" :aria-label="`Note : ${starCount(t.stars)} sur 5`">
            <span v-for="n in 5" :key="n" class="star" :class="{ on: n <= starCount(t.stars) }" :style="{ '--n': n }" aria-hidden="true">★</span>
          </p>
          <blockquote class="testi-text">{{ t.text }}</blockquote>
          <p class="testi-author">{{ t.author }}</p>
          <p class="testi-meta">{{ t.meta }}</p>
        </li>
      </ul>
    </div>
  </section>
</template>

<style scoped>
.testi-grid {
  list-style: none;
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 20px;
}
.testi-card {
  background: var(--surface);
  border: 1px solid var(--border-soft);
  border-radius: var(--radius-lg);
  padding: 26px 24px;
  position: relative;
  display: flex;
  flex-direction: column;
  transition:
    translate 0.35s var(--ease-out),
    box-shadow 0.35s,
    border-color 0.35s;
}
.testi-card:hover {
  translate: 0 -4px;
  box-shadow: var(--shadow-md);
  border-color: #e8a8ae;
}
.quote-mark {
  position: absolute;
  top: 18px;
  right: 18px;
  color: var(--brand-100);
  pointer-events: none;
}
.testi-stars {
  font-size: 1.05rem;
  margin-bottom: 12px;
  letter-spacing: 2px;
}
.star {
  color: var(--border-soft);
  display: inline-block;
}
.star.on {
  color: var(--brand-600);
  transform: scale(0.4);
  opacity: 0;
  transition:
    transform 0.45s cubic-bezier(0.34, 1.56, 0.64, 1),
    opacity 0.3s;
  transition-delay: calc(var(--rv-delay, 0ms) + 300ms + var(--n) * 90ms);
}
.testi-card.vis .star.on {
  transform: none;
  opacity: 1;
}
.testi-text {
  font-size: 0.88rem;
  color: var(--muted);
  line-height: 1.75;
  margin-bottom: 16px;
  font-style: italic;
  flex: 1;
}
.testi-author {
  font-size: 0.84rem;
  font-weight: 600;
  color: var(--heading);
}
.testi-meta {
  font-size: 0.72rem;
  color: var(--muted);
  margin-top: 2px;
}
:root[data-motion="reduce"] .star.on {
  transform: none;
  opacity: 1;
}
</style>
