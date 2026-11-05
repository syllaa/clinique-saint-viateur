<script setup lang="ts">
import Spinner from "@/components/common/Spinner.vue";

withDefaults(defineProps<{ message?: string }>(), {
  message: "Chargement…",
});
</script>

<template>
  <div class="loading-overlay">
    <Spinner :size="26" />
    <p>{{ message }}</p>
  </div>
</template>

<style scoped>
.loading-overlay {
  position: absolute;
  inset: 0;
  border-radius: 10px;
  background: color-mix(in srgb, var(--surface) 85%, transparent);
  backdrop-filter: blur(1.5px);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 10px;
  z-index: 5;
}
.loading-overlay p {
  font-size: 0.85rem;
  font-weight: 600;
  color: var(--heading);
}
</style>
