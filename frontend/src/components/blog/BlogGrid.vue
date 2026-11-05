<script setup lang="ts">
import { onMounted } from "vue";

import BlogCard from "@/components/blog/BlogCard.vue";
import { useArticlesStore } from "@/stores/articles";

const articles = useArticlesStore();

onMounted(() => {
  articles.fetchPublished({ page: 1, page_size: 3 });
});
</script>

<template>
  <div class="blog-grid">
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
