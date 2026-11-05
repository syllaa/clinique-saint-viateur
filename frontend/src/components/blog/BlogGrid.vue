<script setup lang="ts">
import { onMounted, ref } from "vue";

import BlogCard from "@/components/blog/BlogCard.vue";
import LoadError from "@/components/common/LoadError.vue";
import { useArticlesStore } from "@/stores/articles";

const articles = useArticlesStore();
const loadError = ref(false);
const retrying = ref(false);

async function load() {
  loadError.value = false;
  retrying.value = true;
  try {
    await articles.fetchPublished({ page: 1, page_size: 3 });
  } catch {
    loadError.value = true;
  } finally {
    retrying.value = false;
  }
}

onMounted(load);
</script>

<template>
  <LoadError
    v-if="loadError && !articles.items.length"
    title="Impossible de charger les articles"
    :retrying="retrying"
    @retry="load"
  />
  <div v-else class="blog-grid">
    <BlogCard v-for="article in articles.items" :key="article.id" :article="article" />
  </div>
</template>

<style scoped>
.blog-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 22px;
}
</style>
