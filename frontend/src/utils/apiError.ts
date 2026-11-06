import axios from "axios";

/**
 * Turns an API error into a message a visitor can read. The backend sends
 * French messages in `detail` for the cases that matter (429 too many
 * attempts, 400/422 validation); anything else gets the fallback.
 */
export function apiErrorMessage(err: unknown, fallback: string): string {
  if (!axios.isAxiosError(err)) return fallback;
  if (!err.response) return "Connexion impossible. Vérifiez votre accès à internet puis réessayez.";
  const detail = err.response.data?.detail;
  return typeof detail === "string" && detail ? detail : fallback;
}
