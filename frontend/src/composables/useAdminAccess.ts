import { ref, watchEffect } from "vue";

import { storageGet, storageRemove, storageSet } from "@/utils/storage";

const STORAGE_KEY = "sv_admin_unlocked";

// A pure UI-visibility gate, not a security boundary — the actual admin API
// stays protected by JWT auth regardless. This only decides whether the
// "Admin" entry point is shown/reachable in the public-facing UI, so casual
// visitors don't stumble onto it. Unlock: Ctrl+Shift+A. Hide again: Ctrl+Shift+U.
const unlocked = ref(storageGet(STORAGE_KEY) === "1");

watchEffect(() => {
  if (unlocked.value) storageSet(STORAGE_KEY, "1");
  else storageRemove(STORAGE_KEY);
});

export function useAdminAccess() {
  return { unlocked };
}
