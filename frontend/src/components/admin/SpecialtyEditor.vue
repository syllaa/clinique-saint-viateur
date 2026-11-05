<script setup lang="ts">
import { computed, onMounted, ref, watch } from "vue";

import IconPicker from "@/components/admin/IconPicker.vue";
import Spinner from "@/components/common/Spinner.vue";
import { useAdmin } from "@/composables/useAdmin";
import { alertDialog, confirmDialog } from "@/composables/useDialog";
import { mediaUrl } from "@/services/api";
import type { SpecialtyMediaType } from "@/services/specialtyService";
import { uploadService } from "@/services/uploadService";
import SpecialtyMedia from "@/components/specialties/SpecialtyMedia.vue";
import { useSpecialtiesStore } from "@/stores/specialties";

const specialties = useSpecialtiesStore();
const { editingSpecialtyId, setTab } = useAdmin();

const currentId = ref<number | null>(null);
const isEdit = computed(() => currentId.value !== null);

const name = ref("");
const description = ref("");
const fullDescription = ref("");
const servicesOffered = ref("");
const symptomsText = ref("");
const consultationHours = ref("");
const practicalInfo = ref("");
const seoTitle = ref("");
const seoDescription = ref("");

const mediaType = ref<SpecialtyMediaType>("icon");
const iconName = ref<string | null>(null);
const coverImageUrl = ref<string | null>(null);
const imageAlt = ref("");

const saving = ref(false);
const uploadingImage = ref(false);
const savedOk = ref(false);

const newDoctorName = ref("");
const newDoctorTitle = ref("");
const addingDoctor = ref(false);
const removingDoctorId = ref<number | null>(null);

const newFaqQuestion = ref("");
const newFaqAnswer = ref("");
const addingFaq = ref(false);
const removingFaqId = ref<number | null>(null);

function resetForm() {
  name.value = "";
  description.value = "";
  fullDescription.value = "";
  servicesOffered.value = "";
  symptomsText.value = "";
  consultationHours.value = "";
  practicalInfo.value = "";
  seoTitle.value = "";
  seoDescription.value = "";
  mediaType.value = "icon";
  iconName.value = null;
  coverImageUrl.value = null;
  imageAlt.value = "";
}

async function loadForEdit(id: number) {
  const specialty = await specialties.fetchByIdAdmin(id);
  if (!specialty) return;
  name.value = specialty.name;
  description.value = specialty.description;
  fullDescription.value = specialty.full_description;
  servicesOffered.value = specialty.services_offered;
  symptomsText.value = specialty.symptoms_text || "";
  consultationHours.value = specialty.consultation_hours || "";
  practicalInfo.value = specialty.practical_info || "";
  seoTitle.value = specialty.seo_title || "";
  seoDescription.value = specialty.seo_description || "";
  mediaType.value = specialty.media_type;
  iconName.value = specialty.icon_name;
  coverImageUrl.value = specialty.cover_image_url;
  imageAlt.value = specialty.image_alt || "";
}

onMounted(() => {
  currentId.value = editingSpecialtyId.value;
  if (currentId.value) loadForEdit(currentId.value);
  else resetForm();
});

watch(editingSpecialtyId, (id) => {
  currentId.value = id;
  if (id) loadForEdit(id);
  else resetForm();
});

async function onImageChange(e: Event) {
  const input = e.target as HTMLInputElement;
  const file = input.files?.[0];
  if (!file) return;
  uploadingImage.value = true;
  try {
    coverImageUrl.value = await uploadService.uploadImage(file);
  } catch {
    await alertDialog("Échec de l'envoi de l'image (format JPG/PNG/WEBP requis, 5 Mo max).", {
      title: "Erreur d'upload",
    });
  } finally {
    uploadingImage.value = false;
    input.value = "";
  }
}

async function removeImage() {
  const ok = await confirmDialog("Voulez-vous vraiment supprimer cette image ?", {
    title: "Supprimer l'image",
    danger: true,
    confirmLabel: "Supprimer",
  });
  if (!ok) return;
  coverImageUrl.value = null;
  imageAlt.value = "";
  mediaType.value = "icon";
}

async function save() {
  if (!name.value.trim()) {
    await alertDialog("Le nom de la spécialité est requis.", { title: "Champ requis" });
    return;
  }
  if (mediaType.value === "image" && !coverImageUrl.value) {
    await alertDialog("Veuillez téléverser une image, ou choisissez plutôt une icône.", {
      title: "Image requise",
    });
    return;
  }
  saving.value = true;
  try {
    const payload = {
      name: name.value.trim(),
      description: description.value.trim(),
      full_description: fullDescription.value.trim(),
      services_offered: servicesOffered.value.trim(),
      symptoms_text: symptomsText.value.trim() || null,
      consultation_hours: consultationHours.value.trim() || null,
      practical_info: practicalInfo.value.trim() || null,
      seo_title: seoTitle.value.trim() || null,
      seo_description: seoDescription.value.trim() || null,
      media_type: mediaType.value,
      icon_name: mediaType.value === "icon" ? iconName.value : null,
      cover_image_url: mediaType.value === "image" ? coverImageUrl.value : null,
      image_alt: mediaType.value === "image" ? imageAlt.value.trim() || null : null,
    };
    if (isEdit.value && currentId.value) {
      await specialties.update(currentId.value, payload);
    } else {
      const created = await specialties.create(payload);
      currentId.value = created.id;
      editingSpecialtyId.value = created.id;
      await loadForEdit(created.id);
    }
    await specialties.fetchAdminAll();
    savedOk.value = true;
    setTimeout(() => (savedOk.value = false), 3000);
  } catch {
    await alertDialog("Impossible d'enregistrer la spécialité. Vérifiez les champs et réessayez.", {
      title: "Erreur",
    });
  } finally {
    saving.value = false;
  }
}

async function addDoctor() {
  if (!currentId.value || !newDoctorName.value.trim()) return;
  addingDoctor.value = true;
  try {
    await specialties.addDoctor(currentId.value, {
      name: newDoctorName.value.trim(),
      title: newDoctorTitle.value.trim() || undefined,
    });
    newDoctorName.value = "";
    newDoctorTitle.value = "";
  } finally {
    addingDoctor.value = false;
  }
}

async function removeDoctorRow(id: number) {
  removingDoctorId.value = id;
  try {
    await specialties.removeDoctor(id);
  } finally {
    removingDoctorId.value = null;
  }
}

async function addFaqRow() {
  if (!currentId.value || !newFaqQuestion.value.trim() || !newFaqAnswer.value.trim()) return;
  addingFaq.value = true;
  try {
    await specialties.addFaq(currentId.value, {
      question: newFaqQuestion.value.trim(),
      answer: newFaqAnswer.value.trim(),
    });
    newFaqQuestion.value = "";
    newFaqAnswer.value = "";
  } finally {
    addingFaq.value = false;
  }
}

async function removeFaqRow(id: number) {
  removingFaqId.value = id;
  try {
    await specialties.removeFaq(id);
  } finally {
    removingFaqId.value = null;
  }
}
</script>

<template>
  <div>
    <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 14px">
      <div class="a-sec-title" style="margin: 0">
        {{ isEdit ? "Modifier la spécialité" : "Nouvelle spécialité" }}
      </div>
      <button class="back-link" style="margin-top: 0" @click="setTab('specialties-list')">← Retour à la liste</button>
    </div>

    <div class="editor-layout">
      <div class="editor-panel">
        <label class="al">Nom de la spécialité</label>
        <input class="ai" v-model="name" type="text" placeholder="Ex : Cardiologie" />

        <label class="al">Description courte (carte)</label>
        <input class="ai" v-model="description" type="text" placeholder="Résumé affiché sur la carte…" />

        <label class="al">Présentation complète</label>
        <textarea class="ai a-textarea" v-model="fullDescription" placeholder="Présentation détaillée de la spécialité…"></textarea>

        <label class="al">Services proposés (un par ligne)</label>
        <textarea class="ai a-textarea" style="min-height: 100px" v-model="servicesOffered" placeholder="Consultation…&#10;Suivi…"></textarea>

        <label class="al">Symptômes / motifs de consultation (optionnel)</label>
        <textarea class="ai a-textarea" style="min-height: 90px" v-model="symptomsText"></textarea>

        <label class="al">Informations pratiques (optionnel)</label>
        <textarea class="ai a-textarea" style="min-height: 90px" v-model="practicalInfo"></textarea>

        <div v-if="isEdit" style="margin-top: 8px; padding-top: 18px; border-top: 1px solid var(--a-border)">
          <div class="a-sec-title">Médecins associés</div>
          <div v-for="d in specialties.current?.doctors ?? []" :key="d.id" class="art-item">
            <span class="art-title-txt" style="font-weight: 600">{{ d.name }}</span>
            <span style="font-size: 0.78rem; color: var(--a-muted); flex: 1">{{ d.title }}</span>
            <button class="a-btn-sm del" :disabled="removingDoctorId === d.id" @click="removeDoctorRow(d.id)">
              <Spinner v-if="removingDoctorId === d.id" :size="11" />
              <span v-else>✕</span>
            </button>
          </div>
          <div style="display: grid; grid-template-columns: 1fr 1fr auto; gap: 10px; align-items: end; margin-top: 10px">
            <div>
              <label class="al">Nom</label>
              <input class="ai" v-model="newDoctorName" type="text" placeholder="Dr. Koffi…" style="margin-bottom: 0" />
            </div>
            <div>
              <label class="al">Titre</label>
              <input class="ai" v-model="newDoctorTitle" type="text" placeholder="Cardiologue…" style="margin-bottom: 0" />
            </div>
            <button class="ab ab-sec" :disabled="addingDoctor" @click="addDoctor">
              <span class="btn-content"><Spinner v-if="addingDoctor" :size="12" />+ Ajouter</span>
            </button>
          </div>
        </div>

        <div v-if="isEdit" style="margin-top: 22px; padding-top: 18px; border-top: 1px solid var(--a-border)">
          <div class="a-sec-title">Questions fréquentes</div>
          <div v-for="f in specialties.current?.faqs ?? []" :key="f.id" class="art-item" style="align-items: flex-start">
            <div style="flex: 1">
              <div class="art-title-txt" style="font-weight: 600">{{ f.question }}</div>
              <div style="font-size: 0.78rem; color: var(--a-muted); margin-top: 4px">{{ f.answer }}</div>
            </div>
            <button class="a-btn-sm del" :disabled="removingFaqId === f.id" @click="removeFaqRow(f.id)">
              <Spinner v-if="removingFaqId === f.id" :size="11" />
              <span v-else>✕</span>
            </button>
          </div>
          <div style="margin-top: 10px">
            <label class="al">Question</label>
            <input class="ai" v-model="newFaqQuestion" type="text" placeholder="Faut-il être à jeun ?" />
            <label class="al">Réponse</label>
            <textarea class="ai a-textarea" style="min-height: 70px" v-model="newFaqAnswer"></textarea>
            <button class="ab ab-sec" :disabled="addingFaq" @click="addFaqRow">
              <span class="btn-content"><Spinner v-if="addingFaq" :size="12" />+ Ajouter la question</span>
            </button>
          </div>
        </div>

        <div class="ab-row" style="margin-top: 20px">
          <button class="ab ab-gold" :disabled="saving" @click="save">
            <span class="btn-content"><Spinner v-if="saving" :size="14" />{{ saving ? "Enregistrement…" : isEdit ? "Enregistrer les modifications" : "Créer la spécialité" }}</span>
          </button>
        </div>
        <div v-if="savedOk" class="art-success">✓ Spécialité enregistrée.</div>
        <p v-if="!isEdit" style="font-size: 0.74rem; color: var(--a-muted); margin-top: 10px">
          Créez d'abord la spécialité pour pouvoir y ajouter des médecins et des questions fréquentes.
        </p>
      </div>

      <div class="editor-sidebar">
        <div class="a-sec-title" style="margin-bottom: 10px">Média de la spécialité</div>
        <div class="media-toggle">
          <label class="media-radio" :class="{ on: mediaType === 'icon' }">
            <input type="radio" value="icon" v-model="mediaType" />
            <span class="media-radio-dot"></span>
            Icône par défaut
          </label>
          <label class="media-radio" :class="{ on: mediaType === 'image' }">
            <input type="radio" value="image" v-model="mediaType" />
            <span class="media-radio-dot"></span>
            Image personnalisée
          </label>
        </div>

        <IconPicker v-if="mediaType === 'icon'" v-model="iconName" />

        <template v-else>
          <div v-if="!coverImageUrl" class="media-dropzone">
            <input
              id="specialty-image-input"
              type="file"
              accept="image/jpeg,image/jpg,image/png,image/webp"
              style="display: none"
              @change="onImageChange"
            />
            <label for="specialty-image-input" class="media-dropzone-label">
              <span style="font-size: 1.5rem">📤</span>
              <span>Glissez votre image ici ou cliquez pour parcourir</span>
              <span class="media-dropzone-hint">JPG, JPEG, PNG, WEBP — 5 Mo max</span>
            </label>
          </div>
          <div v-else class="media-image-preview">
            <img :src="mediaUrl(coverImageUrl)!" alt="" />
            <div class="media-image-actions">
              <label for="specialty-image-replace" class="a-btn-sm">Remplacer</label>
              <input
                id="specialty-image-replace"
                type="file"
                accept="image/jpeg,image/jpg,image/png,image/webp"
                style="display: none"
                @change="onImageChange"
              />
              <button class="a-btn-sm del" type="button" @click="removeImage">Supprimer</button>
            </div>
          </div>
          <div v-if="uploadingImage" class="media-uploading"><Spinner :size="14" /> Envoi en cours…</div>

          <label class="al" style="margin-top: 12px">Texte alternatif</label>
          <input class="ai" v-model="imageAlt" type="text" placeholder="Décrivez l'image (accessibilité)…" />
        </template>

        <div class="media-preview-block">
          <div class="a-sec-title" style="margin-bottom: 8px">Aperçu</div>
          <SpecialtyMedia
            :media-type="mediaType"
            :icon-name="iconName"
            :image-url="coverImageUrl"
            :image-alt="imageAlt"
            :name="name || 'Spécialité'"
          />
        </div>

        <label class="al" style="margin-top: 14px">Horaires de consultation</label>
        <input class="ai" v-model="consultationHours" type="text" placeholder="Lun–Ven 08h–18h" />

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

<style scoped>
.media-toggle {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 14px;
}
.media-radio {
  display: flex;
  align-items: center;
  gap: 9px;
  padding: 10px 13px;
  border: 1.5px solid var(--a-border);
  border-radius: 8px;
  background: var(--a-tint);
  font-size: 0.82rem;
  color: var(--a-text-2);
  cursor: pointer;
  transition: all 0.15s;
}
.media-radio input {
  display: none;
}
.media-radio-dot {
  width: 15px;
  height: 15px;
  border-radius: 50%;
  border: 1.5px solid var(--a-border);
  flex-shrink: 0;
  position: relative;
}
.media-radio.on {
  border-color: var(--a-gold);
  background: rgba(224, 71, 90, 0.1);
  color: var(--a-text);
}
.media-radio.on .media-radio-dot {
  border-color: var(--a-gold);
}
.media-radio.on .media-radio-dot::after {
  content: "";
  position: absolute;
  inset: 3px;
  border-radius: 50%;
  background: var(--a-gold);
}
.media-dropzone {
  border: 1.5px dashed var(--a-border);
  border-radius: 10px;
  padding: 26px 14px;
  text-align: center;
  margin-bottom: 10px;
  transition: border-color 0.2s;
}
.media-dropzone:hover {
  border-color: var(--a-gold);
}
.media-dropzone-label {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
  cursor: pointer;
  font-size: 0.8rem;
  color: var(--a-text-2);
}
.media-dropzone-hint {
  font-size: 0.68rem;
  color: var(--a-muted);
}
.media-image-preview img {
  width: 100%;
  border-radius: 8px;
  display: block;
  margin-bottom: 8px;
}
.media-image-actions {
  display: flex;
  gap: 8px;
  margin-bottom: 10px;
}
.media-image-actions .a-btn-sm {
  display: inline-flex;
  align-items: center;
}
.media-uploading {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.76rem;
  color: var(--a-muted);
  margin-bottom: 10px;
}
.media-preview-block {
  padding-top: 14px;
  margin-top: 14px;
  border-top: 1px solid var(--a-border);
}
.media-preview-block :deep(.specialty-media.card) {
  width: 70px;
  height: 70px;
}
.media-preview-block :deep(.specialty-media.card.is-image) {
  width: 100%;
  height: 130px;
}
</style>
