import { api } from "@/services/api";

export interface JobOfferListItem {
  id: number;
  title: string;
  slug: string;
  department: string | null;
  contract_type: string;
  location: string;
  short_description: string;
  status: "published" | "draft";
  application_deadline: string | null;
  created_at: string;
}

export interface JobOffer extends JobOfferListItem {
  description: string;
  missions: string | null;
  profile_requirements: string | null;
  skills: string | null;
  experience_level: string | null;
  seo_title: string | null;
  seo_description: string | null;
  updated_at: string;
}

export type JobOfferPayload = Partial<{
  title: string;
  department: string | null;
  contract_type: string;
  location: string;
  short_description: string;
  description: string;
  missions: string | null;
  profile_requirements: string | null;
  skills: string | null;
  experience_level: string | null;
  status: "published" | "draft";
  application_deadline: string | null;
  seo_title: string | null;
  seo_description: string | null;
}>;

export interface JobApplication {
  id: number;
  job_offer_id: number;
  first_name: string;
  last_name: string;
  email: string;
  phone: string;
  cover_letter: string | null;
  status: "nouvelle" | "en_cours" | "retenue" | "rejetee";
  created_at: string;
}

export const jobService = {
  listOffers(params: { department?: string; contract_type?: string } = {}) {
    return api.get<JobOfferListItem[]>("/api/jobs/offers", { params }).then((r) => r.data);
  },
  listAllOffersAdmin() {
    return api.get<JobOfferListItem[]>("/api/jobs/offers/admin/all").then((r) => r.data);
  },
  getOfferByIdAdmin(id: number) {
    return api.get<JobOffer>(`/api/jobs/offers/admin/${id}`).then((r) => r.data);
  },
  getOfferBySlug(slug: string) {
    return api.get<JobOffer>(`/api/jobs/offers/${slug}`).then((r) => r.data);
  },
  createOffer(payload: JobOfferPayload) {
    return api.post<JobOffer>("/api/jobs/offers", payload).then((r) => r.data);
  },
  updateOffer(id: number, payload: JobOfferPayload) {
    return api.patch<JobOffer>(`/api/jobs/offers/${id}`, payload).then((r) => r.data);
  },
  deleteOffer(id: number) {
    return api.delete(`/api/jobs/offers/${id}`);
  },

  submitApplication(slug: string, formData: FormData) {
    return api.post<JobApplication>(`/api/jobs/offers/${slug}/applications`, formData).then((r) => r.data);
  },
  listApplications(params: { offer_id?: number; status?: string } = {}) {
    return api.get<JobApplication[]>("/api/jobs/applications", { params }).then((r) => r.data);
  },
  updateApplicationStatus(id: number, status: string) {
    return api.patch<JobApplication>(`/api/jobs/applications/${id}/status`, { status }).then((r) => r.data);
  },
  async downloadCv(id: number, filename: string) {
    const res = await api.get(`/api/jobs/applications/${id}/cv`, { responseType: "blob" });
    const url = URL.createObjectURL(res.data as Blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    a.remove();
    URL.revokeObjectURL(url);
  },
};
