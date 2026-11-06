<script setup lang="ts">
/**
 * Placeholder cards shown while a list loads. They occupy the same space as
 * the real grid, so nothing jumps when the data arrives (CLS), and a soft
 * shimmer tells the visitor something is coming.
 */
withDefaults(defineProps<{ count?: number; minWidth?: number; media?: boolean }>(), {
  count: 6,
  minWidth: 300,
  media: true,
});
</script>

<template>
  <div class="sk-grid" :style="{ '--sk-min': `${minWidth}px` }" role="status" aria-live="polite">
    <span class="sr-only">Chargement…</span>
    <div v-for="n in count" :key="n" class="sk-card" aria-hidden="true">
      <div v-if="media" class="sk-media sk-shimmer"></div>
      <div class="sk-body">
        <div class="sk-line sk-shimmer" style="width: 35%"></div>
        <div class="sk-line sk-line-lg sk-shimmer" style="width: 85%"></div>
        <div class="sk-line sk-shimmer" style="width: 95%"></div>
        <div class="sk-line sk-shimmer" style="width: 70%"></div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.sk-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(min(var(--sk-min), 100%), 1fr));
  gap: 22px;
}
.sk-card {
  background: var(--surface);
  border: 1px solid var(--border-soft);
  border-radius: var(--radius-lg);
  overflow: hidden;
}
.sk-media {
  aspect-ratio: 16 / 10;
}
.sk-body {
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.sk-line {
  height: 10px;
  border-radius: 5px;
}
.sk-line-lg {
  height: 16px;
  margin-bottom: 4px;
}
.sk-shimmer {
  background: linear-gradient(100deg, var(--bg-alt) 30%, var(--border-soft) 50%, var(--bg-alt) 70%);
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
</style>
