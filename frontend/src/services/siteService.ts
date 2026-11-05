import { api } from "@/services/api";

export interface SiteMessage {
  id: number;
  name: string;
  email: string | null;
  phone: string | null;
  subject: string;
  content: string;
  urgency: "urgence" | "programme";
  wants_hospitalization_info: boolean;
  status: "new" | "read";
  created_at: string;
}

export const siteService = {
  // Messages
  sendMessage(payload: {
    name: string;
    email?: string;
    phone?: string;
    subject: string;
    content: string;
    urgency: "urgence" | "programme";
    wants_hospitalization_info: boolean;
    /** Honeypot (HoneypotField): must stay empty for humans. */
    website?: string;
  }) {
    return api.post<SiteMessage>("/api/messages", payload).then((r) => r.data);
  },
  listMessages() {
    return api.get<SiteMessage[]>("/api/messages").then((r) => r.data);
  },
  markMessageRead(id: number) {
    return api.patch<SiteMessage>(`/api/messages/${id}/read`).then((r) => r.data);
  },
  markAllMessagesRead() {
    return api.post("/api/messages/mark-all-read");
  },
  deleteMessage(id: number) {
    return api.delete(`/api/messages/${id}`);
  },
};
