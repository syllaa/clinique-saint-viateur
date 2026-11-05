import { defineStore } from "pinia";
import { ref } from "vue";

import { jobService, type JobOffer, type JobOfferListItem, type JobOfferPayload } from "@/services/jobService";

export const useJobOffersStore = defineStore("jobOffers", () => {
  const items = ref<JobOfferListItem[]>([]);
  const adminItems = ref<JobOfferListItem[]>([]);
  const current = ref<JobOffer | null>(null);

  async function fetchAll(params: { department?: string; contract_type?: string } = {}) {
    items.value = await jobService.listOffers(params);
  }

  async function fetchAdminAll() {
    adminItems.value = await jobService.listAllOffersAdmin();
  }

  async function fetchBySlug(slug: string) {
    current.value = await jobService.getOfferBySlug(slug);
    return current.value;
  }

  async function fetchByIdAdmin(id: number) {
    current.value = await jobService.getOfferByIdAdmin(id);
    return current.value;
  }

  async function create(payload: JobOfferPayload) {
    const created = await jobService.createOffer(payload);
    adminItems.value = [created, ...adminItems.value];
    return created;
  }

  async function update(id: number, payload: JobOfferPayload) {
    const updated = await jobService.updateOffer(id, payload);
    adminItems.value = adminItems.value.map((o) => (o.id === id ? updated : o));
    if (current.value?.id === id) current.value = updated;
    return updated;
  }

  async function remove(id: number) {
    await jobService.deleteOffer(id);
    adminItems.value = adminItems.value.filter((o) => o.id !== id);
  }

  return { items, adminItems, current, fetchAll, fetchAdminAll, fetchBySlug, fetchByIdAdmin, create, update, remove };
});
