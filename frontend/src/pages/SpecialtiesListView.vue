<script setup lang="ts">
import { Stethoscope } from "@lucide/vue";
import { onMounted, ref } from "vue";

import EmptyState from "@/components/common/EmptyState.vue";
import LoadError from "@/components/common/LoadError.vue";
import PageHeader from "@/components/common/PageHeader.vue";
import SkeletonGrid from "@/components/common/SkeletonGrid.vue";
import SpecialtyCard from "@/components/specialties/SpecialtyCard.vue";
import { vTilt } from "@/directives/tilt";
import { applySeo } from "@/composables/useHead";
import { useSpecialtiesStore } from "@/stores/specialties";

const specialties = useSpecialtiesStore();
// Start in the loading state when nothing is cached yet, so the empty state
// never flashes before the first request.
const loading = ref(!specialties.items.length);
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
  <PageHeader
    kicker="Nos spécialités"
    title="Une gamme complète de soins médicaux"
    lead="De la médecine générale aux spécialités les plus pointues, la Clinique Saint Viateur vous accueille avec un plateau technique complet et des médecins qualifiés. Sélectionnez une spécialité pour en savoir plus."
    :crumbs="[{ label: 'Accueil', to: '/' }, { label: 'Nos spécialités' }]"
  />

  <section class="section list-section" aria-labelledby="specialties-list-title">
    <div class="section-inner">
      <h2 id="specialties-list-title" class="sr-only">Liste de nos spécialités</h2>
      <div v-if="specialties.items.length" class="specialties-grid">
        <SpecialtyCard
          v-for="(s, i) in specialties.items"
          :key="s.id"
          v-reveal="{ type: 'up', delay: (i % 4) * 80 }"
          v-tilt="4"
          :specialty="s"
        />
      </div>
      <SkeletonGrid v-else-if="loading" :count="8" :min-width="220" />
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
.list-section {
  background: var(--bg-alt);
  min-height: 50vh;
}
.specialties-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(min(220px, 100%), 1fr));
  gap: 18px;
  perspective: 1000px;
}
</style>
