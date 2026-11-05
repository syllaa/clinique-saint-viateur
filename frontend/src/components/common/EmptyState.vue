<script setup lang="ts">
withDefaults(defineProps<{ icon?: string; title: string; message?: string }>(), {
  icon: "🔍",
});
</script>

<template>
  <div class="empty-state">
    <div class="empty-icon">{{ icon }}</div>
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
  font-size: 2.4rem;
  margin-bottom: 14px;
  opacity: 0.6;
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
