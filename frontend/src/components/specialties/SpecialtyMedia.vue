<script setup lang="ts">
import { computed } from "vue";

import { resolveSpecialtyIcon } from "@/constants/specialtyIcons";
import { mediaUrl } from "@/services/api";

const props = withDefaults(
  defineProps<{
    mediaType: string;
    iconName?: string | null;
    imageUrl?: string | null;
    imageAlt?: string | null;
    name: string;
    size?: "card" | "hero";
  }>(),
  { size: "card" },
);

// Never render both at once: media_type is the single source of truth, and an
// "image" type without an actual URL still falls back to the icon so the UI
// never shows a broken image box.
const isImage = computed(() => props.mediaType === "image" && !!props.imageUrl);
const icon = computed(() => resolveSpecialtyIcon(props.iconName));
</script>

<template>
  <div class="specialty-media" :class="[size, { 'is-image': isImage }]">
    <img v-if="isImage" :src="mediaUrl(imageUrl)!" :alt="imageAlt || name" />
    <component :is="icon.component" v-else :size="size === 'hero' ? 40 : 24" :stroke-width="1.75" />
  </div>
</template>

<style scoped>
.specialty-media {
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

/* Card variant: small rounded icon box (matches the existing card language),
   or a wider inset image thumbnail when an image is used. */
.specialty-media.card {
  width: 50px;
  height: 50px;
  border-radius: 11px;
  background: var(--bg-alt);
  color: var(--blue);
  margin-bottom: 15px;
  transition:
    transform 0.35s,
    background 0.3s;
}
.specialty-media.card.is-image {
  width: 100%;
  height: 140px;
  border-radius: 11px;
  overflow: hidden;
  background: var(--bg-alt);
}
.specialty-media.card img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
  transition: transform 0.55s cubic-bezier(0.22, 0.68, 0, 1);
}
.specialty-media.card.is-image:hover img {
  transform: scale(1.09);
}

/* Hero variant: large header media on the specialty detail page. */
.specialty-media.hero {
  width: 92px;
  height: 92px;
  border-radius: 22px;
  background: rgba(255, 255, 255, 0.1);
  color: #fff;
  margin-bottom: 18px;
}
.specialty-media.hero.is-image {
  width: 100%;
  max-width: 480px;
  height: 260px;
  border-radius: 18px;
  overflow: hidden;
}
.specialty-media.hero img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}
</style>
