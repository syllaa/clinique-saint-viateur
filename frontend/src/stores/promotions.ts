import { defineStore } from "pinia";
import { ref } from "vue";

import { useDeviceId } from "@/composables/useDeviceId";
import {
  promotionService,
  type Promotion,
  type PromotionListItem,
  type PromotionListParams,
  type PromotionPayload,
  type ReactionType,
} from "@/services/promotionService";

export const usePromotionsStore = defineStore("promotions", () => {
  const items = ref<PromotionListItem[]>([]); // active promotions, homepage carousel
  const allItems = ref<PromotionListItem[]>([]); // "Toutes les offres" page
  const total = ref(0);
  const page = ref(1);
  const pageSize = ref(12);
  const categories = ref<string[]>([]);
  const adminItems = ref<PromotionListItem[]>([]);
  const current = ref<Promotion | null>(null);

  async function fetchActive() {
    items.value = await promotionService.listActive(useDeviceId());
  }

  async function fetchAll(params: Omit<PromotionListParams, "device_id"> = {}) {
    const result = await promotionService.listAll({ ...params, device_id: useDeviceId() });
    allItems.value = result.items;
    total.value = result.total;
    page.value = result.page;
    pageSize.value = result.page_size;
  }

  async function fetchCategories() {
    categories.value = await promotionService.listCategories();
  }

  async function fetchAdminAll() {
    adminItems.value = await promotionService.listAllAdmin();
  }

  async function fetchByIdAdmin(id: number) {
    current.value = await promotionService.getByIdAdmin(id);
    return current.value;
  }

  function applyUpdate(updated: PromotionListItem) {
    items.value = items.value.map((p) => (p.id === updated.id ? (updated as PromotionListItem) : p));
    allItems.value = allItems.value.map((p) => (p.id === updated.id ? updated : p));
    adminItems.value = adminItems.value.map((p) => (p.id === updated.id ? updated : p));
    if (current.value?.id === updated.id) current.value = updated as Promotion;
  }

  async function create(payload: PromotionPayload) {
    const created = await promotionService.create(payload);
    adminItems.value = [created, ...adminItems.value];
    return created;
  }

  async function update(id: number, payload: PromotionPayload) {
    const updated = await promotionService.update(id, payload);
    applyUpdate(updated);
    return updated;
  }

  async function toggleActive(id: number) {
    const updated = await promotionService.toggleActive(id);
    applyUpdate(updated);
    return updated;
  }

  async function remove(id: number) {
    await promotionService.remove(id);
    adminItems.value = adminItems.value.filter((p) => p.id !== id);
  }

  async function react(id: number, reactionType: ReactionType) {
    const updated = await promotionService.react(id, useDeviceId(), reactionType);
    applyUpdate(updated);
    return updated;
  }

  return {
    items,
    allItems,
    total,
    page,
    pageSize,
    categories,
    adminItems,
    current,
    fetchActive,
    fetchAll,
    fetchCategories,
    fetchAdminAll,
    fetchByIdAdmin,
    create,
    update,
    toggleActive,
    remove,
    react,
  };
});
