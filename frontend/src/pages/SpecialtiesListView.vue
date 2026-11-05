<script setup lang="ts">
import { Stethoscope } from "@lucide/vue";
import { onMounted, ref } from "vue";

import Breadcrumbs from "@/components/common/Breadcrumbs.vue";
import EmptyState from "@/components/common/EmptyState.vue";
import LoadError from "@/components/common/LoadError.vue";
import Spinner from "@/components/common/Spinner.vue";
import SpecialtyCard from "@/components/specialties/SpecialtyCard.vue";
import { applySeo } from "@/composables/useHead";
import { useSpecialtiesStore } from "@/stores/specialties";

const specialties = useSpecialtiesStore();
const loading = ref(false);
const loadError = ref(false);

async function load() {
  loading.value = true;
  loadError.value = false;
  try {
    await specialties.fetchAll();
  } catch {
    loadError.value = true;
  } finally {
    loading.value = false;
  }
}

onMounted(() => {
  load();
  applySeo({
    title: "Nos spécialités médicales – Clinique Saint Viateur",
    description:
      "Découvrez l'ensemble des spécialités médicales proposées par la Clinique Saint Viateur à Cocody, Abidjan.",
    canonical: window.location.href,
  });
});
</script>

<template>

  <section class="section specialties-hero">
    <div class="section-inner">
      <Breadcrumbs :items="[{ label: 'Accueil', to: '/' }, { label: 'Nos spécialités' }]" />
      <p v-reveal class="section-kicker">Nos spécialités</p>
      <h1 v-reveal="'words'" class="section-title d1">Une gamme complète de soins médicaux</h1>
      <p v-reveal class="section-lead d2">
        De la médecine générale aux spécialités les plus pointues, la Clinique Saint Viateur vous accueille avec un
        plateau technique complet et des médecins qualifiés. Sélectionnez une spécialité pour en savoir plus.
      </p>

      <div v-if="specialties.items.length" class="specialties-grid">
        <SpecialtyCard v-for="s in specialties.items" :key="s.id" :specialty="s" />
      </div>
      <div v-else-if="loading" class="specialties-loading"><Spinner :size="26" /></div>
      <LoadError v-else-if="loadError" @retry="load" />
      <EmptyState
        v-else
        :icon="Stethoscope"
        title="Aucune spécialité pour le moment"
        message="Revenez bientôt, notre offre de soins est mise à jour régulièrement."
      />
    </div>
  </section>

</template>

<style scoped>
.specialties-hero {
  padding-top: 128px;
  background: var(--bg-alt);
  min-height: 60vh;
}
.specialties-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 18px;
}
.specialties-loading {
  display: flex;
  justify-content: center;
  padding: 60px 0;
}
</style>
