<script setup lang="ts">
import { onMounted } from "vue";

import { setTitle } from "@/composables/useHead";

onMounted(() => {
  setTitle("Page introuvable – Clinique Saint Viateur");
});
</script>

<template>

  <section class="nf-section">
    <div class="nf-inner">
      <div class="nf-code">404</div>
      <h1>Page introuvable</h1>
      <p>La page que vous cherchez n'existe pas ou a été déplacée.</p>
      <div class="nf-actions">
        <RouterLink to="/" class="btn-primary">← Retour à l'accueil</RouterLink>
        <RouterLink to="/specialites" class="btn-outline">Voir nos spécialités</RouterLink>
      </div>
    </div>
  </section>

</template>

<style scoped>
.nf-section {
  min-height: 80vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 128px 5vw 60px;
  background: var(--bg-alt);
}
.nf-inner {
  text-align: center;
  max-width: 480px;
}
.nf-code {
  font-family: "Cormorant Garamond", serif;
  font-size: 5.5rem;
  color: var(--blue);
  line-height: 1;
  margin-bottom: 8px;
  opacity: 0.85;
}
.nf-inner h1 {
  font-size: 1.5rem;
  color: var(--heading);
  margin-bottom: 12px;
}
.nf-inner p {
  color: var(--muted);
  font-size: 0.94rem;
  margin-bottom: 28px;
}
.nf-actions {
  display: flex;
  gap: 14px;
  justify-content: center;
  flex-wrap: wrap;
}
</style>
