<script setup lang="ts">
import { onMounted, ref } from "vue";

import Spinner from "@/components/common/Spinner.vue";
import { confirmDialog } from "@/composables/useDialog";
import type { SiteMessage } from "@/services/siteService";
import { useMessagesStore } from "@/stores/messages";

const messages = useMessagesStore();
const selected = ref<SiteMessage | null>(null);
const markingAll = ref(false);
const removingId = ref<number | null>(null);

onMounted(() => {
  messages.fetchAll();
});

async function view(message: SiteMessage) {
  selected.value = message;
  if (message.status === "new") await messages.markRead(message.id);
}

function closeModal() {
  selected.value = null;
}

async function markAllRead() {
  markingAll.value = true;
  try {
    await messages.markAllRead();
  } finally {
    markingAll.value = false;
  }
}

async function remove(id: number) {
  const ok = await confirmDialog("Supprimer ce message ?", {
    title: "Supprimer ce message",
    danger: true,
    confirmLabel: "Supprimer",
  });
  if (!ok) return;
  removingId.value = id;
  try {
    await messages.remove(id);
    if (selected.value?.id === id) selected.value = null;
  } finally {
    removingId.value = null;
  }
}
</script>

<template>
  <div>
    <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 14px">
      <div class="a-sec-title" style="margin: 0">Boîte de réception</div>
      <button class="ab ab-sec" style="font-size: 0.73rem" :disabled="markingAll" @click="markAllRead">
        <span class="btn-content"><Spinner v-if="markingAll" :size="12" />{{ markingAll ? "Marquage…" : "Tout marquer comme lu" }}</span>
      </button>
    </div>
    <table class="a-table">
      <thead>
        <tr>
          <th>Nom</th>
          <th>Email</th>
          <th>Service</th>
          <th>Message</th>
          <th>Date</th>
          <th>Statut</th>
          <th>Action</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="m in messages.items" :key="m.id">
          <td style="font-weight: 500; color: var(--a-text)">{{ m.name }}</td>
          <td>{{ m.email || "—" }}</td>
          <td>{{ m.subject }}</td>
          <td style="max-width: 160px; overflow: hidden; white-space: nowrap; text-overflow: ellipsis">
            {{ m.content }}
          </td>
          <td style="white-space: nowrap; font-size: 0.75rem">
            {{ new Date(m.created_at).toLocaleString("fr-FR") }}
          </td>
          <td>
            <span class="msg-badge" :class="m.status === 'new' ? 'mb-new' : 'mb-read'">
              {{ m.status === "new" ? "Nouveau" : "Lu" }}
            </span>
          </td>
          <td>
            <button class="a-btn-sm" @click="view(m)">Voir</button>
            <button class="a-btn-sm del" style="margin-left: 4px" :disabled="removingId === m.id" @click="remove(m.id)">
              <Spinner v-if="removingId === m.id" :size="11" />
              <span v-else>✕</span>
            </button>
          </td>
        </tr>
      </tbody>
    </table>

    <div v-if="selected" class="a-modal-over on" @click.self="closeModal">
      <div class="a-modal">
        <h3>Détail du message</h3>
        <div class="mf"><label>Expéditeur</label><p>{{ selected.name }}</p></div>
        <div class="mf"><label>Email</label><p>{{ selected.email || "—" }}</p></div>
        <div class="mf"><label>Téléphone</label><p>{{ selected.phone || "—" }}</p></div>
        <div class="mf"><label>Service recherché</label><p>{{ selected.subject }}</p></div>
        <div class="mf"><label>Type de demande</label><p>{{ selected.urgency === "urgence" ? "Urgence" : "Rendez-vous programmé" }}</p></div>
        <div class="mf"><label>Infos hospitalisation / soins intensifs</label><p>{{ selected.wants_hospitalization_info ? "Oui" : "Non" }}</p></div>
        <div class="mf"><label>Demande</label><p style="white-space: pre-wrap">{{ selected.content }}</p></div>
        <div class="mf"><label>Date de réception</label><p>{{ new Date(selected.created_at).toLocaleString("fr-FR") }}</p></div>
        <div class="a-modal-foot">
          <button class="ab ab-danger" :disabled="removingId === selected.id" @click="remove(selected.id)">
            <span class="btn-content"><Spinner v-if="removingId === selected.id" :size="13" />{{ removingId === selected.id ? "Suppression…" : "Supprimer" }}</span>
          </button>
          <button class="ab ab-sec" @click="closeModal">Fermer</button>
        </div>
      </div>
    </div>
  </div>
</template>
