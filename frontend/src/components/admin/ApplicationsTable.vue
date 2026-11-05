<script setup lang="ts">
import { onMounted, ref } from "vue";

import Spinner from "@/components/common/Spinner.vue";
import type { JobApplication } from "@/services/jobService";
import { useJobApplicationsStore } from "@/stores/jobApplications";
import { useJobOffersStore } from "@/stores/jobOffers";

const STATUS_LABELS: Record<string, string> = {
  nouvelle: "Nouvelle",
  en_cours: "En cours d'étude",
  retenue: "Retenue",
  rejetee: "Rejetée",
};

const applications = useJobApplicationsStore();
const jobs = useJobOffersStore();
const updatingId = ref<number | null>(null);
const downloadingId = ref<number | null>(null);
const selected = ref<JobApplication | null>(null);

onMounted(() => {
  applications.fetchAll();
  if (!jobs.adminItems.length) jobs.fetchAdminAll();
});

function offerTitle(offerId: number) {
  return jobs.adminItems.find((o) => o.id === offerId)?.title || `Offre #${offerId}`;
}

async function changeStatus(id: number, status: string) {
  updatingId.value = id;
  try {
    await applications.updateStatus(id, status);
  } finally {
    updatingId.value = null;
  }
}

async function downloadCv(app: JobApplication) {
  downloadingId.value = app.id;
  try {
    await applications.downloadCv(app.id, `CV_${app.last_name}_${app.first_name}.pdf`);
  } finally {
    downloadingId.value = null;
  }
}
</script>

<template>
  <div>
    <div class="a-sec-title">Candidatures reçues</div>
    <table class="a-table">
      <thead>
        <tr>
          <th>Candidat</th>
          <th>Poste</th>
          <th>Contact</th>
          <th>Date</th>
          <th>Statut</th>
          <th>Action</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="a in applications.items" :key="a.id">
          <td style="font-weight: 500; color: var(--a-text); cursor: pointer" @click="selected = a">
            {{ a.first_name }} {{ a.last_name }}
          </td>
          <td>{{ offerTitle(a.job_offer_id) }}</td>
          <td style="font-size: 0.75rem">{{ a.email }}<br />{{ a.phone }}</td>
          <td style="white-space: nowrap; font-size: 0.75rem">
            {{ new Date(a.created_at).toLocaleDateString("fr-FR") }}
          </td>
          <td>
            <select
              class="ai"
              style="margin-bottom: 0; padding: 5px 8px; font-size: 0.72rem"
              :value="a.status"
              :disabled="updatingId === a.id"
              @change="changeStatus(a.id, ($event.target as HTMLSelectElement).value)"
            >
              <option v-for="(label, key) in STATUS_LABELS" :key="key" :value="key">{{ label }}</option>
            </select>
          </td>
          <td>
            <button class="a-btn-sm" :disabled="downloadingId === a.id" @click="downloadCv(a)">
              <Spinner v-if="downloadingId === a.id" :size="11" />
              <span v-else>📄 CV</span>
            </button>
          </td>
        </tr>
      </tbody>
    </table>
    <p v-if="!applications.items.length" style="color: var(--a-muted); font-size: 0.85rem; margin-top: 14px">
      Aucune candidature reçue pour le moment.
    </p>

    <div v-if="selected" class="a-modal-over on" @click.self="selected = null">
      <div class="a-modal">
        <h3>Candidature de {{ selected.first_name }} {{ selected.last_name }}</h3>
        <div class="mf"><label>Poste</label><p>{{ offerTitle(selected.job_offer_id) }}</p></div>
        <div class="mf"><label>Email</label><p>{{ selected.email }}</p></div>
        <div class="mf"><label>Téléphone</label><p>{{ selected.phone }}</p></div>
        <div class="mf"><label>Lettre de motivation</label><p style="white-space: pre-wrap">{{ selected.cover_letter || "—" }}</p></div>
        <div class="mf"><label>Date de candidature</label><p>{{ new Date(selected.created_at).toLocaleString("fr-FR") }}</p></div>
        <div class="a-modal-foot">
          <button class="ab ab-gold" @click="downloadCv(selected)">📄 Télécharger le CV</button>
          <button class="ab ab-sec" @click="selected = null">Fermer</button>
        </div>
      </div>
    </div>
  </div>
</template>
