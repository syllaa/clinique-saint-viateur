import { api } from "@/services/api";

export const uploadService = {
  async uploadImage(file: File): Promise<string> {
    const formData = new FormData();
    formData.append("file", file);
    const res = await api.post<{ url: string }>("/api/uploads/images", formData);
    return res.data.url;
  },
};
