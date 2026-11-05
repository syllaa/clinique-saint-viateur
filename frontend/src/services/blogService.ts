import { api } from "@/services/api";

export interface BlogCategory {
  id: number;
  name: string;
  slug: string;
  is_active: boolean;
  position: number;
}

export interface ArticleListItem {
  id: number;
  title: string;
  slug: string;
  excerpt: string;
  category: BlogCategory;
  author: string;
  cover_image_url: string | null;
  icon: string;
  status: "published" | "draft";
  published_at: string | null;
  created_at: string;
}

export interface ArticleFaq {
  id: number;
  question: string;
  answer: string;
  position: number;
}

export interface Article extends ArticleListItem {
  content: string;
  practical_info: string | null;
  included_items: string | null;
  benefits: string | null;
  secondary_image_url: string | null;
  secondary_image_alt: string | null;
  seo_title: string | null;
  seo_description: string | null;
  faqs: ArticleFaq[];
}

export interface ArticlePage {
  items: ArticleListItem[];
  total: number;
  page: number;
  page_size: number;
}

export type ArticlePayload = Partial<{
  title: string;
  excerpt: string;
  content: string;
  category_id: number;
  author: string;
  cover_image_url: string | null;
  icon: string;
  status: "published" | "draft";
  practical_info: string | null;
  included_items: string | null;
  benefits: string | null;
  secondary_image_url: string | null;
  secondary_image_alt: string | null;
  seo_title: string | null;
  seo_description: string | null;
}>;

export interface ArticleListParams {
  search?: string;
  category?: string;
  page?: number;
  page_size?: number;
}

export const blogService = {
  listArticles(params: ArticleListParams = {}) {
    return api.get<ArticlePage>("/api/blog/articles", { params }).then((r) => r.data);
  },
  listAllArticlesAdmin(params: ArticleListParams = {}) {
    return api.get<ArticlePage>("/api/blog/articles/admin/all", { params }).then((r) => r.data);
  },
  getArticleByIdAdmin(id: number) {
    return api.get<Article>(`/api/blog/articles/admin/${id}`).then((r) => r.data);
  },
  getArticleBySlug(slug: string) {
    return api.get<Article>(`/api/blog/articles/${slug}`).then((r) => r.data);
  },
  getRelatedArticles(slug: string) {
    return api.get<ArticleListItem[]>(`/api/blog/articles/${slug}/related`).then((r) => r.data);
  },
  createArticle(payload: ArticlePayload) {
    return api.post<Article>("/api/blog/articles", payload).then((r) => r.data);
  },
  updateArticle(id: number, payload: ArticlePayload) {
    return api.patch<Article>(`/api/blog/articles/${id}`, payload).then((r) => r.data);
  },
  deleteArticle(id: number) {
    return api.delete(`/api/blog/articles/${id}`);
  },

  addArticleFaq(articleId: number, payload: Partial<ArticleFaq>) {
    return api.post<ArticleFaq>(`/api/blog/articles/${articleId}/faqs`, payload).then((r) => r.data);
  },
  updateArticleFaq(faqId: number, payload: Partial<ArticleFaq>) {
    return api.patch<ArticleFaq>(`/api/blog/articles/faqs/${faqId}`, payload).then((r) => r.data);
  },
  removeArticleFaq(faqId: number) {
    return api.delete(`/api/blog/articles/faqs/${faqId}`);
  },

  listCategories() {
    return api.get<BlogCategory[]>("/api/blog/categories").then((r) => r.data);
  },
  listAllCategoriesAdmin() {
    return api.get<BlogCategory[]>("/api/blog/categories/admin/all").then((r) => r.data);
  },
  createCategory(payload: { name: string; position?: number }) {
    return api.post<BlogCategory>("/api/blog/categories", payload).then((r) => r.data);
  },
  updateCategory(id: number, payload: Partial<{ name: string; position: number; is_active: boolean }>) {
    return api.patch<BlogCategory>(`/api/blog/categories/${id}`, payload).then((r) => r.data);
  },
  toggleCategoryActive(id: number) {
    return api.patch<BlogCategory>(`/api/blog/categories/${id}/toggle-active`).then((r) => r.data);
  },
  deleteCategory(id: number) {
    return api.delete(`/api/blog/categories/${id}`);
  },
};
