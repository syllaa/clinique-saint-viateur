import { defineStore } from "pinia";
import { ref } from "vue";

import { backupService, type Backup } from "@/services/backupService";

export const useBackupsStore = defineStore("backups", () => {
  const items = ref<Backup[]>([]);

  async function fetchAll() {
    items.value = await backupService.list();
  }

  async function create() {
    const created = await backupService.create();
    items.value = [created, ...items.value];
    return created;
  }

  async function remove(filename: string) {
    await backupService.remove(filename);
    items.value = items.value.filter((b) => b.filename !== filename);
  }

  async function download(filename: string) {
    await backupService.download(filename);
  }

  return { items, fetchAll, create, remove, download };
});
