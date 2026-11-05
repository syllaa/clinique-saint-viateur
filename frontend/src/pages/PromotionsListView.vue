<script setup lang="ts">
import { Gift } from "@lucide/vue";
import { onMounted, ref, watch } from "vue";

import Breadcrumbs from "@/components/common/Breadcrumbs.vue";
import EmptyState from "@/components/common/EmptyState.vue";
import LoadError from "@/components/common/LoadError.vue";
import Pagination from "@/components/common/Pagination.vue";
import Spinner from "@/components/common/Spinner.vue";
import PromotionCard from "@/components/promotions/PromotionCard.vue";
import { applySeo } from "@/composables/useHead";
import { usePromotionsStore } from "@/stores/promotions";

const promotions = usePromotionsStore();

const search = ref("");
const activeCategory = ref<string | null>(null);
const sort = ref<"date" | "popular">("date");
const loading = ref(true);
const loadError = ref(false);

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

function selectCategory(category: string | null) {
  activeCategory.value = category;
  load(1);
}

function onSortChange() {
  load(1);
}

function onPageChange(page: number) {
  load(page);
  window.scrollTo({ top: 0, behavior: "smooth" });
}
</script>

<template>

  <section class="section promo-hero">
    <div class="section-inner">
      <Breadcrumbs :items="[{ label: 'Accueil', to: '/' }, { label: 'Nos offres' }]" />
      <p v-reveal class="section-kicker">Nos offres</p>
      <h1 v-reveal class="section-title d1">Toutes nos offres</h1>
      <p v-reveal class="section-lead d2">
        Consultez l'ensemble de nos offres et promotions, actives ou passées, et réagissez à celles qui vous
        intéressent.
      </p>

      <div class="promo-toolbar">
        <input v-model="search" type="search" placeholder="Rechercher une offre…" class="promo-search" />
        <div class="promo-toolbar-row">
          <div class="promo-cats">
            <button class="cat-pill" :class="{ on: activeCategory === null }" @click="selectCategory(null)">
              Toutes
            </button>
            <button
              v-for="c in promotions.categories"
              :key="c"
              class="cat-pill"
              :class="{ on: activeCategory === c }"
              @click="selectCategory(c)"
            >
              {{ c }}
            </button>
          </div>
          <select v-model="sort" class="promo-sort" @change="onSortChange">
            <option value="date">Plus récentes</option>
            <option value="popular">Plus populaires</option>
          </select>
        </div>
      </div>

      <div v-if="loading" class="promo-loading"><Spinner :size="26" /></div>
      <LoadError v-else-if="loadError" @retry="load()" />
      <template v-else-if="promotions.allItems.length">
        <div class="promo-grid">
          <PromotionCard v-for="p in promotions.allItems" :key="p.id" :promotion="p" />
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
.promo-hero {
  padding-top: 128px;
  background: var(--bg-alt);
  min-height: 60vh;
}
.promo-toolbar {
  margin-bottom: 32px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}
.promo-search {
  width: 100%;
  max-width: 420px;
  padding: 12px 16px;
  border: 1px solid var(--border-soft);
  border-radius: 8px;
  font-size: 0.88rem;
  background: var(--surface);
  color: var(--text);
  outline: none;
  transition: border-color 0.2s;
}
.promo-search:focus {
  border-color: var(--blue);
}
.promo-toolbar-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 12px;
}
.promo-cats {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}
.cat-pill {
  background: var(--surface);
  border: 1px solid var(--border-soft);
  color: var(--muted);
  padding: 7px 15px;
  border-radius: 100px;
  font-size: 0.78rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}
.cat-pill:hover {
  border-color: var(--blue);
  color: var(--blue);
}
.cat-pill.on {
  background: var(--blue);
  border-color: var(--blue);
  color: #fff;
}
.promo-sort {
  padding: 9px 14px;
  border: 1px solid var(--border-soft);
  border-radius: 8px;
  font-size: 0.82rem;
  background: var(--surface);
  color: var(--text);
  cursor: pointer;
}
.promo-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 22px;
}
.promo-loading {
  display: flex;
  justify-content: center;
  padding: 60px 0;
}
</style>
