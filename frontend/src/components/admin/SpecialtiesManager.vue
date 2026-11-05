<script setup lang="ts">
import { onMounted, ref } from "vue";

import Spinner from "@/components/common/Spinner.vue";
import { useAdmin } from "@/composables/useAdmin";
import { confirmDialog } from "@/composables/useDialog";
import { resolveSpecialtyIcon } from "@/constants/specialtyIcons";
import { mediaUrl } from "@/services/api";
import { useSpecialtiesStore } from "@/stores/specialties";

const specialties = useSpecialtiesStore();
const { editSpecialty } = useAdmin();
const removingId = ref<number | null>(null);
const togglingId = ref<number | null>(null);

onMounted(() => {
  specialties.fetchAdminAll();
});

async function remove(id: number) {
  const ok = await confirmDialog(
    "Supprimer cette spécialité ? Les médecins et questions fréquentes associés seront aussi supprimés.",
    { title: "Supprimer la spécialité", danger: true, confirmLabel: "Supprimer" },
  );
  if (!ok) return;
  removingId.value = id;
  try {
    await specialties.remove(id);
  } finally {
    removingId.value = null;
  }
}

async function toggle(id: number) {
  togglingId.value = id;
  try {
    await specialties.toggleActive(id);
  } finally {
    togglingId.value = null;
  }
}
</script>

<template>
  <div>
    <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 14px">
      <div class="a-sec-title" style="margin: 0">Spécialités médicales</div>
      <button class="ab ab-gold" style="font-size: 0.78rem" @click="editSpecialty(null)">
        + Nouvelle spécialité
      </button>
    </div>
    <div id="specialties-admin-list">
      <div v-for="s in specialties.adminItems" :key="s.id" class="art-item">
        <img
          v-if="s.media_type === 'image' && mediaUrl(s.cover_image_url)"
          :src="mediaUrl(s.cover_image_url)!"
          alt=""
          style="width: 28px; height: 28px; border-radius: 6px; object-fit: cover; flex-shrink: 0"
        />
        <component
          v-else
          :is="resolveSpecialtyIcon(s.icon_name).component"
          :size="20"
          style="flex-shrink: 0; color: var(--a-gold)"
        />
        <span class="art-title-txt" style="font-weight: 600; flex: 0 0 auto; min-width: 160px">{{ s.name }}</span>
        <span style="font-size: 0.78rem; color: var(--a-muted); flex: 1">{{ s.description }}</span>
        <span class="msg-badge" :class="s.is_active ? 'mb-new' : 'mb-read'">
          {{ s.is_active ? "Active" : "Masquée" }}
        </span>
        <button class="a-btn-sm" :disabled="togglingId === s.id" @click="toggle(s.id)">
          <Spinner v-if="togglingId === s.id" :size="11" />
          <span v-else>{{ s.is_active ? "Masquer" : "Activer" }}</span>
        </button>
        <button class="a-btn-sm" @click="editSpecialty(s.id)">Modifier</button>
        <button class="a-btn-sm del" :disabled="removingId === s.id" @click="remove(s.id)">
          <Spinner v-if="removingId === s.id" :size="11" />
          <span v-else>✕</span>
        </button>
      </div>
      <p v-if="!specialties.adminItems.length" style="color: var(--a-muted); font-size: 0.85rem">
        Aucune spécialité pour le moment.
      </p>
    </div>
  </div>
</template>
