<script setup lang="ts">
import { ref } from "vue";
import { useRoute, useRouter } from "vue-router";

import "@/assets/admin.css";
import Spinner from "@/components/common/Spinner.vue";
import { useAuthStore } from "@/stores/auth";
import { apiErrorMessage } from "@/utils/apiError";

const username = ref("");
const password = ref("");
const error = ref("");
const loading = ref(false);

const auth = useAuthStore();
const router = useRouter();
const route = useRoute();

async function doLogin() {
  if (loading.value) return;
  error.value = "";
  loading.value = true;
  try {
    await auth.login(username.value.trim(), password.value);
    const redirect = (route.query.redirect as string) || "/admin";
    router.push(redirect);
  } catch (err) {
    // 401 → wrong credentials; 429 → temporarily blocked (message from the API).
    error.value = apiErrorMessage(err, "Identifiants incorrects. Veuillez réessayer.");
  } finally {
    loading.value = false;
  }
}

function backToSite() {
  router.push({ name: "home" });
}
</script>

<template>
  <div class="login-screen">
    <div class="login-card">
      <div class="login-head">
        <div class="login-emblem">✚</div>
        <div>
          <div style="font-size: 0.83rem; font-weight: 600; color: var(--a-text)">Administration</div>
          <div style="font-size: 0.66rem; color: var(--a-muted); text-transform: uppercase; letter-spacing: 0.1em">
            Clinique Saint Viateur
          </div>
        </div>
      </div>
      <h2>Connexion</h2>
      <p>Espace réservé au personnel administratif autorisé</p>
      <div v-if="error" class="login-err" role="alert">{{ error }}</div>
      <label class="al" for="lu">Identifiant</label>
      <input id="lu" class="ai" v-model="username" type="text" placeholder="admin" :disabled="loading" @keydown.enter="doLogin" />
      <label class="al" for="lp">Mot de passe</label>
      <input id="lp" class="ai" v-model="password" type="password" placeholder="••••••••" :disabled="loading" @keydown.enter="doLogin" />
      <button class="ab ab-gold ab-full" :disabled="loading" @click="doLogin">
        <span class="btn-content"><Spinner v-if="loading" :size="14" />{{ loading ? "Connexion…" : "Connexion →" }}</span>
      </button>
      <button class="back-link" :disabled="loading" @click="backToSite">← Retour au site</button>
    </div>
  </div>
</template>

<style scoped>
.login-screen {
  min-height: 100vh;
  background: var(--a-bg);
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>
