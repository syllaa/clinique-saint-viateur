import { storageGet, storageSet } from "@/utils/storage";

const STORAGE_KEY = "sv_device_id";

let cached: string | null = null;

function randomId(): string {
  // crypto.randomUUID only exists in secure contexts (HTTPS / localhost).
  if (typeof crypto !== "undefined" && typeof crypto.randomUUID === "function") {
    return crypto.randomUUID();
  }
  return `${Date.now().toString(36)}-${Math.random().toString(36).slice(2)}-${Math.random().toString(36).slice(2)}`;
}

/** An anonymous per-browser id used to attribute offer reactions — the site has
 * no public user accounts, so this is the only identity a visitor has. Generated
 * once and persisted in localStorage, mirroring useTheme.ts's storage pattern. */
export function useDeviceId(): string {
  if (cached) return cached;
  const stored = storageGet(STORAGE_KEY);
  if (stored) {
    cached = stored;
    return cached;
  }
  const id = randomId();
  storageSet(STORAGE_KEY, id);
  cached = id;
  return id;
}
