<script setup lang="ts">
import { onMounted, ref } from "vue";

import Spinner from "@/components/common/Spinner.vue";
import { alertDialog, confirmDialog } from "@/composables/useDialog";
import { useBackupsStore } from "@/stores/backups";

const backups = useBackupsStore();
const loading = ref(true);
const creating = ref(false);
const downloadingFile = ref<string | null>(null);
const removingFile = ref<string | null>(null);

onMounted(async () => {
  loading.value = true;
  try {
    await backups.fetchAll();
  } finally {
    loading.value = false;
  }
});

function formatSize(bytes: number) {
  if (bytes < 1024) return `${bytes} o`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(0)} Ko`;
  return `${(bytes / (1024 * 1024)).toFixed(1)} Mo`;
}

function formatDate(iso: string) {
  return new Date(iso).toLocaleString("fr-FR", {
    day: "2-digit",
    month: "2-digit",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
}

async function createNow() {
  creating.value = true;
  try {
    await backups.create();
  } catch {
    await alertDialog(
      "Impossible de créer la sauvegarde. Vérifiez que mysqldump est correctement configuré (MYSQLDUMP_PATH).",
      { title: "Échec de la sauvegarde" },
    );
  } finally {
    creating.value = false;
  }
}

async function downloadOne(filename: string) {
  downloadingFile.value = filename;
  try {
    await backups.download(filename);
  } finally {
    downloadingFile.value = null;
  }
}

async function removeOne(filename: string) {
  const ok = await confirmDialog(`Supprimer définitivement la sauvegarde « ${filename} » ?`, {
    title: "Supprimer la sauvegarde",
    danger: true,
    confirmLabel: "Supprimer",
  });
  if (!ok) return;
  removingFile.value = filename;
  try {
    await backups.remove(filename);
  } finally {
    removingFile.value = null;
  }
}
</script>

<template>
  <div>
    <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 14px">
      <div class="a-sec-title" style="margin: 0">Sauvegardes de la base de données</div>
      <button class="ab ab-gold" :disabled="creating" @click="createNow">
        <span class="btn-content"><Spinner v-if="creating" :size="14" />{{ creating ? "Sauvegarde en cours…" : "🗄 Sauvegarder maintenant" }}</span>
      </button>
    </div>

    <p style="font-size: 0.8rem; color: var(--a-muted); margin-bottom: 16px">
      Une sauvegarde automatique complète de la base de données est effectuée toutes les 24 heures et conservée
      14 jours. Vous pouvez aussi déclencher une sauvegarde manuelle à tout moment.
    </p>

    <div v-if="loading" style="padding: 30px 0; display: flex; justify-content: center"><Spinner :size="24" /></div>

    <div v-else id="backups-list">
      <div v-for="b in backups.items" :key="b.filename" class="art-item">
        <span class="art-title-txt" style="font-family: monospace; font-size: 0.78rem">{{ b.filename }}</span>
        <span style="font-size: 0.78rem; color: var(--a-muted)">{{ formatDate(b.created_at) }}</span>
        <span style="font-size: 0.78rem; color: var(--a-muted)">{{ formatSize(b.size_bytes) }}</span>
        <button class="a-btn-sm" :disabled="downloadingFile === b.filename" @click="downloadOne(b.filename)">
          <Spinner v-if="downloadingFile === b.filename" :size="11" />
          <span v-else>Télécharger</span>
        </button>
        <button class="a-btn-sm del" :disabled="removingFile === b.filename" @click="removeOne(b.filename)">
          <Spinner v-if="removingFile === b.filename" :size="11" />
          <span v-else>✕</span>
        </button>
      </div>
      <p v-if="!backups.items.length" style="color: var(--a-muted); font-size: 0.85rem">
        Aucune sauvegarde pour le moment.
      </p>
    </div>
  </div>
</template>
