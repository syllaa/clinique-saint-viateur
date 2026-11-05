<script setup lang="ts">
import { RouterLink } from "vue-router";

defineProps<{ items: { label: string; to?: string }[] }>();
</script>

<template>
  <nav class="crumbs" aria-label="Fil d'Ariane">
    <template v-for="(item, i) in items" :key="i">
      <RouterLink v-if="item.to" :to="item.to" class="crumb-link">{{ item.label }}</RouterLink>
      <span v-else class="crumb-current">{{ item.label }}</span>
      <span v-if="i < items.length - 1" class="crumb-sep">/</span>
    </template>
  </nav>
</template>

<style scoped>
.crumbs {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 8px;
  font-size: 0.78rem;
  margin-bottom: 22px;
}
.crumb-link {
  color: var(--muted);
  text-decoration: none;
  transition: color 0.2s;
}
.crumb-link:hover {
  color: var(--blue);
}
.crumb-current {
  color: var(--heading);
  font-weight: 600;
}
.crumb-sep {
  color: var(--border-soft);
}
</style>
