<script setup lang="ts">
import { Calendar } from "@lucide/vue";
import { mediaUrl } from "@/services/api";
import type { ArticleListItem } from "@/services/blogService";

defineProps<{ article: ArticleListItem }>();
</script>

<template>
  <RouterLink :to="`/blog/${article.slug}`" class="blog-card" v-reveal>
    <div class="blog-thumb">
      <img v-if="mediaUrl(article.cover_image_url)" :src="mediaUrl(article.cover_image_url)!" :alt="article.title" />
      <div v-else class="blog-emoji">{{ article.icon }}</div>
      <span class="blog-tag">{{ article.category.name }}</span>
      <span class="blog-date meta-item"><Calendar :size="13" aria-hidden="true" />{{ new Date(article.created_at).toLocaleDateString("fr-FR") }}</span>
    </div>
    <div class="blog-body">
      <div class="blog-title">{{ article.title }}</div>
      <div class="blog-excerpt">{{ article.excerpt }}</div>
    </div>
    <div class="blog-footer">
      <span class="blog-more">Lire l'article →</span>
      <span style="font-size: 0.7rem; color: var(--muted)">{{ article.author }}</span>
    </div>
  </RouterLink>
</template>

<style scoped>
.blog-card {
  display: block;
  background: var(--surface);
  border-radius: 15px;
  overflow: hidden;
  border: 1px solid var(--border-soft);
  text-decoration: none;
  color: inherit;
  transition:
    transform 0.32s,
    box-shadow 0.32s,
    border-color 0.32s;
}
.blog-card:hover {
  transform: translateY(-7px);
  box-shadow: 0 22px 52px rgba(150, 12, 30, 0.1);
  border-color: #e8a8ae;
}
.blog-thumb {
  height: 185px;
  background: linear-gradient(135deg, var(--navy), var(--blue));
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
}
.blog-thumb img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.55s cubic-bezier(0.22, 0.68, 0, 1);
}
.blog-card:hover .blog-thumb img {
  transform: scale(1.08);
}
.blog-emoji {
  font-size: 4rem;
  opacity: 0.32;
}
.blog-tag {
  position: absolute;
  top: 13px;
  left: 13px;
  background: var(--gold);
  color: #fff;
  font-size: 0.62rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  padding: 4px 10px;
  border-radius: 100px;
}
.blog-date {
  position: absolute;
  bottom: 13px;
  right: 13px;
  background: rgba(0, 0, 0, 0.5);
  color: rgba(255, 255, 255, 0.8);
  font-size: 0.65rem;
  padding: 3px 9px;
  border-radius: 100px;
}
.blog-body {
  padding: 20px;
}
.blog-title {
  font-family: var(--font-serif);
  font-size: 1.1rem;
  color: var(--heading);
  line-height: 1.38;
  margin-bottom: 9px;
  font-weight: 600;
}
.blog-excerpt {
  font-size: 0.8rem;
  color: var(--muted);
  line-height: 1.68;
}
.blog-footer {
  padding: 13px 20px;
  border-top: 1px solid var(--border-soft);
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.blog-more {
  font-size: 0.78rem;
  color: var(--blue);
  font-weight: 600;
  text-decoration: none;
  display: flex;
  align-items: center;
  gap: 5px;
  transition: gap 0.2s;
}
.blog-card:hover .blog-more {
  gap: 9px;
}
</style>
