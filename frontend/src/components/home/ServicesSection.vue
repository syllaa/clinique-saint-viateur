<script setup lang="ts">
import { onMounted, ref } from "vue";

import LoadError from "@/components/common/LoadError.vue";
import SpecialtyMedia from "@/components/specialties/SpecialtyMedia.vue";
import { vTilt } from "@/directives/tilt";
import { useSpecialtiesStore } from "@/stores/specialties";

const specialties = useSpecialtiesStore();
const loadError = ref(false);
const retrying = ref(false);
const loading = ref(!specialties.items.length);

async function load() {
  loadError.value = false;
  retrying.value = true;
  try {
    await specialties.fetchAll();
  } catch {
    loadError.value = true;
  } finally {
    retrying.value = false;
    loading.value = false;
  }
}

onMounted(load);
</script>

<template>
  <section id="services" class="section" aria-labelledby="services-title">
    <div class="section-inner">
      <p v-reveal class="section-kicker">Nos spécialités</p>
      <h2 id="services-title" v-reveal="'words'" class="section-title d1">Une gamme complète de soins médicaux</h2>
      <p v-reveal class="section-lead d2">
        De la médecine générale aux spécialités les plus pointues, la Clinique Saint Viateur vous accueille avec un
        plateau technique complet et des médecins qualifiés.
      </p>

      <!-- Skeletons reserve the grid's height while the API answers (no layout shift). -->
      <div v-if="loading" class="svc-grid" aria-hidden="true">
        <div v-for="n in 8" :key="n" class="svc-card svc-skeleton"></div>
      </div>
      <div v-else class="svc-grid">
        <RouterLink
          v-for="(s, i) in specialties.items"
          :key="s.id"
          v-reveal="{ type: 'up', delay: (i % 5) * 70 }"
          v-tilt
          :to="`/specialites/${s.slug}`"
          class="svc-card"
        >
          <SpecialtyMedia
            class="svc-icon"
            :media-type="s.media_type"
            :icon-name="s.icon_name"
            :image-url="s.cover_image_url"
            :image-alt="s.image_alt"
            :name="s.name"
          />
          <h3>{{ s.name }}</h3>
          <p>{{ s.description }}</p>
          <span class="svc-link" aria-hidden="true">Découvrir →</span>
        </RouterLink>
      </div>
      <LoadError
        v-if="loadError && !specialties.items.length"
        title="Impossible de charger nos spécialités"
        :retrying="retrying"
        @retry="load"
      />
      <div class="section-more">
        <RouterLink to="/specialites" class="btn-outline">Voir toutes nos spécialités →</RouterLink>
      </div>
    </div>
  </section>
</template>

<style scoped>
#services {
  background: var(--bg);
}
.svc-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(205px, 1fr));
  gap: 16px;
  perspective: 1000px;
}
.svc-card {
  --tilt-x: 0deg;
  --tilt-y: 0deg;
  --tilt-active: 0;
  position: relative;
  display: flex;
  flex-direction: column;
  background: var(--surface);
  border-radius: var(--radius-lg);
  padding: 24px 20px 20px;
  border: 1px solid var(--border-soft);
  text-decoration: none;
  color: inherit;
  overflow: hidden;
  transform-style: preserve-3d;
  transition:
    box-shadow 0.35s,
    border-color 0.35s;
}
/* Hover: 3D tilt (transform, driven by v-tilt) + lift (independent
   `translate` property). Short, delay-free transitions so the tilt tracks
   the cursor instead of inheriting the reveal's slow spring and stagger. */
.svc-card:hover {
  transform: perspective(900px) rotateX(var(--tilt-x)) rotateY(var(--tilt-y));
  translate: 0 -6px;
  box-shadow: var(--shadow-lg);
  border-color: #e8a8ae;
  transition:
    transform 0.12s linear,
    translate 0.35s var(--ease-out),
    box-shadow 0.35s,
    border-color 0.35s;
  transition-delay: 0s;
}
/* Soft light that follows the cursor. */
.svc-card::after {
  content: "";
  position: absolute;
  inset: 0;
  border-radius: inherit;
  pointer-events: none;
  background: radial-gradient(
    circle at var(--glare-x, 50%) var(--glare-y, 0%),
    rgba(255, 255, 255, 0.55),
    transparent 55%
  );
  opacity: calc(var(--tilt-active) * 0.6);
  transition: opacity 0.3s;
  mix-blend-mode: soft-light;
}
.svc-card:hover .svc-icon:not(.is-image) {
  transform: scale(1.12) rotate(-6deg);
  background: var(--brand-100);
}
/* Icon "heartbeat" while the card is hovered (double beat, then rest). */
.svc-card:hover .svc-icon:not(.is-image) :deep(svg) {
  animation: iconBeat 1.2s ease-in-out infinite;
}
@keyframes iconBeat {
  0%,
  40%,
  100% {
    scale: 1;
  }
  10%,
  28% {
    scale: 1.18;
  }
  18% {
    scale: 0.96;
  }
}
.svc-card.rv.vis .svc-icon {
  animation: iconPop 0.6s cubic-bezier(0.34, 1.56, 0.64, 1) calc(var(--rv-delay, 0ms) + 0.15s) backwards;
}
@keyframes iconPop {
  0% {
    transform: scale(0.4) rotate(-14deg);
    opacity: 0;
  }
  100% {
    transform: scale(1) rotate(0);
    opacity: 1;
  }
}
.svc-card h3 {
  font-family: "DM Sans", sans-serif;
  font-size: 0.94rem;
  font-weight: 600;
  color: var(--heading);
  margin-bottom: 6px;
}
.svc-card p {
  font-size: 0.79rem;
  color: var(--muted);
  line-height: 1.6;
  flex: 1;
}
.svc-link {
  margin-top: 12px;
  font-size: 0.76rem;
  font-weight: 600;
  color: var(--blue);
  opacity: 0;
  translate: -6px 0;
  transition:
    opacity 0.3s,
    translate 0.3s var(--ease-out);
}
.svc-card:hover .svc-link,
.svc-card:focus-visible .svc-link {
  opacity: 1;
  translate: 0 0;
}
.svc-skeleton {
  min-height: 230px;
  background: linear-gradient(100deg, var(--surface) 30%, var(--bg-alt) 50%, var(--surface) 70%);
  background-size: 300% 100%;
  animation: shimmer 1.4s linear infinite;
}
@keyframes shimmer {
  from {
    background-position: 100% 0;
  }
  to {
    background-position: 0 0;
  }
}
@media (max-width: 640px) {
  .svc-grid {
    grid-template-columns: 1fr 1fr;
    gap: 10px;
  }
  .svc-card {
    padding: 18px 14px 14px;
  }
  .svc-link {
    display: none;
  }
}
@media (max-width: 380px) {
  .svc-grid {
    grid-template-columns: 1fr;
  }
}
</style>
