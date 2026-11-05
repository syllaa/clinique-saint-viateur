<script setup lang="ts">
import { computed } from "vue";

const props = defineProps<{ page: number; total: number; pageSize: number }>();
const emit = defineEmits<{ (e: "update:page", page: number): void }>();

const totalPages = computed(() => Math.max(1, Math.ceil(props.total / props.pageSize)));

function go(p: number) {
  if (p < 1 || p > totalPages.value || p === props.page) return;
  emit("update:page", p);
}
</script>

<template>
  <nav v-if="totalPages > 1" class="pagination" aria-label="Pagination">
    <button class="page-btn" :disabled="page <= 1" @click="go(page - 1)">← Précédent</button>
    <span class="page-info">Page {{ page }} / {{ totalPages }}</span>
    <button class="page-btn" :disabled="page >= totalPages" @click="go(page + 1)">Suivant →</button>
  </nav>
</template>

<style scoped>
.pagination {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 16px;
  margin-top: 36px;
}
.page-btn {
  background: var(--surface);
  border: 1px solid var(--border-soft);
  color: var(--heading);
  padding: 9px 18px;
  border-radius: 6px;
  font-size: 0.82rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}
.page-btn:hover:not(:disabled) {
  border-color: var(--blue);
  color: var(--blue);
}
.page-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}
.page-info {
  font-size: 0.82rem;
  color: var(--muted);
}
</style>
