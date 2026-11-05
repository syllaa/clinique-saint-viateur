<script setup lang="ts">
import { computed, ref } from "vue";

import { ARTICLE_ICONS } from "@/constants/articleIcons";

defineProps<{ modelValue: string }>();
const emit = defineEmits<{ (e: "update:modelValue", value: string): void }>();

const search = ref("");

const filtered = computed(() => {
  const q = search.value.trim().toLowerCase();
  if (!q) return ARTICLE_ICONS;
  return ARTICLE_ICONS.filter((i) => i.label.toLowerCase().includes(q));
});

function select(emoji: string) {
  emit("update:modelValue", emoji);
}
</script>

<template>
  <div class="emoji-picker">
    <input v-model="search" type="text" class="emoji-search" placeholder="🔍 Rechercher une icône…" />
    <div class="emoji-grid">
      <button
        v-for="opt in filtered"
        :key="opt.emoji"
        type="button"
        class="emoji-tile"
        :class="{ selected: modelValue === opt.emoji }"
        :title="opt.label"
        @click="select(opt.emoji)"
      >
        <span class="emoji-tile-glyph">{{ opt.emoji }}</span>
        <span class="emoji-tile-label">{{ opt.label }}</span>
        <span v-if="modelValue === opt.emoji" class="emoji-tile-check">✓</span>
      </button>
    </div>
    <p v-if="!filtered.length" class="emoji-empty">Aucune icône trouvée pour « {{ search }} ».</p>
  </div>
</template>

<style scoped>
.emoji-picker {
  border: 1px solid var(--a-border);
  border-radius: 10px;
  padding: 14px;
  background: var(--a-tint);
  margin-bottom: 14px;
}
.emoji-search {
  width: 100%;
  padding: 10px 13px;
  background: var(--a-panel);
  border: 1px solid var(--a-border);
  border-radius: 7px;
  color: var(--a-text);
  font-size: 0.85rem;
  outline: none;
  margin-bottom: 12px;
}
.emoji-search:focus {
  border-color: var(--a-gold);
}
.emoji-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(88px, 1fr));
  gap: 8px;
}
.emoji-tile {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 5px;
  background: var(--a-panel);
  border: 1.5px solid var(--a-border);
  border-radius: 9px;
  padding: 12px 6px 8px;
  cursor: pointer;
  color: var(--a-text-2);
  transition: all 0.15s;
}
.emoji-tile:hover {
  border-color: rgba(224, 71, 90, 0.5);
  color: var(--a-text);
}
.emoji-tile.selected {
  border-color: var(--a-gold);
  background: rgba(224, 71, 90, 0.12);
  color: var(--a-gold);
}
.emoji-tile-glyph {
  font-size: 1.4rem;
  line-height: 1;
}
.emoji-tile-label {
  font-size: 0.62rem;
  text-align: center;
  line-height: 1.3;
}
.emoji-tile-check {
  position: absolute;
  top: 4px;
  right: 6px;
  color: var(--a-gold);
  font-size: 0.7rem;
  font-weight: 700;
}
.emoji-empty {
  font-size: 0.8rem;
  color: var(--a-muted);
  text-align: center;
  padding: 16px 0;
}
</style>
