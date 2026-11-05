import { defineStore } from "pinia";
import { ref } from "vue";

import {
  blogService,
  type Article,
  type ArticleFaq,
  type ArticleListItem,
  type ArticleListParams,
  type ArticlePayload,
} from "@/services/blogService";

export const useArticlesStore = defineStore("articles", () => {
  const items = ref<ArticleListItem[]>([]);
  const adminItems = ref<ArticleListItem[]>([]);
  const total = ref(0);
  const page = ref(1);
  const pageSize = ref(9);
  const current = ref<Article | null>(null);
  const related = ref<ArticleListItem[]>([]);

  async function fetchPublished(params: ArticleListParams = {}) {
    const result = await blogService.listArticles({ page: page.value, page_size: pageSize.value, ...params });
    items.value = result.items;
    total.value = result.total;
    page.value = result.page;
    pageSize.value = result.page_size;
    return result;
  }

  async function fetchAll(params: ArticleListParams = {}) {
    const result = await blogService.listAllArticlesAdmin(params);
    adminItems.value = result.items;
    return result;
  }

  async function fetchByIdAdmin(id: number) {
    current.value = await blogService.getArticleByIdAdmin(id);
    return current.value;
  }

  async function fetchBySlug(slug: string) {
    current.value = await blogService.getArticleBySlug(slug);
    related.value = await blogService.getRelatedArticles(slug);
    return current.value;
  }

  async function create(payload: ArticlePayload) {
    const created = await blogService.createArticle(payload);
    adminItems.value = [created, ...adminItems.value];
    return created;
  }

  async function update(id: number, payload: ArticlePayload) {
    const updated = await blogService.updateArticle(id, payload);
    adminItems.value = adminItems.value.map((a) => (a.id === id ? updated : a));
    if (current.value?.id === id) current.value = updated;
    return updated;
  }

  async function remove(id: number) {
    await blogService.deleteArticle(id);
    adminItems.value = adminItems.value.filter((a) => a.id !== id);
  }

  async function addFaq(articleId: number, payload: Partial<ArticleFaq>) {
    const faq = await blogService.addArticleFaq(articleId, payload);
    if (current.value?.id === articleId) current.value.faqs = [...current.value.faqs, faq];
    return faq;
  }

  async function removeFaq(faqId: number) {
    await blogService.removeArticleFaq(faqId);
    if (current.value) current.value.faqs = current.value.faqs.filter((f) => f.id !== faqId);
  }

  return {
    items,
    adminItems,
    total,
    page,
    pageSize,
    current,
    related,
    fetchPublished,
    fetchAll,
    fetchByIdAdmin,
    fetchBySlug,
    create,
    update,
    remove,
    addFaq,
    removeFaq,
  };
});
