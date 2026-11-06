import { ref, watchEffect } from "vue";

import { storageGet, storageRemove, storageSet } from "@/utils/storage";

type Theme = "light" | "dark" | null;

const STORAGE_KEY = "sv_theme";
const stored = storageGet(STORAGE_KEY);
const theme = ref<Theme>(stored === "light" || stored === "dark" ? stored : null);

watchEffect(() => {
  const root = document.documentElement;
  if (theme.value) {
    root.setAttribute("data-theme", theme.value);
    storageSet(STORAGE_KEY, theme.value);
  } else {
    root.removeAttribute("data-theme");
    storageRemove(STORAGE_KEY);
  }
});

export function useTheme() {
  function isDark(defaultsDark: boolean) {
    if (theme.value === "dark") return true;
    if (theme.value === "light") return false;
    return defaultsDark;
  }

  function toggle(defaultsDark: boolean) {
    theme.value = isDark(defaultsDark) ? "light" : "dark";
  }

  return { theme, isDark, toggle };
}
