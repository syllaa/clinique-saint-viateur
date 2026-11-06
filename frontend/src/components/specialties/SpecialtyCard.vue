<script setup lang="ts">
import { RouterLink } from "vue-router";

import SpecialtyMedia from "@/components/specialties/SpecialtyMedia.vue";
import type { SpecialtyListItem } from "@/services/specialtyService";

defineProps<{ specialty: SpecialtyListItem }>();
</script>

<template>
  <!-- Reveal and tilt are applied by the parent list (v-reveal / v-tilt). -->
  <RouterLink :to="`/specialites/${specialty.slug}`" class="spc-card">
    <SpecialtyMedia
      class="spc-media"
      :media-type="specialty.media_type"
      :icon-name="specialty.icon_name"
      :image-url="specialty.cover_image_url"
      :image-alt="specialty.image_alt"
      :name="specialty.name"
    />
    <h3>{{ specialty.name }}</h3>
    <p>{{ specialty.description }}</p>
    <span class="spc-more">En savoir plus →</span>
  </RouterLink>
</template>

<style scoped>
.spc-card {
  display: block;
  background: var(--surface);
  border-radius: 13px;
  padding: 26px 20px;
  border: 1px solid var(--border-soft);
  text-decoration: none;
  color: inherit;
  transition:
    transform 0.35s cubic-bezier(0.22, 0.68, 0, 1.2),
    box-shadow 0.35s,
    border-color 0.35s;
}
/* Hover: lift + 3D tilt towards the cursor (variables set by v-tilt). */
.spc-card:hover {
  transform: perspective(900px) rotateX(var(--tilt-x, 0deg)) rotateY(var(--tilt-y, 0deg)) translateY(-7px);
  box-shadow: 0 18px 44px rgba(150, 12, 30, 0.11);
  border-color: #e8a8ae;
  transition:
    transform 0.15s linear,
    box-shadow 0.35s,
    border-color 0.35s;
  transition-delay: 0s;
}
.spc-card:hover :deep(.specialty-media.card:not(.is-image)) {
  transform: scale(1.12) rotate(-6deg);
  background: #fbe1e3;
}
.spc-card:hover :deep(.specialty-media.card:not(.is-image) svg) {
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
.spc-card h3 {
  font-family: var(--font-sans);
  font-size: 0.95rem;
  font-weight: 600;
  color: var(--heading);
  margin-bottom: 6px;
}
.spc-card p {
  font-size: 0.8rem;
  color: var(--muted);
  line-height: 1.6;
  margin-bottom: 14px;
}
.spc-more {
  font-size: 0.78rem;
  color: var(--blue);
  font-weight: 600;
  display: inline-flex;
  align-items: center;
  gap: 5px;
  transition: gap 0.2s;
}
.spc-card:hover .spc-more {
  gap: 9px;
}
</style>
