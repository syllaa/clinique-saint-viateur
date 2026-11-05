import { api } from "@/services/api";

export type SpecialtyMediaType = "icon" | "image";

export interface SpecialtyListItem {
  id: number;
  slug: string;
  name: string;
  description: string;
  position: number;
  is_active: boolean;
  media_type: SpecialtyMediaType;
  icon_name: string | null;
  cover_image_url: string | null;
  image_alt: string | null;
  cover_video_url: string | null;
}

export interface SpecialtyDoctor {
  id: number;
  name: string;
  title: string | null;
  photo_url: string | null;
  bio: string | null;
  position: number;
}

export interface SpecialtyFaq {
  id: number;
  question: string;
  answer: string;
  position: number;
}

export interface Specialty extends SpecialtyListItem {
  full_description: string;
  services_offered: string;
  symptoms_text: string | null;
  consultation_hours: string | null;
  practical_info: string | null;
  seo_title: string | null;
  seo_description: string | null;
  created_at: string;
  updated_at: string;
  doctors: SpecialtyDoctor[];
  faqs: SpecialtyFaq[];
}

export type SpecialtyPayload = Partial<{
  name: string;
  description: string;
  position: number;
  media_type: SpecialtyMediaType;
  icon_name: string | null;
  cover_image_url: string | null;
  image_alt: string | null;
  cover_video_url: string | null;
  full_description: string;
  services_offered: string;
  symptoms_text: string | null;
  consultation_hours: string | null;
  practical_info: string | null;
  seo_title: string | null;
  seo_description: string | null;
}>;

export const specialtyService = {
  list() {
    return api.get<SpecialtyListItem[]>("/api/specialties").then((r) => r.data);
  },
  listAllAdmin() {
    return api.get<SpecialtyListItem[]>("/api/specialties/admin/all").then((r) => r.data);
  },
  getBySlug(slug: string) {
    return api.get<Specialty>(`/api/specialties/${slug}`).then((r) => r.data);
  },
  getByIdAdmin(id: number) {
    return api.get<Specialty>(`/api/specialties/admin/${id}`).then((r) => r.data);
  },
  create(payload: SpecialtyPayload) {
    return api.post<Specialty>("/api/specialties", payload).then((r) => r.data);
  },
  update(id: number, payload: SpecialtyPayload) {
    return api.patch<Specialty>(`/api/specialties/${id}`, payload).then((r) => r.data);
  },
  toggleActive(id: number) {
    return api.patch<Specialty>(`/api/specialties/${id}/toggle-active`).then((r) => r.data);
  },
  remove(id: number) {
    return api.delete(`/api/specialties/${id}`);
  },

  addDoctor(specialtyId: number, payload: Partial<SpecialtyDoctor>) {
    return api.post<SpecialtyDoctor>(`/api/specialties/${specialtyId}/doctors`, payload).then((r) => r.data);
  },
  updateDoctor(doctorId: number, payload: Partial<SpecialtyDoctor>) {
    return api.patch<SpecialtyDoctor>(`/api/specialties/doctors/${doctorId}`, payload).then((r) => r.data);
  },
  removeDoctor(doctorId: number) {
    return api.delete(`/api/specialties/doctors/${doctorId}`);
  },

  addFaq(specialtyId: number, payload: Partial<SpecialtyFaq>) {
    return api.post<SpecialtyFaq>(`/api/specialties/${specialtyId}/faqs`, payload).then((r) => r.data);
  },
  updateFaq(faqId: number, payload: Partial<SpecialtyFaq>) {
    return api.patch<SpecialtyFaq>(`/api/specialties/faqs/${faqId}`, payload).then((r) => r.data);
  },
  removeFaq(faqId: number) {
    return api.delete(`/api/specialties/faqs/${faqId}`);
  },
};
