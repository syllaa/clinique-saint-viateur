<script setup lang="ts">
import { SearchX } from "@lucide/vue";
import type { Component } from "vue";

/** `icon` is a Lucide icon component (preferred). A plain string (emoji) is still accepted. */
withDefaults(defineProps<{ icon?: Component | string; title: string; message?: string }>(), {
  icon: () => SearchX,
  message: undefined,
});
</script>

<template>
  <div class="empty-state">
    <div class="empty-icon" aria-hidden="true">
      <template v-if="typeof icon === 'string'">{{ icon }}</template>
      <component :is="icon" v-else :size="40" :stroke-width="1.5" />
    </div>
    <h3>{{ title }}</h3>
    <p v-if="message">{{ message }}</p>
    <slot />
  </div>
</template>

<style scoped>
.empty-state {
  text-align: center;
  padding: 56px 20px;
  color: var(--muted);
}
.empty-icon {
  display: flex;
  justify-content: center;
  font-size: 2.4rem;
  margin-bottom: 14px;
  color: var(--brand-400);
  opacity: 0.8;
}
.empty-state h3 {
  font-size: 1.05rem;
  color: var(--heading);
  margin-bottom: 8px;
}
.empty-state p {
  font-size: 0.86rem;
  max-width: 380px;
  margin: 0 auto;
  line-height: 1.6;
}
</style>
