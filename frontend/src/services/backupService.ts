import { api } from "@/services/api";

export interface Backup {
  filename: string;
  size_bytes: number;
  created_at: string;
}

export const backupService = {
  list() {
    return api.get<Backup[]>("/api/backups").then((r) => r.data);
  },
  create() {
    return api.post<Backup>("/api/backups").then((r) => r.data);
  },
  remove(filename: string) {
    return api.delete(`/api/backups/${filename}`);
  },
  async download(filename: string) {
    const res = await api.get(`/api/backups/${filename}/download`, { responseType: "blob" });
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
