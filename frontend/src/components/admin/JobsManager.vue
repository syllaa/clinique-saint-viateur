<script setup lang="ts">
import { onMounted, ref } from "vue";

import Spinner from "@/components/common/Spinner.vue";
import { useAdmin } from "@/composables/useAdmin";
import { confirmDialog } from "@/composables/useDialog";
import { useJobOffersStore } from "@/stores/jobOffers";

const jobs = useJobOffersStore();
const { editJobOffer } = useAdmin();
const removingId = ref<number | null>(null);
const togglingId = ref<number | null>(null);

onMounted(() => {
  jobs.fetchAdminAll();
});

async function remove(id: number) {
  const ok = await confirmDialog("Supprimer cette offre ? Les candidatures reçues seront aussi supprimées.", {
    title: "Supprimer l'offre",
    danger: true,
    confirmLabel: "Supprimer",
  });
  if (!ok) return;
  removingId.value = id;
  try {
    await jobs.remove(id);
  } finally {
    removingId.value = null;
  }
}

async function togglePublish(id: number, currentStatus: string) {
  togglingId.value = id;
  try {
    await jobs.update(id, { status: currentStatus === "published" ? "draft" : "published" });
  } finally {
    togglingId.value = null;
  }
}
</script>

<template>
  <div>
    <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 14px">
      <div class="a-sec-title" style="margin: 0">Offres d'emploi</div>
      <button class="ab ab-gold" style="font-size: 0.78rem" @click="editJobOffer(null)">+ Nouvelle offre</button>
    </div>
    <div id="jobs-admin-list">
      <div v-for="o in jobs.adminItems" :key="o.id" class="art-item">
        <span class="art-cat">{{ o.contract_type }}</span>
        <span class="art-title-txt">{{ o.title }}</span>
        <span style="font-size: 0.78rem; color: var(--a-muted)">{{ o.location }}</span>
        <span class="msg-badge" :class="o.status === 'published' ? 'mb-new' : 'mb-read'">
          {{ o.status === "published" ? "Publiée" : "Brouillon" }}
        </span>
        <button class="a-btn-sm" :disabled="togglingId === o.id" @click="togglePublish(o.id, o.status)">
          <Spinner v-if="togglingId === o.id" :size="11" />
          <span v-else>{{ o.status === "published" ? "Dépublier" : "Publier" }}</span>
        </button>
        <button class="a-btn-sm" @click="editJobOffer(o.id)">Modifier</button>
        <button class="a-btn-sm del" :disabled="removingId === o.id" @click="remove(o.id)">
          <Spinner v-if="removingId === o.id" :size="11" />
          <span v-else>✕</span>
        </button>
      </div>
      <p v-if="!jobs.adminItems.length" style="color: var(--a-muted); font-size: 0.85rem">
        Aucune offre d'emploi pour le moment.
      </p>
    </div>
  </div>
</template>
