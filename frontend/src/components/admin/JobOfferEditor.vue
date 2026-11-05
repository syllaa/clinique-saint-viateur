<script setup lang="ts">
import { computed, onMounted, ref, watch } from "vue";

import RichTextEditor from "@/components/admin/RichTextEditor.vue";
import Spinner from "@/components/common/Spinner.vue";
import { useAdmin } from "@/composables/useAdmin";
import { alertDialog } from "@/composables/useDialog";
import { useJobOffersStore } from "@/stores/jobOffers";

const CONTRACT_TYPES = ["CDI", "CDD", "Stage", "Freelance"];

const jobs = useJobOffersStore();
const { editingJobOfferId, setTab } = useAdmin();

const currentId = ref<number | null>(null);
const isEdit = computed(() => currentId.value !== null);

const title = ref("");
const department = ref("");
const contractType = ref(CONTRACT_TYPES[0]);
const location = ref("Cocody, Abidjan");
const shortDescription = ref("");
const description = ref("");
const missions = ref("");
const profileRequirements = ref("");
const skills = ref("");
const experienceLevel = ref("");
const applicationDeadline = ref("");
const seoTitle = ref("");
const seoDescription = ref("");
const status = ref<"published" | "draft">("published");

const saving = ref(false);
const savedOk = ref(false);

function resetForm() {
  title.value = "";
  department.value = "";
  contractType.value = CONTRACT_TYPES[0];
  location.value = "Cocody, Abidjan";
  shortDescription.value = "";
  description.value = "";
  missions.value = "";
  profileRequirements.value = "";
  skills.value = "";
  experienceLevel.value = "";
  applicationDeadline.value = "";
  seoTitle.value = "";
  seoDescription.value = "";
  status.value = "published";
}

async function loadForEdit(id: number) {
  const offer = await jobs.fetchByIdAdmin(id);
  if (!offer) return;
  title.value = offer.title;
  department.value = offer.department || "";
  contractType.value = offer.contract_type;
  location.value = offer.location;
  shortDescription.value = offer.short_description;
  description.value = offer.description;
  missions.value = offer.missions || "";
  profileRequirements.value = offer.profile_requirements || "";
  skills.value = offer.skills || "";
  experienceLevel.value = offer.experience_level || "";
  applicationDeadline.value = offer.application_deadline || "";
  seoTitle.value = offer.seo_title || "";
  seoDescription.value = offer.seo_description || "";
  status.value = offer.status as "published" | "draft";
}

onMounted(() => {
  currentId.value = editingJobOfferId.value;
  if (currentId.value) loadForEdit(currentId.value);
  else resetForm();
});

watch(editingJobOfferId, (id) => {
  currentId.value = id;
  if (id) loadForEdit(id);
  else resetForm();
});

async function save() {
  if (!title.value.trim()) {
    await alertDialog("Le titre du poste est requis.", { title: "Champ requis" });
    return;
  }
  saving.value = true;
  try {
    const payload = {
      title: title.value.trim(),
      department: department.value.trim() || null,
      contract_type: contractType.value,
      location: location.value.trim() || "Cocody, Abidjan",
      short_description: shortDescription.value.trim(),
      description: description.value,
      missions: missions.value.trim() || null,
      profile_requirements: profileRequirements.value.trim() || null,
      skills: skills.value.trim() || null,
      experience_level: experienceLevel.value.trim() || null,
      application_deadline: applicationDeadline.value || null,
      seo_title: seoTitle.value.trim() || null,
      seo_description: seoDescription.value.trim() || null,
      status: status.value,
    };
    if (isEdit.value && currentId.value) {
      await jobs.update(currentId.value, payload);
    } else {
      const created = await jobs.create(payload);
      currentId.value = created.id;
      editingJobOfferId.value = created.id;
    }
    await jobs.fetchAdminAll();
    savedOk.value = true;
    setTimeout(() => (savedOk.value = false), 3000);
  } finally {
    saving.value = false;
  }
}
</script>

<template>
  <div>
    <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 14px">
      <div class="a-sec-title" style="margin: 0">{{ isEdit ? "Modifier l'offre" : "Nouvelle offre" }}</div>
      <button class="back-link" style="margin-top: 0" @click="setTab('jobs-list')">← Retour à la liste</button>
    </div>

    <div class="editor-layout">
      <div class="editor-panel">
        <label class="al">Intitulé du poste</label>
        <input class="ai" v-model="title" type="text" placeholder="Ex : Infirmier(ère) diplômé(e) d'État" />

        <label class="al">Description courte (carte)</label>
        <input class="ai" v-model="shortDescription" type="text" placeholder="Résumé affiché sur la carte…" />

        <label class="al">Description complète</label>
        <RichTextEditor v-model="description" />

        <label class="al">Missions</label>
        <textarea class="ai a-textarea" style="min-height: 100px" v-model="missions"></textarea>

        <label class="al">Profil recherché</label>
        <textarea class="ai a-textarea" style="min-height: 100px" v-model="profileRequirements"></textarea>

        <label class="al">Compétences</label>
        <textarea class="ai a-textarea" style="min-height: 90px" v-model="skills"></textarea>

        <div class="ab-row" style="margin-top: 20px">
          <button class="ab ab-gold" :disabled="saving" @click="save">
            <span class="btn-content"><Spinner v-if="saving" :size="14" />{{ saving ? "Enregistrement…" : isEdit ? "Enregistrer les modifications" : "Créer l'offre" }}</span>
          </button>
        </div>
        <div v-if="savedOk" class="art-success">✓ Offre enregistrée.</div>
      </div>

      <div class="editor-sidebar">
        <label class="al">Département</label>
        <input class="ai" v-model="department" type="text" placeholder="Soins infirmiers…" />

        <label class="al">Type de contrat</label>
        <select class="ai" v-model="contractType">
          <option v-for="c in CONTRACT_TYPES" :key="c" :value="c">{{ c }}</option>
        </select>

        <label class="al">Localisation</label>
        <input class="ai" v-model="location" type="text" />

        <label class="al">Expérience requise</label>
        <input class="ai" v-model="experienceLevel" type="text" placeholder="2 ans minimum…" />

        <label class="al">Date limite de candidature</label>
        <input class="ai" v-model="applicationDeadline" type="date" />

        <label class="al">Statut</label>
        <select class="ai" v-model="status">
          <option value="published">Publiée</option>
          <option value="draft">Brouillon</option>
        </select>

        <div style="padding-top: 13px; border-top: 1px solid var(--a-border); margin-top: 4px">
          <div class="a-sec-title" style="margin-bottom: 10px">SEO</div>
          <label class="al">Titre SEO</label>
          <input class="ai" v-model="seoTitle" type="text" />
          <label class="al">Meta description</label>
          <textarea class="ai a-textarea" style="min-height: 70px" v-model="seoDescription"></textarea>
        </div>
      </div>
    </div>
  </div>
</template>
