import { defineStore } from "pinia";
import { ref } from "vue";

import { blogService, type BlogCategory } from "@/services/blogService";

export const useBlogCategoriesStore = defineStore("blogCategories", () => {
  const items = ref<BlogCategory[]>([]);
  const adminItems = ref<BlogCategory[]>([]);

  async function fetchAll() {
    items.value = await blogService.listCategories();
  }

  async function fetchAdminAll() {
    adminItems.value = await blogService.listAllCategoriesAdmin();
  }

  async function create(payload: { name: string; position?: number }) {
    const created = await blogService.createCategory(payload);
    adminItems.value = [...adminItems.value, created];
    return created;
  }

  async function update(id: number, payload: Partial<{ name: string; position: number; is_active: boolean }>) {
    const updated = await blogService.updateCategory(id, payload);
    adminItems.value = adminItems.value.map((c) => (c.id === id ? updated : c));
    return updated;
  }

  async function toggleActive(id: number) {
    const updated = await blogService.toggleCategoryActive(id);
    adminItems.value = adminItems.value.map((c) => (c.id === id ? updated : c));
    return updated;
  }

  async function remove(id: number) {
    await blogService.deleteCategory(id);
    adminItems.value = adminItems.value.filter((c) => c.id !== id);
  }

  return { items, adminItems, fetchAll, fetchAdminAll, create, update, toggleActive, remove };
});
