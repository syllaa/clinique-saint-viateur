/**
 * localStorage wrappers that never throw. Access can fail in strict private
 * browsing (Safari), with blocked site data or when the quota is full; in
 * those cases the app keeps working with in-memory state only.
 */
export function storageGet(key: string): string | null {
  try {
    return window.localStorage.getItem(key);
  } catch {
    return null;
  }
}

export function storageSet(key: string, value: string): void {
  try {
    window.localStorage.setItem(key, value);
  } catch {
    /* storage unavailable: value stays in memory only */
  }
}

export function storageRemove(key: string): void {
  try {
    window.localStorage.removeItem(key);
  } catch {
    /* storage unavailable: nothing to remove */
  }
}
