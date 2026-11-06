import { api } from "@/services/api";

export const uploadService = {
  async uploadImage(file: File): Promise<string> {
    const formData = new FormData();
    formData.append("file", file);
    const res = await api.post<{ url: string }>("/api/uploads/images", formData);
    return res.data.url;
  },
  /** MP4 or WebM, checked server-side (signature + size). */
  async uploadVideo(file: File): Promise<string> {
    const formData = new FormData();
    formData.append("file", file);
    const res = await api.post<{ url: string }>("/api/uploads/videos", formData);
    return res.data.url;
  },
};
