import { api } from "@/services/api";

export interface Ticket {
  id: number;
  subject: string;
  description: string;
  status: "open" | "in_progress" | "closed";
  priority: "low" | "normal" | "high" | "urgent";
  created_at: string;
  updated_at: string;
}

export const ticketService = {
  list(status?: string) {
    return api.get<Ticket[]>("/api/support/tickets", { params: status ? { status } : {} }).then((r) => r.data);
  },
  create(payload: { subject: string; description: string; priority?: string }) {
    return api.post<Ticket>("/api/support/tickets", payload).then((r) => r.data);
  },
  update(id: number, payload: { status?: string; priority?: string }) {
    return api.patch<Ticket>(`/api/support/tickets/${id}`, payload).then((r) => r.data);
  },
  remove(id: number) {
    return api.delete(`/api/support/tickets/${id}`);
  },
};
