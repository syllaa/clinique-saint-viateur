<script setup lang="ts">
import { Newspaper, Search } from "@lucide/vue";
import { computed, onMounted, ref, watch } from "vue";

import BlogCard from "@/components/blog/BlogCard.vue";
import EmptyState from "@/components/common/EmptyState.vue";
import FilterPills from "@/components/common/FilterPills.vue";
import LoadError from "@/components/common/LoadError.vue";
import PageHeader from "@/components/common/PageHeader.vue";
import Pagination from "@/components/common/Pagination.vue";
import SkeletonGrid from "@/components/common/SkeletonGrid.vue";
import { applySeo } from "@/composables/useHead";
import { scrollToHash } from "@/motion/useLenis";
import { useArticlesStore } from "@/stores/articles";
import { useBlogCategoriesStore } from "@/stores/blogCategories";

const articles = useArticlesStore();
const categories = useBlogCategoriesStore();

const search = ref("");
const activeCategory = ref<string | null>(null);
const loading = ref(true);
const loadError = ref(false);

const categoryOptions = computed(() => [
  { value: null, label: "Tous" },
  ...categories.items.map((c) => ({ value: c.slug as string | null, label: c.name })),
]);

let searchTimeout: ReturnType<typeof setTimeout> | undefined;

async function load(page = 1) {
  loading.value = true;
  loadError.value = false;
  try {
    await articles.fetchPublished({
      page,
      page_size: 9,
      search: search.value || undefined,
      category: activeCategory.value || undefined,
    });
  } catch {
    loadError.value = true;
  } finally {
    loading.value = false;
  }
}

onMounted(() => {
  // Category filters are optional: without them the list still works.
  categories.fetchAll().catch(() => undefined);
  load();
  applySeo({
    title: "Blog médical – Actualités & Conseils santé – Clinique Saint Viateur",
    description:
      "Actualités médicales, conseils de prévention et nouvelles de la Clinique Saint Viateur à Cocody, Abidjan.",
    canonical: window.location.href,
  });
});

watch(search, () => {
  clearTimeout(searchTimeout);
  searchTimeout = setTimeout(() => load(1), 350);
});

watch(activeCategory, () => load(1));

function onPageChange(page: number) {
  load(page);
  scrollToHash("#resultats");
}
</script>

<template>
  <PageHeader
    kicker="Notre blog médical"
    title="Actualités & Conseils santé"
    lead="Restez informé des actualités de la clinique, des conseils de prévention et des nouvelles médicales utiles pour votre santé et celle de votre famille."
    :crumbs="[{ label: 'Accueil', to: '/' }, { label: 'Blog médical' }]"
  />

  <section id="resultats" class="section list-section" aria-label="Articles">
    <div class="section-inner">
      <div class="list-toolbar">
        <label class="list-search">
          <Search :size="16" aria-hidden="true" />
          <span class="sr-only">Rechercher un article</span>
          <input v-model="search" type="search" placeholder="Rechercher un article…" />
        </label>
        <FilterPills v-model="activeCategory" :options="categoryOptions" label="Filtrer par catégorie" />
      </div>

      <SkeletonGrid v-if="loading && !articles.items.length" :count="6" />
      <LoadError v-else-if="loadError" @retry="load()" />
      <template v-else-if="articles.items.length">
        <div class="blog-grid" :class="{ 'is-refreshing': loading }" :aria-busy="loading">
          <BlogCard
            v-for="(a, i) in articles.items"
            :key="a.id"
            v-reveal="{ type: 'up', delay: (i % 3) * 90 }"
            :article="a"
          />
        </div>
        <Pagination :page="articles.page" :total="articles.total" :page-size="articles.pageSize" @update:page="onPageChange" />
      </template>
      <EmptyState v-else :icon="Newspaper" title="Aucun article trouvé" message="Essayez une autre recherche ou catégorie." />
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
.blog-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(min(300px, 100%), 1fr));
  gap: 22px;
  transition: opacity 0.3s;
}
.blog-grid.is-refreshing {
  opacity: 0.45;
  pointer-events: none;
}
</style>
