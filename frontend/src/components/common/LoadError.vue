<script setup lang="ts">
import EmptyState from "@/components/common/EmptyState.vue";

withDefaults(defineProps<{ title?: string; message?: string; retrying?: boolean }>(), {
  title: "Impossible de charger ce contenu",
  message: "Vérifiez votre connexion internet puis réessayez. En cas d'urgence, appelez le 27 22 59 04 17.",
  retrying: false,
});

defineEmits<{ retry: [] }>();
</script>

<template>
  <div role="alert">
    <EmptyState icon="⚠️" :title="title" :message="message">
      <button type="button" class="load-error-retry" :disabled="retrying" @click="$emit('retry')">
        {{ retrying ? "Chargement…" : "Réessayer" }}
      </button>
    </EmptyState>
  </div>
</template>

<style scoped>
.load-error-retry {
  margin-top: 18px;
  padding: 10px 22px;
  border-radius: 6px;
  border: 1px solid var(--blue);
  background: transparent;
  color: var(--blue);
  font-weight: 600;
  font-size: 0.85rem;
  cursor: pointer;
  transition:
    background 0.2s,
    color 0.2s;
}
.load-error-retry:hover:not(:disabled) {
  background: var(--blue);
  color: #fff;
}
</style>
