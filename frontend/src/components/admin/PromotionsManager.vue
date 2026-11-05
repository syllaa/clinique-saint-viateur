<script setup lang="ts">
import { onMounted, ref } from "vue";

import Spinner from "@/components/common/Spinner.vue";
import { useAdmin } from "@/composables/useAdmin";
import { confirmDialog } from "@/composables/useDialog";
import { usePromotionsStore } from "@/stores/promotions";

const promotions = usePromotionsStore();
const { editPromotion } = useAdmin();
const removingId = ref<number | null>(null);
const togglingId = ref<number | null>(null);

onMounted(() => {
  promotions.fetchAdminAll();
});

async function remove(id: number) {
  const ok = await confirmDialog("Supprimer cette offre ? Les réactions reçues seront aussi supprimées.", {
    title: "Supprimer l'offre",
    danger: true,
    confirmLabel: "Supprimer",
  });
  if (!ok) return;
  removingId.value = id;
  try {
    await promotions.remove(id);
  } finally {
    removingId.value = null;
  }
}

async function toggle(id: number) {
  togglingId.value = id;
  try {
    await promotions.toggleActive(id);
  } finally {
    togglingId.value = null;
  }
}

function totalReactions(counts: Record<string, number>) {
  return Object.values(counts).reduce((sum, n) => sum + n, 0);
}
</script>

<template>
  <div>
    <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 14px">
      <div class="a-sec-title" style="margin: 0">Offres promotionnelles</div>
      <button class="ab ab-gold" style="font-size: 0.78rem" @click="editPromotion(null)">+ Nouvelle offre</button>
    </div>
    <div id="promotions-admin-list">
      <div v-for="p in promotions.adminItems" :key="p.id" class="art-item">
        <span v-if="p.category" class="art-cat">{{ p.category }}</span>
        <span class="art-title-txt">{{ p.title }}</span>
        <span style="font-size: 0.78rem; color: var(--a-muted)">
          Jusqu'au {{ new Date(p.valid_until).toLocaleDateString("fr-FR") }}
        </span>
        <span style="font-size: 0.78rem; color: var(--a-muted)">{{ totalReactions(p.reaction_counts) }} réaction(s)</span>
        <span class="msg-badge" :class="p.is_expired ? 'mb-read' : p.is_published ? 'mb-new' : 'mb-read'">
          {{ p.is_expired ? "Expirée" : p.is_published ? "Publiée" : "Brouillon" }}
        </span>
        <button class="a-btn-sm" :disabled="togglingId === p.id" @click="toggle(p.id)">
          <Spinner v-if="togglingId === p.id" :size="11" />
          <span v-else>{{ p.is_published ? "Dépublier" : "Publier" }}</span>
        </button>
        <button class="a-btn-sm" @click="editPromotion(p.id)">Modifier</button>
        <button class="a-btn-sm del" :disabled="removingId === p.id" @click="remove(p.id)">
          <Spinner v-if="removingId === p.id" :size="11" />
          <span v-else>✕</span>
        </button>
      </div>
      <p v-if="!promotions.adminItems.length" style="color: var(--a-muted); font-size: 0.85rem">
        Aucune offre promotionnelle pour le moment.
      </p>
    </div>
  </div>
</template>
