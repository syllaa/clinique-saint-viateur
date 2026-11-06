<script setup lang="ts">
import emblem128 from "@/assets/images/brand/emblem-128.webp";
import emblem256 from "@/assets/images/brand/emblem-256.webp";

/**
 * Clinic emblem (official logo supplied by the clinic): blue cross, white
 * figure and green swoosh. The artwork has a black, glowing background that
 * cannot be cut out cleanly, so it is shown as a rounded icon tile.
 */
withDefaults(defineProps<{ size?: number; title?: string }>(), {
  size: 38,
  title: undefined,
});
</script>

<template>
  <img
    class="brand-mark"
    :src="emblem128"
    :srcset="`${emblem128} 128w, ${emblem256} 256w`"
    :sizes="`${size}px`"
    :width="size"
    :height="size"
    :alt="title ?? ''"
    :aria-hidden="title ? undefined : 'true'"
    decoding="async"
    draggable="false"
  />
</template>

<style scoped>
.brand-mark {
  display: block;
  flex-shrink: 0;
  border-radius: 24%;
  background: #000;
  box-shadow: 0 0 0 1px rgba(255, 255, 255, 0.08);
}
</style>
