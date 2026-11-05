import { defineStore } from "pinia";
import { computed, ref } from "vue";

import { siteService, type SiteMessage } from "@/services/siteService";

export const useMessagesStore = defineStore("messages", () => {
  const items = ref<SiteMessage[]>([]);

  const unreadCount = computed(() => items.value.filter((m) => m.status === "new").length);

  async function fetchAll() {
    items.value = await siteService.listMessages();
  }

  async function markRead(id: number) {
    const updated = await siteService.markMessageRead(id);
    const index = items.value.findIndex((m) => m.id === id);
    if (index !== -1) items.value[index] = updated;
  }

  async function markAllRead() {
    await siteService.markAllMessagesRead();
    items.value = items.value.map((m) => ({ ...m, status: "read" as const }));
  }

  async function remove(id: number) {
    await siteService.deleteMessage(id);
    items.value = items.value.filter((m) => m.id !== id);
  }

  return { items, unreadCount, fetchAll, markRead, markAllRead, remove };
});
