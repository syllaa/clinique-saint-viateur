<script setup lang="ts">
import axios from "axios";
import { computed, ref } from "vue";

import Spinner from "@/components/common/Spinner.vue";
import { authService } from "@/services/authService";
import { useAuthStore } from "@/stores/auth";

/**
 * Password change for the signed-in admin. The rules mirror the backend
 * (app/auth/service.py: password_problem), which stays the authority.
 */
const auth = useAuthStore();

const current = ref("");
const next = ref("");
const confirm = ref("");
const show = ref(false);
const saving = ref(false);
const error = ref("");
const done = ref(false);

const checks = computed(() => [
  { ok: next.value.length >= 10, label: "Au moins 10 caractères" },
  { ok: /[a-zA-ZÀ-ÿ]/.test(next.value) && /\d/.test(next.value), label: "Au moins une lettre et un chiffre" },
  { ok: !!next.value && next.value !== current.value, label: "Différent du mot de passe actuel" },
  { ok: !!next.value && next.value === confirm.value, label: "Les deux saisies sont identiques" },
]);
const canSubmit = computed(() => !!current.value && checks.value.every((c) => c.ok) && !saving.value);

async function submit() {
  if (!canSubmit.value) return;
  saving.value = true;
  error.value = "";
  done.value = false;
  try {
    await authService.changePassword(current.value, next.value);
    done.value = true;
    auth.weakPassword = false;
    current.value = next.value = confirm.value = "";
  } catch (e) {
    const detail = axios.isAxiosError(e) ? e.response?.data?.detail : null;
    error.value = typeof detail === "string" ? detail : "Le changement a échoué. Réessayez dans un instant.";
  } finally {
    saving.value = false;
  }
}
</script>

<template>
  <div class="sec-wrap">
    <div v-if="auth.weakPassword" class="sec-alert" role="alert">
      <strong>Mot de passe à changer.</strong> Vous vous êtes connecté avec le mot de passe par défaut ou un mot de passe
      trop court. Toute personne qui le connaît peut accéder à l'administration.
    </div>

    <div class="a-sec-title">Changer mon mot de passe</div>
    <p class="sec-help">
      Compte : <strong>{{ auth.user?.username }}</strong>. Choisissez un mot de passe que vous n'utilisez nulle part
      ailleurs. Après plusieurs essais erronés, la connexion est bloquée quelques minutes.
    </p>

    <form class="sec-form" @submit.prevent="submit">
      <label class="al" for="sec-current">Mot de passe actuel</label>
      <input id="sec-current" v-model="current" class="ai" :type="show ? 'text' : 'password'" autocomplete="current-password" required />

      <label class="al" for="sec-new">Nouveau mot de passe</label>
      <input id="sec-new" v-model="next" class="ai" :type="show ? 'text' : 'password'" autocomplete="new-password" required />

      <label class="al" for="sec-confirm">Confirmer le nouveau mot de passe</label>
      <input id="sec-confirm" v-model="confirm" class="ai" :type="show ? 'text' : 'password'" autocomplete="new-password" required />

      <label class="sec-show"><input v-model="show" type="checkbox" /> Afficher les mots de passe</label>

      <ul class="sec-checks" aria-label="Exigences du mot de passe">
        <li v-for="c in checks" :key="c.label" :class="{ ok: c.ok }">
          <span aria-hidden="true">{{ c.ok ? "✓" : "○" }}</span> {{ c.label }}
          <span class="sr-only">{{ c.ok ? "(respecté)" : "(non respecté)" }}</span>
        </li>
      </ul>

      <p v-if="error" class="sec-error" role="alert">{{ error }}</p>
      <p v-if="done" class="sec-ok" role="status">Mot de passe modifié. Utilisez-le dès votre prochaine connexion.</p>

      <button class="ab ab-gold" type="submit" :disabled="!canSubmit">
        <span class="btn-content"><Spinner v-if="saving" :size="14" />{{ saving ? "Enregistrement…" : "Enregistrer le nouveau mot de passe" }}</span>
      </button>
    </form>
  </div>
</template>

<style scoped>
.sec-wrap {
  max-width: 520px;
}
.sec-alert {
  margin-bottom: 20px;
  padding: 14px 16px;
  border-radius: 10px;
  border: 1px solid rgba(251, 191, 36, 0.45);
  background: rgba(251, 191, 36, 0.12);
  color: var(--a-text);
  font-size: 0.84rem;
  line-height: 1.55;
}
.sec-help {
  font-size: 0.8rem;
  color: var(--a-muted);
  margin-bottom: 16px;
  line-height: 1.6;
}
.sec-form {
  display: flex;
  flex-direction: column;
}
.sec-show {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.78rem;
  color: var(--a-text-2);
  margin: 4px 0 12px;
  cursor: pointer;
}
.sec-checks {
  list-style: none;
  margin-bottom: 16px;
  font-size: 0.78rem;
  color: var(--a-muted);
  display: grid;
  gap: 4px;
}
.sec-checks li.ok {
  color: #4ade80;
}
.sec-error {
  color: #f87171;
  font-size: 0.82rem;
  margin-bottom: 12px;
}
.sec-ok {
  color: #4ade80;
  font-size: 0.82rem;
  margin-bottom: 12px;
}
</style>
