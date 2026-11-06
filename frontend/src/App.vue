<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref, watch } from "vue";
import { useRoute, useRouter } from "vue-router";

import DialogModal from "@/components/common/DialogModal.vue";
import FooterBar from "@/components/layout/FooterBar.vue";
import JobsTicker from "@/components/layout/JobsTicker.vue";
import NavBar from "@/components/layout/NavBar.vue";
import NavProgress from "@/components/layout/NavProgress.vue";
import { useAdminAccess } from "@/composables/useAdminAccess";
import { reducedMotion } from "@/motion/motionPreferences";
import { notifyPageLeft } from "@/motion/pageTransition";
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

// Admin entry point: the "Admin" button and the /login, /admin routes are
// shown by default; Ctrl+Shift+U hides them on this browser, Ctrl+Shift+A
// shows them again (see useAdminAccess).
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

// After a page change, move keyboard/screen-reader focus to the new content
// (otherwise it stays on the link that was clicked in the old page).
const mainRef = ref<HTMLElement | null>(null);
function onPageEntered() {
  mainRef.value?.focus({ preventScroll: true });
}
</script>

<style>
/* Page transitions (App.vue). Leave: quick fade + slight rise. Enter: fade
   only — a transform here would briefly become the containing block of
   fixed/pinned elements (GSAP pins, overlays) on the incoming page. */
.page-leave-active {
  transition:
    opacity 0.25s ease,
    transform 0.25s ease;
}
.page-leave-to {
  opacity: 0;
  transform: translateY(-12px);
}
.page-enter-active {
  transition: opacity 0.45s var(--ease-out);
}
.page-enter-from {
  opacity: 0;
}
</style>

<template>
  <template v-if="isPublic">
    <NavProgress />
    <a href="#main-content" class="skip-link">Aller au contenu</a>
    <NavBar />
    <JobsTicker />
    <main id="main-content" ref="mainRef" tabindex="-1">
      <!-- Page transition: the old page fades up and out, the new one fades
           in. The wrapper gives multi-root pages a single element to animate. -->
      <router-view v-slot="{ Component, route: viewRoute }">
        <Transition name="page" mode="out-in" @after-leave="notifyPageLeft" @after-enter="onPageEntered">
          <div :key="viewRoute.path" class="page">
            <component :is="Component" />
          </div>
        </Transition>
      </router-view>
    </main>
    <FooterBar />
  </template>
  <router-view v-else />
  <DialogModal />
</template>
