const STORAGE_KEY = "sv_device_id";

let cached: string | null = null;

/** An anonymous per-browser id used to attribute offer reactions — the site has
 * no public user accounts, so this is the only identity a visitor has. Generated
 * once and persisted in localStorage, mirroring useTheme.ts's storage pattern. */
export function useDeviceId(): string {
  if (cached) return cached;
  const stored = localStorage.getItem(STORAGE_KEY);
  if (stored) {
    cached = stored;
    return cached;
  }
  const id = crypto.randomUUID();
  localStorage.setItem(STORAGE_KEY, id);
  cached = id;
  return id;
}
