import { defineStore } from "pinia";
import { ref } from "vue";

import {
  specialtyService,
  type Specialty,
  type SpecialtyDoctor,
  type SpecialtyFaq,
  type SpecialtyListItem,
  type SpecialtyPayload,
} from "@/services/specialtyService";

export const useSpecialtiesStore = defineStore("specialties", () => {
  const items = ref<SpecialtyListItem[]>([]);
  const adminItems = ref<SpecialtyListItem[]>([]);
  const current = ref<Specialty | null>(null);

  async function fetchAll() {
    items.value = await specialtyService.list();
  }

  async function fetchAdminAll() {
    adminItems.value = await specialtyService.listAllAdmin();
  }

  async function fetchBySlug(slug: string) {
    current.value = await specialtyService.getBySlug(slug);
    return current.value;
  }

  async function fetchByIdAdmin(id: number) {
    current.value = await specialtyService.getByIdAdmin(id);
    return current.value;
  }

  async function create(payload: SpecialtyPayload) {
    const created = await specialtyService.create(payload);
    adminItems.value = [...adminItems.value, created];
    return created;
  }

  async function update(id: number, payload: SpecialtyPayload) {
    const updated = await specialtyService.update(id, payload);
    adminItems.value = adminItems.value.map((s) => (s.id === id ? updated : s));
    if (current.value?.id === id) current.value = updated;
    return updated;
  }

  async function toggleActive(id: number) {
    const updated = await specialtyService.toggleActive(id);
    adminItems.value = adminItems.value.map((s) => (s.id === id ? updated : s));
    return updated;
  }

  async function remove(id: number) {
    await specialtyService.remove(id);
    adminItems.value = adminItems.value.filter((s) => s.id !== id);
  }

  async function addDoctor(specialtyId: number, payload: Partial<SpecialtyDoctor>) {
    const doctor = await specialtyService.addDoctor(specialtyId, payload);
    if (current.value) current.value.doctors = [...current.value.doctors, doctor];
    return doctor;
  }

  async function removeDoctor(doctorId: number) {
    await specialtyService.removeDoctor(doctorId);
    if (current.value) current.value.doctors = current.value.doctors.filter((d) => d.id !== doctorId);
  }

  async function addFaq(specialtyId: number, payload: Partial<SpecialtyFaq>) {
    const faq = await specialtyService.addFaq(specialtyId, payload);
    if (current.value) current.value.faqs = [...current.value.faqs, faq];
    return faq;
  }

  async function removeFaq(faqId: number) {
    await specialtyService.removeFaq(faqId);
    if (current.value) current.value.faqs = current.value.faqs.filter((f) => f.id !== faqId);
  }

  return {
    items,
    adminItems,
    current,
    fetchAll,
    fetchAdminAll,
    fetchBySlug,
    fetchByIdAdmin,
    create,
    update,
    toggleActive,
    remove,
    addDoctor,
    removeDoctor,
    addFaq,
    removeFaq,
  };
});
