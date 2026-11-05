<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, watch } from "vue";
import { useRoute, useRouter } from "vue-router";

import DialogModal from "@/components/common/DialogModal.vue";
import FooterBar from "@/components/layout/FooterBar.vue";
import JobsTicker from "@/components/layout/JobsTicker.vue";
import NavBar from "@/components/layout/NavBar.vue";
import { useAdminAccess } from "@/composables/useAdminAccess";
import { reducedMotion } from "@/motion/motionPreferences";
import { startLenis, stopLenis } from "@/motion/useLenis";
import { useAuthStore } from "@/stores/auth";

const auth = useAuthStore();
auth.restoreSession();

const route = useRoute();
const router = useRouter();
// Public pages share one chrome (skip link, NavBar, ticker, footer) rendered
// here once, so it persists across navigations. Admin and login are a
// separate internal tool with their own chrome, so it's skipped there.
const isPublic = computed(() => route.name !== "admin" && route.name !== "login");

// Smooth scrolling: public pages only (the admin has scrollable tables and
// editors where inertia gets in the way), and never under reduced motion.
watch(
  [isPublic, reducedMotion, () => route.matched.length],
  ([pub, reduced, resolved]) => {
    // Wait for the initial route to resolve, so a direct visit to /admin
    // never downloads Lenis.
    if (!resolved) return;
    if (pub && !reduced) startLenis();
    else stopLenis();
  },
  { immediate: true },
);

// Hidden entry point: the "Admin" link and the /login, /admin routes stay
// invisible/unreachable until unlocked with Ctrl+Shift+A (hide again with
// Ctrl+Shift+U) — keeps casual visitors from stumbling onto the admin area.
const { unlocked } = useAdminAccess();

function onKeydown(e: KeyboardEvent) {
  if (!e.ctrlKey || !e.shiftKey) return;
  const key = e.key.toLowerCase();
  if (key === "a") {
    unlocked.value = true;
  } else if (key === "u") {
    unlocked.value = false;
    if (route.name === "admin" || route.name === "login") {
      router.push({ name: "home" });
    }
  }
}

onMounted(() => window.addEventListener("keydown", onKeydown));
onBeforeUnmount(() => window.removeEventListener("keydown", onKeydown));
</script>

<template>
  <template v-if="isPublic">
    <a href="#main-content" class="skip-link">Aller au contenu</a>
    <NavBar />
    <JobsTicker />
    <main id="main-content" tabindex="-1">
      <router-view />
    </main>
    <FooterBar />
  </template>
  <router-view v-else />
  <DialogModal />
</template>
