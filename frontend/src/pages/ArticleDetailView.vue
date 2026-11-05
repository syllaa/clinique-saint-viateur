<script setup lang="ts">
import { computed, onMounted, ref, watch } from "vue";
import { useRoute } from "vue-router";

import BlogCard from "@/components/blog/BlogCard.vue";
import Breadcrumbs from "@/components/common/Breadcrumbs.vue";
import EmptyState from "@/components/common/EmptyState.vue";
import Spinner from "@/components/common/Spinner.vue";
import FooterBar from "@/components/layout/FooterBar.vue";
import NavBar from "@/components/layout/NavBar.vue";
import { applySeo, resetSeo } from "@/composables/useHead";
import { mediaUrl } from "@/services/api";
import { useArticlesStore } from "@/stores/articles";

const route = useRoute();
const articles = useArticlesStore();
const loading = ref(true);
const notFound = ref(false);
const shareCopied = ref(false);

const readTimeMinutes = computed(() => {
  const text = (articles.current?.content || "").replace(/<[^>]*>/g, " ");
  const words = text.trim().split(/\s+/).filter(Boolean).length;
  return Math.max(1, Math.round(words / 200));
});

// Shared parser for the optional structured fields (practical_info/included_items/
// benefits): one item per line, each starting with an emoji — same "plain
// newline-delimited text, parsed into cards" convention as Specialty.services_offered.
function parseIconLines(text: string | null | undefined) {
  if (!text) return [];
  return text
    .split("\n")
    .map((line) => line.trim())
    .filter(Boolean)
    .map((line) => {
      const match = line.match(/^(\p{Extended_Pictographic}(?:️|‍\p{Extended_Pictographic})*)\s*(.*)$/u);
      return match ? { icon: match[1], text: match[2] } : { icon: "•", text: line };
    });
}

const practicalInfoItems = computed(() => parseIconLines(articles.current?.practical_info));
const includedItems = computed(() => parseIconLines(articles.current?.included_items));
const benefitItems = computed(() => parseIconLines(articles.current?.benefits));

async function load(slug: string) {
  loading.value = true;
  notFound.value = false;
  try {
    const article = await articles.fetchBySlug(slug);
    applySeo({
      title: article.seo_title || `${article.title} – Blog Clinique Saint Viateur`,
      description: article.seo_description || article.excerpt,
      ogImage: mediaUrl(article.cover_image_url) || undefined,
      canonical: window.location.href,
      jsonLd: {
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        headline: article.title,
        description: article.excerpt,
        author: { "@type": "Organization", name: article.author },
        datePublished: article.published_at || article.created_at,
        url: window.location.href,
      },
    });
  } catch {
    notFound.value = true;
    resetSeo();
  } finally {
    loading.value = false;
  }
}

onMounted(() => load(route.params.slug as string));
watch(
  () => route.params.slug,
  (slug) => slug && load(slug as string),
);

async function share() {
  const url = window.location.href;
  const title = articles.current?.title ?? "";
  if (navigator.share) {
    try {
      await navigator.share({ title, url });
    } catch {
      /* user cancelled share sheet, nothing to do */
    }
    return;
  }
  await navigator.clipboard.writeText(url);
  shareCopied.value = true;
  setTimeout(() => (shareCopied.value = false), 2200);
}
</script>

<template>
  <NavBar />

  <div v-if="loading" class="detail-loading"><Spinner :size="30" /></div>

  <template v-else-if="notFound || !articles.current">
    <section class="section" style="padding-top: 128px">
      <div class="section-inner">
        <EmptyState icon="📰" title="Article introuvable" message="Cet article n'existe pas ou n'est plus publié.">
          <RouterLink to="/blog" class="btn-primary" style="margin-top: 16px; display: inline-flex">
            ← Retour au blog
          </RouterLink>
        </EmptyState>
      </div>
    </section>
  </template>

  <template v-else>
    <section class="art-hero">
      <div v-if="mediaUrl(articles.current.cover_image_url)" class="art-hero-img">
        <img :src="mediaUrl(articles.current.cover_image_url)!" :alt="articles.current.title" />
        <div class="art-hero-fade"></div>
      </div>
      <div class="section-inner art-hero-inner">
        <Breadcrumbs
          :items="[
            { label: 'Accueil', to: '/' },
            { label: 'Blog', to: '/blog' },
            { label: articles.current.title },
          ]"
        />
        <span class="art-tag">{{ articles.current.category.name }}</span>
        <h1>{{ articles.current.title }}</h1>
        <div class="art-meta">
          <span>✍️ {{ articles.current.author }}</span>
          <span>📅 {{ new Date(articles.current.created_at).toLocaleDateString("fr-FR") }}</span>
          <span>⏱ {{ readTimeMinutes }} min de lecture</span>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="section-inner art-grid">
        <article class="art-body">
          <div v-if="!mediaUrl(articles.current.cover_image_url)" class="art-emoji">{{ articles.current.icon }}</div>
          <div class="art-content" v-html="articles.current.content || `<p>${articles.current.excerpt}</p>`"></div>

          <section v-if="practicalInfoItems.length" class="art-section">
            <h2>Informations pratiques</h2>
            <div class="art-icon-grid">
              <div v-for="(item, i) in practicalInfoItems" :key="i" class="art-icon-card">
                <span class="aic-icon" aria-hidden="true">{{ item.icon }}</span>
                <span class="aic-text">{{ item.text }}</span>
              </div>
            </div>
          </section>

          <section v-if="includedItems.length" class="art-section">
            <h2>L'essentiel</h2>
            <div class="art-icon-grid">
              <div v-for="(item, i) in includedItems" :key="i" class="art-icon-card">
                <span class="aic-icon" aria-hidden="true">{{ item.icon }}</span>
                <span class="aic-text">{{ item.text }}</span>
              </div>
            </div>
          </section>

          <div v-if="mediaUrl(articles.current.secondary_image_url)" class="art-secondary-img">
            <img
              :src="mediaUrl(articles.current.secondary_image_url)!"
              :alt="articles.current.secondary_image_alt || articles.current.title"
              loading="lazy"
              decoding="async"
            />
          </div>

          <section v-if="benefitItems.length" class="art-section">
            <h2>Les bénéfices</h2>
            <div class="art-icon-grid">
              <div v-for="(item, i) in benefitItems" :key="i" class="art-icon-card">
                <span class="aic-icon" aria-hidden="true">{{ item.icon }}</span>
                <span class="aic-text">{{ item.text }}</span>
              </div>
            </div>
          </section>

          <section v-if="articles.current.faqs.length" class="art-section">
            <h2>Questions fréquentes</h2>
            <details v-for="f in articles.current.faqs" :key="f.id" class="art-faq">
              <summary>{{ f.question }}</summary>
              <p>{{ f.answer }}</p>
            </details>
          </section>

          <div class="art-actions">
            <button class="btn-primary" type="button" @click="share">🔗 Partager</button>
            <span v-if="shareCopied" class="art-copied">Lien copié !</span>
            <a href="tel:+2252722590417" class="btn-ghost-art">📞 Prendre rendez-vous</a>
            <a href="tel:+2252722590417" class="art-phone-link">+225 27 22 59 04 17</a>
          </div>
        </article>

        <aside class="art-side">
          <div v-if="articles.related.length" class="art-related">
            <h3>Articles similaires</h3>
            <div class="art-related-list">
              <BlogCard v-for="a in articles.related" :key="a.id" :article="a" />
            </div>
          </div>
        </aside>
      </div>
    </section>
  </template>

  <FooterBar />
</template>

<style scoped>
.detail-loading {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
}
.art-hero {
  position: relative;
  padding-top: 128px;
  padding-bottom: 40px;
  background: linear-gradient(155deg, var(--navy) 0%, #8f1620 100%);
  overflow: hidden;
}
.art-hero-img {
  position: absolute;
  inset: 0;
  z-index: 0;
}
.art-hero-img img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  opacity: 0.3;
}
.art-hero-fade {
  position: absolute;
  inset: 0;
  background: linear-gradient(155deg, rgba(122, 15, 26, 0.88) 0%, rgba(143, 22, 32, 0.92) 100%);
}
.art-hero-inner {
  position: relative;
  z-index: 1;
}
.art-hero :deep(.crumb-link),
.art-hero :deep(.crumb-sep) {
  color: rgba(255, 255, 255, 0.5);
}
.art-hero :deep(.crumb-current) {
  color: #fff;
}
.art-tag {
  display: inline-block;
  background: var(--gold);
  color: #fff;
  font-size: 0.65rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.09em;
  padding: 4px 12px;
  border-radius: 100px;
  margin-bottom: 14px;
}
.art-hero-inner h1 {
  font-family: "Cormorant Garamond", serif;
  font-size: clamp(1.7rem, 3.2vw, 2.4rem);
  color: #fff;
  max-width: 780px;
  margin-bottom: 16px;
  line-height: 1.25;
}
.art-meta {
  display: flex;
  gap: 20px;
  flex-wrap: wrap;
  font-size: 0.82rem;
  color: rgba(255, 255, 255, 0.6);
}
.art-grid {
  display: grid;
  grid-template-columns: 1.7fr 1fr;
  gap: 48px;
  align-items: start;
}
.art-emoji {
  font-size: 3rem;
  margin-bottom: 20px;
  opacity: 0.5;
}
.art-content {
  font-size: 0.96rem;
  line-height: 1.85;
  color: var(--text);
}
.art-content :deep(h2) {
  font-size: 1.3rem;
  color: var(--heading);
  margin: 28px 0 14px;
  font-family: "Cormorant Garamond", serif;
}
.art-content :deep(h3) {
  font-size: 1.1rem;
  color: var(--heading);
  margin: 22px 0 10px;
}
.art-content :deep(p) {
  margin-bottom: 16px;
}
.art-content :deep(ul),
.art-content :deep(ol) {
  padding-left: 24px;
  margin-bottom: 16px;
}
.art-content :deep(blockquote) {
  border-left: 3px solid var(--gold);
  padding-left: 16px;
  color: var(--muted);
  font-style: italic;
  margin-bottom: 16px;
}
.art-content :deep(a) {
  color: var(--blue);
}
.art-section {
  margin: 32px 0;
}
.art-section h2 {
  font-family: "Cormorant Garamond", serif;
  font-size: 1.25rem;
  color: var(--heading);
  margin-bottom: 16px;
}
.art-icon-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 12px;
}
.art-icon-card {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  background: var(--surface);
  border: 1px solid var(--border-soft);
  border-radius: 12px;
  padding: 15px 16px;
  transition:
    transform 0.25s,
    border-color 0.25s;
}
.art-icon-card:hover {
  transform: translateY(-3px);
  border-color: #e8a8ae;
}
.aic-icon {
  font-size: 1.3rem;
  line-height: 1.2;
  flex-shrink: 0;
}
.aic-text {
  font-size: 0.86rem;
  color: var(--text);
  line-height: 1.55;
}
.art-secondary-img {
  border-radius: 14px;
  overflow: hidden;
  margin: 32px 0;
}
.art-secondary-img img {
  width: 100%;
  max-height: 420px;
  object-fit: cover;
  display: block;
}
.art-faq {
  border: 1px solid var(--border-soft);
  border-radius: 10px;
  padding: 14px 16px;
  margin-bottom: 10px;
  background: var(--surface);
}
.art-faq summary {
  cursor: pointer;
  font-weight: 600;
  font-size: 0.88rem;
  color: var(--heading);
}
.art-faq p {
  margin-top: 10px;
  font-size: 0.86rem;
  color: var(--muted);
  line-height: 1.65;
}
.art-actions {
  display: flex;
  align-items: center;
  gap: 14px;
  flex-wrap: wrap;
  margin-top: 32px;
  padding-top: 24px;
  border-top: 1px solid var(--border-soft);
}
.art-phone-link {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 0.86rem;
  font-weight: 600;
  color: var(--heading);
  text-decoration: none;
  transition: color 0.2s;
}
.art-phone-link:hover {
  color: var(--blue);
}
.btn-ghost-art {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: transparent;
  color: var(--heading);
  border: 1.5px solid var(--border-soft);
  padding: 13px 26px;
  border-radius: 5px;
  text-decoration: none;
  font-weight: 500;
  font-size: 0.9rem;
  transition: all 0.2s;
}
.btn-ghost-art:hover {
  border-color: var(--blue);
  color: var(--blue);
}
.art-copied {
  font-size: 0.8rem;
  color: var(--green);
  font-weight: 600;
}
.art-related h3 {
  font-size: 0.95rem;
  color: var(--heading);
  margin-bottom: 14px;
}
.art-related-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

@media (max-width: 980px) {
  .art-grid {
    grid-template-columns: 1fr;
  }
}
</style>
