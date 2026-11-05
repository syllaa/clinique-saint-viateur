import { computed, ref, watchEffect } from "vue";

import { storageGet, storageRemove, storageSet } from "@/utils/storage";

/**
 * Single source of truth for "should this site animate?".
 *
 * Reduced motion is ON when the visitor chose it on the site, or when their
 * system asks for it (prefers-reduced-motion) and they did not override it.
 * The result is mirrored on <html data-motion="reduce|full">, so CSS can use
 * one selector instead of duplicating @media queries.
 */
type Choice = "reduce" | "full" | null;

const STORAGE_KEY = "sv_motion";

const media =
  typeof window !== "undefined" && typeof window.matchMedia === "function"
    ? window.matchMedia("(prefers-reduced-motion: reduce)")
    : null;

const systemReduced = ref(media?.matches ?? false);
media?.addEventListener?.("change", (e) => {
  systemReduced.value = e.matches;
});

const storedChoice = storageGet(STORAGE_KEY);
const userChoice = ref<Choice>(storedChoice === "reduce" || storedChoice === "full" ? storedChoice : null);

export const reducedMotion = computed(() =>
  userChoice.value === null ? systemReduced.value : userChoice.value === "reduce",
);

watchEffect(() => {
  if (typeof document !== "undefined") {
    document.documentElement.dataset.motion = reducedMotion.value ? "reduce" : "full";
  }
  if (userChoice.value) storageSet(STORAGE_KEY, userChoice.value);
  else storageRemove(STORAGE_KEY);
});

/** Non-reactive read, for code running once (directives, canvas setup). */
export function isReducedMotion(): boolean {
  return reducedMotion.value;
}

export function useMotionPreference() {
  function toggle() {
    const next: Choice = reducedMotion.value ? "full" : "reduce";
    // Going back to the system default clears the stored override.
    const systemDefault: Choice = systemReduced.value ? "reduce" : "full";
    userChoice.value = next === systemDefault ? null : next;
  }
  return { reducedMotion, toggle };
}
