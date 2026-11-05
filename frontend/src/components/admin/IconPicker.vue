<script setup lang="ts">
import { computed, ref, watch } from "vue";
import type { Component } from "vue";

import { ICON_CATEGORIES, SPECIALTY_ICONS } from "@/constants/specialtyIcons";

const props = defineProps<{ modelValue: string | null }>();
const emit = defineEmits<{ (e: "update:modelValue", value: string): void }>();

const search = ref("");
const activeCategory = ref<string | null>(null);
const extraResults = ref<{ name: string; label: string; component: Component }[]>([]);
const searching = ref(false);

const filteredCurated = computed(() => {
  const q = search.value.trim().toLowerCase();
  return SPECIALTY_ICONS.filter((icon) => {
    const matchesCategory = !activeCategory.value || icon.category === activeCategory.value;
    const matchesSearch = !q || icon.label.toLowerCase().includes(q) || icon.name.includes(q);
    return matchesCategory && matchesSearch;
  });
});

function pascalToKebab(value: string): string {
  return value.replace(/([a-z0-9])([A-Z])/g, "$1-$2").toLowerCase();
}

let searchTimeout: ReturnType<typeof setTimeout> | undefined;

// The curated grid above covers the common medical set; for anything more
// specific, fall back to searching the full Lucide catalog on demand (lazy
// import so it never weighs on the initial bundle) — satisfies "si la
// bibliothèque possède suffisamment d'icônes, permettre de rechercher parmi
// toutes les icônes disponibles."
watch(search, (value) => {
  clearTimeout(searchTimeout);
  extraResults.value = [];
  const q = value.trim().toLowerCase();
  if (q.length < 3 || filteredCurated.value.length >= 6) return;
  searchTimeout = setTimeout(async () => {
    searching.value = true;
    try {
      const mod = await import("@lucide/vue");
      const seen = new Set(SPECIALTY_ICONS.map((i) => i.name));
      const results: { name: string; label: string; component: Component }[] = [];
      for (const [exportName, exportValue] of Object.entries(mod)) {
        if (!/^[A-Z]/.test(exportName) || exportName.endsWith("Icon") || exportName === "Icon") continue;
        const kebab = pascalToKebab(exportName);
        if (seen.has(kebab) || !kebab.includes(q)) continue;
        results.push({ name: kebab, label: exportName, component: exportValue as Component });
        seen.add(kebab);
        if (results.length >= 24) break;
      }
      extraResults.value = results;
    } finally {
      searching.value = false;
    }
  }, 300);
});

function select(name: string) {
  emit("update:modelValue", name);
}
</script>

<template>
  <div class="icon-picker">
    <input v-model="search" type="text" class="icon-search" placeholder="🔍 Rechercher une icône…" />
    <div class="icon-cats">
      <button type="button" class="cat-pill" :class="{ on: activeCategory === null }" @click="activeCategory = null">
        Toutes
      </button>
      <button
        v-for="c in ICON_CATEGORIES"
        :key="c"
        type="button"
        class="cat-pill"
        :class="{ on: activeCategory === c }"
        @click="activeCategory = activeCategory === c ? null : c"
      >
        {{ c }}
      </button>
    </div>

    <div class="icon-grid">
      <button
        v-for="icon in filteredCurated"
        :key="icon.name"
        type="button"
        class="icon-tile"
        :class="{ selected: modelValue === icon.name }"
        :title="icon.label"
        @click="select(icon.name)"
      >
        <component :is="icon.component" :size="22" />
        <span class="icon-tile-label">{{ icon.label }}</span>
        <span v-if="modelValue === icon.name" class="icon-tile-check">✓</span>
      </button>
    </div>

    <div v-if="searching" class="icon-searching">Recherche…</div>
    <template v-if="extraResults.length">
      <div class="icon-more-label">Plus d'icônes</div>
      <div class="icon-grid">
        <button
          v-for="icon in extraResults"
          :key="icon.name"
          type="button"
          class="icon-tile"
          :class="{ selected: modelValue === icon.name }"
          :title="icon.label"
          @click="select(icon.name)"
        >
          <component :is="icon.component" :size="22" />
          <span class="icon-tile-label">{{ icon.label }}</span>
          <span v-if="modelValue === icon.name" class="icon-tile-check">✓</span>
        </button>
      </div>
    </template>

    <p v-if="!filteredCurated.length && !extraResults.length && !searching" class="icon-empty">
      Aucune icône trouvée pour « {{ search }} ».
    </p>
  </div>
</template>

<style scoped>
.icon-picker {
  border: 1px solid var(--a-border);
  border-radius: 10px;
  padding: 14px;
  background: var(--a-tint);
  margin-bottom: 14px;
}
.icon-search {
  width: 100%;
  padding: 10px 13px;
  background: var(--a-panel);
  border: 1px solid var(--a-border);
  border-radius: 7px;
  color: var(--a-text);
  font-size: 0.85rem;
  outline: none;
  margin-bottom: 10px;
}
.icon-search:focus {
  border-color: var(--a-gold);
}
.icon-cats {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  margin-bottom: 14px;
}
.cat-pill {
  background: var(--a-panel);
  border: 1px solid var(--a-border);
  color: var(--a-text-3);
  padding: 5px 12px;
  border-radius: 100px;
  font-size: 0.7rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}
.cat-pill:hover {
  color: var(--a-text);
}
.cat-pill.on {
  background: var(--a-gold);
  border-color: var(--a-gold);
  color: #fff;
}
.icon-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(96px, 1fr));
  gap: 8px;
}
.icon-tile {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
  background: var(--a-panel);
  border: 1.5px solid var(--a-border);
  border-radius: 9px;
  padding: 12px 6px 8px;
  cursor: pointer;
  color: var(--a-text-2);
  transition: all 0.15s;
}
.icon-tile:hover {
  border-color: rgba(224, 71, 90, 0.5);
  color: var(--a-text);
}
.icon-tile.selected {
  border-color: var(--a-gold);
  background: rgba(224, 71, 90, 0.12);
  color: var(--a-gold);
}
.icon-tile-label {
  font-size: 0.62rem;
  text-align: center;
  line-height: 1.3;
}
.icon-tile-check {
  position: absolute;
  top: 4px;
  right: 6px;
  color: var(--a-gold);
  font-size: 0.7rem;
  font-weight: 700;
}
.icon-searching {
  font-size: 0.76rem;
  color: var(--a-muted);
  margin-top: 10px;
}
.icon-more-label {
  font-size: 0.62rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--a-muted);
  margin: 14px 0 8px;
}
.icon-empty {
  font-size: 0.8rem;
  color: var(--a-muted);
  text-align: center;
  padding: 16px 0;
}
</style>
