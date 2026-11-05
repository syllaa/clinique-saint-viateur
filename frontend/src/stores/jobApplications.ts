import { defineStore } from "pinia";
import { ref } from "vue";

import { jobService, type JobApplication } from "@/services/jobService";

export const useJobApplicationsStore = defineStore("jobApplications", () => {
  const items = ref<JobApplication[]>([]);

  async function fetchAll(params: { offer_id?: number; status?: string } = {}) {
    items.value = await jobService.listApplications(params);
  }

  async function submit(slug: string, formData: FormData) {
    return jobService.submitApplication(slug, formData);
  }

  async function updateStatus(id: number, status: string) {
    const updated = await jobService.updateApplicationStatus(id, status);
    items.value = items.value.map((a) => (a.id === id ? updated : a));
    return updated;
  }

  async function downloadCv(id: number, filename: string) {
    await jobService.downloadCv(id, filename);
  }

  return { items, fetchAll, submit, updateStatus, downloadCv };
});
