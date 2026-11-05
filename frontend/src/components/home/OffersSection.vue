<script setup lang="ts">
import { onMounted } from "vue";

import PromotionCarousel from "@/components/promotions/PromotionCarousel.vue";
import { usePromotionsStore } from "@/stores/promotions";

const promotions = usePromotionsStore();

// The section simply stays hidden if this fails (it is v-if'd on items).
onMounted(() => promotions.fetchActive().catch(() => undefined));
</script>

<template>
  <section v-if="promotions.items.length" id="offres" class="section offers" aria-labelledby="offers-title">
    <div class="section-inner">
      <p v-reveal class="section-kicker">Nos offres</p>
      <h2 id="offers-title" v-reveal="'words'" class="section-title d1">Offres et promotions du moment</h2>
      <p v-reveal class="section-lead d2">Profitez de nos offres en cours et faites-nous savoir ce que vous en pensez.</p>
      <div v-reveal="'scale'" class="d2">
        <PromotionCarousel :items="promotions.items" />
      </div>
      <div class="section-more">
        <RouterLink to="/promotions" class="btn-outline">Voir toutes nos offres →</RouterLink>
      </div>
    </div>
  </section>
</template>

<style scoped>
.offers {
  background: var(--bg-alt);
}
</style>
