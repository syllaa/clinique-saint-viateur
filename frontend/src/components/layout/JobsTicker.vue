<script setup lang="ts">
import { onMounted } from "vue";

import { useJobOffersStore } from "@/stores/jobOffers";

const jobs = useJobOffersStore();

onMounted(() => {
  // Decorative ticker: on failure it just stays empty, never blocks the page.
  if (!jobs.items.length) jobs.fetchAll().catch(() => undefined);
});
</script>

<template>
  <div v-if="jobs.items.length" class="jobs-ticker" role="region" aria-label="Offres d'emploi en cours">
    <RouterLink to="/nous-rejoindre" class="jt-label">
      <span class="jt-dot" aria-hidden="true"></span>
      Nous recrutons
    </RouterLink>
    <div class="jt-track">
      <div class="jt-row" aria-hidden="true">
        <RouterLink
          v-for="(o, i) in [...jobs.items, ...jobs.items]"
          :key="`${o.id}-${i}`"
          :to="`/nous-rejoindre/offres/${o.slug}`"
          class="jt-item"
        >
          <span class="jt-title">{{ o.title }}</span>
          <span class="jt-sep">·</span>
          <span class="jt-meta">{{ o.contract_type }}</span>
          <span v-if="o.department" class="jt-sep">·</span>
          <span v-if="o.department" class="jt-meta">{{ o.department }}</span>
          <span class="jt-arrow">→</span>
        </RouterLink>
      </div>
    </div>
  </div>
</template>

<style scoped>
.jobs-ticker {
  position: fixed;
  top: 68px;
  left: 0;
  right: 0;
  z-index: 490;
  height: 30px;
  display: flex;
  align-items: stretch;
  background: linear-gradient(90deg, var(--navy) 0%, #8f1620 100%);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.15);
  overflow: hidden;
}
.jt-label {
  flex-shrink: 0;
  display: flex;
  align-items: center;
  gap: 7px;
  padding: 0 16px;
  background: var(--gold);
  color: #fff;
  font-size: 0.68rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.07em;
  text-decoration: none;
  white-space: nowrap;
}
.jt-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: #fff;
  animation: jtPulse 2.2s infinite;
}
@keyframes jtPulse {
  0% {
    box-shadow: 0 0 0 0 rgba(255, 255, 255, 0.6);
  }
  70% {
    box-shadow: 0 0 0 6px rgba(255, 255, 255, 0);
  }
  100% {
    box-shadow: 0 0 0 0 rgba(255, 255, 255, 0);
  }
}
.jt-track {
  flex: 1;
  overflow: hidden;
  position: relative;
}
.jt-row {
  display: flex;
  align-items: center;
  height: 100%;
  width: max-content;
  animation: jtScroll 28s linear infinite;
}
.jobs-ticker:hover .jt-row {
  animation-play-state: paused;
}
@keyframes jtScroll {
  0% {
    transform: translateX(0);
  }
  100% {
    transform: translateX(-50%);
  }
}
.jt-item {
  display: inline-flex;
  align-items: center;
  gap: 7px;
  padding: 0 22px;
  height: 100%;
  color: rgba(255, 255, 255, 0.88);
  text-decoration: none;
  font-size: 0.72rem;
  white-space: nowrap;
  transition: color 0.2s;
}
.jt-item:hover {
  color: #fff;
}
.jt-item:hover .jt-title {
  text-decoration: underline;
}
.jt-title {
  font-weight: 700;
}
.jt-sep {
  opacity: 0.4;
}
.jt-meta {
  opacity: 0.75;
}
.jt-arrow {
  opacity: 0.6;
  transition: transform 0.2s;
}
.jt-item:hover .jt-arrow {
  transform: translateX(3px);
  opacity: 1;
}

@media (prefers-reduced-motion: reduce) {
  .jt-dot {
    animation: none;
  }
  .jt-row {
    animation: none;
    overflow-x: auto;
  }
}

@media (max-width: 640px) {
  .jt-label span:not(.jt-dot) {
    display: none;
  }
  .jt-label {
    padding: 0 12px;
  }
  .jt-item {
    padding: 0 16px;
    font-size: 0.68rem;
  }
}
</style>
