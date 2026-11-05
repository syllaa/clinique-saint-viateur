<script setup lang="ts">
import { Newspaper } from "@lucide/vue";
import { onMounted, ref, watch } from "vue";

import BlogCard from "@/components/blog/BlogCard.vue";
import Breadcrumbs from "@/components/common/Breadcrumbs.vue";
import EmptyState from "@/components/common/EmptyState.vue";
import LoadError from "@/components/common/LoadError.vue";
import Pagination from "@/components/common/Pagination.vue";
import Spinner from "@/components/common/Spinner.vue";
import { applySeo } from "@/composables/useHead";
import { useArticlesStore } from "@/stores/articles";
import { useBlogCategoriesStore } from "@/stores/blogCategories";

const articles = useArticlesStore();
const categories = useBlogCategoriesStore();

const search = ref("");
const activeCategory = ref<string | null>(null);
const loading = ref(true);
const loadError = ref(false);

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

function selectCategory(slug: string | null) {
  activeCategory.value = slug;
  load(1);
}

function onPageChange(page: number) {
  load(page);
  window.scrollTo({ top: 0, behavior: "smooth" });
}
</script>

<template>

  <section class="section blog-hero">
    <div class="section-inner">
      <Breadcrumbs :items="[{ label: 'Accueil', to: '/' }, { label: 'Blog médical' }]" />
      <p v-reveal class="section-kicker">Notre blog médical</p>
      <h1 v-reveal="'words'" class="section-title d1">Actualités & Conseils santé</h1>
      <p v-reveal class="section-lead d2">
        Restez informé des actualités de la clinique, des conseils de prévention et des nouvelles médicales utiles
        pour votre santé et celle de votre famille.
      </p>

      <div class="blog-toolbar">
        <input v-model="search" type="search" placeholder="Rechercher un article…" class="blog-search" />
        <div class="blog-cats">
          <button class="cat-pill" :class="{ on: activeCategory === null }" @click="selectCategory(null)">
            Tous
          </button>
          <button
            v-for="c in categories.items"
            :key="c.id"
            class="cat-pill"
            :class="{ on: activeCategory === c.slug }"
            @click="selectCategory(c.slug)"
          >
            {{ c.name }}
          </button>
        </div>
      </div>

      <div v-if="loading" class="blog-loading"><Spinner :size="26" /></div>
      <LoadError v-else-if="loadError" @retry="load()" />
      <template v-else-if="articles.items.length">
        <div class="blog-grid">
          <BlogCard v-for="a in articles.items" :key="a.id" :article="a" />
        </div>
        <Pagination :page="articles.page" :total="articles.total" :page-size="articles.pageSize" @update:page="onPageChange" />
      </template>
      <EmptyState v-else :icon="Newspaper" title="Aucun article trouvé" message="Essayez une autre recherche ou catégorie." />
    </div>
  </section>

</template>

<style scoped>
.blog-hero {
  padding-top: 128px;
  background: var(--bg-alt);
  min-height: 60vh;
}
.blog-toolbar {
  margin-bottom: 32px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}
.blog-search {
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
.blog-search:focus {
  border-color: var(--blue);
}
.blog-cats {
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
.blog-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 22px;
}
.blog-loading {
  display: flex;
  justify-content: center;
  padding: 60px 0;
}
</style>
