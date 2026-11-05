<script setup lang="ts">
import { Gift, Search } from "@lucide/vue";
import { computed, onMounted, ref, watch } from "vue";

import EmptyState from "@/components/common/EmptyState.vue";
import FilterPills from "@/components/common/FilterPills.vue";
import LoadError from "@/components/common/LoadError.vue";
import PageHeader from "@/components/common/PageHeader.vue";
import Pagination from "@/components/common/Pagination.vue";
import SkeletonGrid from "@/components/common/SkeletonGrid.vue";
import PromotionCard from "@/components/promotions/PromotionCard.vue";
import { applySeo } from "@/composables/useHead";
import { scrollToHash } from "@/motion/useLenis";
import { usePromotionsStore } from "@/stores/promotions";

const promotions = usePromotionsStore();

const search = ref("");
const activeCategory = ref<string | null>(null);
const sort = ref<"date" | "popular">("date");
const loading = ref(true);
const loadError = ref(false);

const categoryOptions = computed(() => [
  { value: null, label: "Toutes" },
  ...promotions.categories.map((c) => ({ value: c as string | null, label: c })),
]);

let searchTimeout: ReturnType<typeof setTimeout> | undefined;

async function load(page = 1) {
  loading.value = true;
  loadError.value = false;
  try {
    await promotions.fetchAll({
      page,
      page_size: 12,
      search: search.value || undefined,
      category: activeCategory.value || undefined,
      sort: sort.value,
    });
  } catch {
    loadError.value = true;
  } finally {
    loading.value = false;
  }
}

onMounted(() => {
  // Category filters are optional: without them the list still works.
  promotions.fetchCategories().catch(() => undefined);
  load();
  applySeo({
    title: "Toutes nos offres – Clinique Saint Viateur",
    description: "Découvrez toutes les offres et promotions de la Clinique Médicale Saint Viateur à Cocody, Abidjan.",
    canonical: window.location.href,
  });
});

watch(search, () => {
  clearTimeout(searchTimeout);
  searchTimeout = setTimeout(() => load(1), 350);
});

watch([activeCategory, sort], () => load(1));

function onPageChange(page: number) {
  load(page);
  scrollToHash("#resultats");
}
</script>

<template>
  <PageHeader
    kicker="Nos offres"
    title="Toutes nos offres"
    lead="Consultez l'ensemble de nos offres et promotions, actives ou passées, et réagissez à celles qui vous intéressent."
    :crumbs="[{ label: 'Accueil', to: '/' }, { label: 'Nos offres' }]"
  />

  <section id="resultats" class="section list-section" aria-label="Offres">
    <div class="section-inner">
      <div class="list-toolbar">
        <label class="list-search">
          <Search :size="16" aria-hidden="true" />
          <span class="sr-only">Rechercher une offre</span>
          <input v-model="search" type="search" placeholder="Rechercher une offre…" />
        </label>
        <div class="promo-toolbar-row">
          <FilterPills v-model="activeCategory" :options="categoryOptions" label="Filtrer par catégorie" />
          <label class="promo-sort-label">
            <span class="sr-only">Trier les offres</span>
            <select v-model="sort" class="promo-sort">
              <option value="date">Plus récentes</option>
              <option value="popular">Plus populaires</option>
            </select>
          </label>
        </div>
      </div>

      <SkeletonGrid v-if="loading && !promotions.allItems.length" :count="6" :min-width="280" />
      <LoadError v-else-if="loadError" @retry="load()" />
      <template v-else-if="promotions.allItems.length">
        <div class="promo-grid" :class="{ 'is-refreshing': loading }" :aria-busy="loading">
          <PromotionCard
            v-for="(p, i) in promotions.allItems"
            :key="p.id"
            v-reveal="{ type: 'up', delay: (i % 4) * 80 }"
            :promotion="p"
          />
        </div>
        <Pagination
          :page="promotions.page"
          :total="promotions.total"
          :page-size="promotions.pageSize"
          @update:page="onPageChange"
        />
      </template>
      <EmptyState v-else :icon="Gift" title="Aucune offre trouvée" message="Essayez une autre recherche ou catégorie." />
    </div>
  </section>
</template>

<style scoped>
.list-section {
  background: var(--bg-alt);
  min-height: 50vh;
}
.list-toolbar {
  margin-bottom: 36px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}
.promo-toolbar-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 12px;
}
.promo-sort {
  padding: 9px 14px;
  border: 1px solid var(--border-soft);
  border-radius: var(--radius-pill);
  font-size: 0.82rem;
  background: var(--surface);
  color: var(--text);
  cursor: pointer;
}
.promo-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(min(280px, 100%), 1fr));
  gap: 22px;
  transition: opacity 0.3s;
}
.promo-grid.is-refreshing {
  opacity: 0.45;
  pointer-events: none;
}
</style>
