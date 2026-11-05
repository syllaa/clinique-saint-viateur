import { api } from "@/services/api";

export type ReactionType = "like" | "interested" | "hot" | "not_interested";

export interface ReactionCounts {
  like: number;
  interested: number;
  hot: number;
  not_interested: number;
}

export interface PromotionListItem {
  id: number;
  title: string;
  slug: string;
  short_description: string;
  value_label: string;
  category: string | null;
  cover_image_url: string | null;
  image_alt: string | null;
  valid_until: string;
  is_published: boolean;
  position: number;
  created_at: string;
  is_expired: boolean;
  reaction_counts: ReactionCounts;
  my_reaction: ReactionType | null;
}

export interface Promotion extends PromotionListItem {
  updated_at: string;
}

export interface PromotionPage {
  items: PromotionListItem[];
  total: number;
  page: number;
  page_size: number;
}

export type PromotionPayload = Partial<{
  title: string;
  short_description: string;
  value_label: string;
  category: string | null;
  cover_image_url: string | null;
  image_alt: string | null;
  valid_until: string;
  is_published: boolean;
  position: number;
}>;

export interface PromotionListParams {
  search?: string;
  category?: string;
  sort?: "date" | "popular";
  page?: number;
  page_size?: number;
  device_id?: string;
}

export const promotionService = {
  listActive(deviceId?: string) {
    return api
      .get<PromotionListItem[]>("/api/promotions", { params: deviceId ? { device_id: deviceId } : {} })
      .then((r) => r.data);
  },
  listAll(params: PromotionListParams) {
    return api.get<PromotionPage>("/api/promotions/all", { params }).then((r) => r.data);
  },
  listCategories() {
    return api.get<string[]>("/api/promotions/categories").then((r) => r.data);
  },
  listAllAdmin() {
    return api.get<PromotionListItem[]>("/api/promotions/admin/all").then((r) => r.data);
  },
  getByIdAdmin(id: number) {
    return api.get<Promotion>(`/api/promotions/admin/${id}`).then((r) => r.data);
  },
  create(payload: PromotionPayload) {
    return api.post<Promotion>("/api/promotions", payload).then((r) => r.data);
  },
  update(id: number, payload: PromotionPayload) {
    return api.patch<Promotion>(`/api/promotions/${id}`, payload).then((r) => r.data);
  },
  toggleActive(id: number) {
    return api.patch<Promotion>(`/api/promotions/${id}/toggle-active`).then((r) => r.data);
  },
  remove(id: number) {
    return api.delete(`/api/promotions/${id}`);
  },
  react(id: number, deviceId: string, reactionType: ReactionType) {
    return api
      .post<Promotion>(`/api/promotions/${id}/reactions`, { device_id: deviceId, reaction_type: reactionType })
      .then((r) => r.data);
  },
};
