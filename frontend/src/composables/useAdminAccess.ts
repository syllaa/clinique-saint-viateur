import { ref, watchEffect } from "vue";

import { storageGet, storageSet } from "@/utils/storage";

const STORAGE_KEY = "sv_admin_unlocked";

// Controls whether the "Admin" entry point (nav button + /login, /admin
// routes) is shown in the public UI. Visible by default; Ctrl+Shift+U hides
// it on this browser, Ctrl+Shift+A shows it again.
//
// This is NOT a security boundary: the admin API stays protected by login
// (JWT + admin role, rate-limited) whether the button is shown or not.
const unlocked = ref(storageGet(STORAGE_KEY) !== "0");

watchEffect(() => {
  storageSet(STORAGE_KEY, unlocked.value ? "1" : "0");
});

export function useAdminAccess() {
  return { unlocked };
}
