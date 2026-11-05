<script setup lang="ts">
withDefaults(defineProps<{ size?: number }>(), { size: 16 });
</script>

<template>
  <span class="sv-spinner" :style="{ width: size + 'px', height: size + 'px' }" aria-hidden="true"></span>
</template>

<style scoped>
.sv-spinner {
  display: inline-block;
  flex-shrink: 0;
  border: 2px solid currentColor;
  border-top-color: transparent;
  border-radius: 50%;
  opacity: 0.75;
  animation: sv-spin 0.7s linear infinite;
}

@keyframes sv-spin {
  to {
    transform: rotate(360deg);
  }
}
</style>
