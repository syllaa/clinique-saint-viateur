<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";

import DialogModal from "@/components/common/DialogModal.vue";
import JobsTicker from "@/components/layout/JobsTicker.vue";
import { useAdminAccess } from "@/composables/useAdminAccess";
import { useAuthStore } from "@/stores/auth";

const auth = useAuthStore();
auth.restoreSession();

const route = useRoute();
const router = useRouter();
// The ticker rides under the public NavBar on every public page — admin and
// login are a separate internal tool with their own chrome, so it's skipped there.
const showJobsTicker = computed(() => route.name !== "admin" && route.name !== "login");

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
  <JobsTicker v-if="showJobsTicker" />
  <router-view />
  <DialogModal />
</template>
