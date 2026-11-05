<script setup lang="ts">
import { computed, onMounted, ref, watch } from "vue";

import Spinner from "@/components/common/Spinner.vue";
import { useAdmin } from "@/composables/useAdmin";
import { alertDialog, confirmDialog } from "@/composables/useDialog";
import { mediaUrl } from "@/services/api";
import { uploadService } from "@/services/uploadService";
import { usePromotionsStore } from "@/stores/promotions";

const promotions = usePromotionsStore();
const { editingPromotionId, setTab } = useAdmin();

const currentId = ref<number | null>(null);
const isEdit = computed(() => currentId.value !== null);

const title = ref("");
const shortDescription = ref("");
const valueLabel = ref("");
const category = ref("");
const validUntil = ref("");
const isPublished = ref(true);
const coverImageUrl = ref<string | null>(null);
const imageAlt = ref("");

const saving = ref(false);
const uploadingImage = ref(false);
const savedOk = ref(false);

function resetForm() {
  title.value = "";
  shortDescription.value = "";
  valueLabel.value = "";
  category.value = "";
  validUntil.value = "";
  isPublished.value = true;
  coverImageUrl.value = null;
  imageAlt.value = "";
}

async function loadForEdit(id: number) {
  const promotion = await promotions.fetchByIdAdmin(id);
  if (!promotion) return;
  title.value = promotion.title;
  shortDescription.value = promotion.short_description;
  valueLabel.value = promotion.value_label;
  category.value = promotion.category || "";
  validUntil.value = promotion.valid_until;
  isPublished.value = promotion.is_published;
  coverImageUrl.value = promotion.cover_image_url;
  imageAlt.value = promotion.image_alt || "";
}

onMounted(() => {
  currentId.value = editingPromotionId.value;
  if (currentId.value) loadForEdit(currentId.value);
  else resetForm();
});

watch(editingPromotionId, (id) => {
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
}

async function save() {
  if (!title.value.trim()) {
    await alertDialog("Le titre de l'offre est requis.", { title: "Champ requis" });
    return;
  }
  if (!validUntil.value) {
    await alertDialog("La date limite de validité est requise.", { title: "Champ requis" });
    return;
  }
  saving.value = true;
  try {
    const payload = {
      title: title.value.trim(),
      short_description: shortDescription.value.trim(),
      value_label: valueLabel.value.trim(),
      category: category.value.trim() || null,
      valid_until: validUntil.value,
      is_published: isPublished.value,
      cover_image_url: coverImageUrl.value,
      image_alt: imageAlt.value.trim() || null,
    };
    if (isEdit.value && currentId.value) {
      await promotions.update(currentId.value, payload);
    } else {
      const created = await promotions.create(payload);
      currentId.value = created.id;
      editingPromotionId.value = created.id;
    }
    await promotions.fetchAdminAll();
    savedOk.value = true;
    setTimeout(() => (savedOk.value = false), 3000);
  } catch {
    await alertDialog("Impossible d'enregistrer l'offre. Vérifiez les champs et réessayez.", { title: "Erreur" });
  } finally {
    saving.value = false;
  }
}
</script>

<template>
  <div>
    <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 14px">
      <div class="a-sec-title" style="margin: 0">{{ isEdit ? "Modifier l'offre" : "Nouvelle offre" }}</div>
      <button class="back-link" style="margin-top: 0" @click="setTab('promotions-list')">← Retour à la liste</button>
    </div>

    <div class="editor-layout">
      <div class="editor-panel">
        <label class="al">Titre de l'offre</label>
        <input class="ai" v-model="title" type="text" placeholder="Ex : Bilan de santé complet" />

        <label class="al">Description courte</label>
        <textarea class="ai a-textarea" style="min-height: 90px" v-model="shortDescription" placeholder="Description affichée sur la carte…"></textarea>

        <label class="al">Prix ou avantage proposé</label>
        <input class="ai" v-model="valueLabel" type="text" placeholder="Ex : -20 %, Consultation offerte…" />

        <div class="ab-row" style="margin-top: 20px">
          <button class="ab ab-gold" :disabled="saving" @click="save">
            <span class="btn-content"><Spinner v-if="saving" :size="14" />{{ saving ? "Enregistrement…" : isEdit ? "Enregistrer les modifications" : "Créer l'offre" }}</span>
          </button>
        </div>
        <div v-if="savedOk" class="art-success">✓ Offre enregistrée.</div>
      </div>

      <div class="editor-sidebar">
        <label class="al">Catégorie</label>
        <input class="ai" v-model="category" type="text" placeholder="Ex : Pédiatrie, Laboratoire…" />

        <label class="al">Date limite de validité</label>
        <input class="ai" v-model="validUntil" type="date" />

        <label class="al">Statut</label>
        <select class="ai" v-model="isPublished">
          <option :value="true">Publiée</option>
          <option :value="false">Brouillon</option>
        </select>

        <div class="a-sec-title" style="margin: 14px 0 10px">Image de l'offre</div>
        <div v-if="!coverImageUrl" class="media-dropzone">
          <input
            id="promotion-image-input"
            type="file"
            accept="image/jpeg,image/jpg,image/png,image/webp"
            style="display: none"
            @change="onImageChange"
          />
          <label for="promotion-image-input" class="media-dropzone-label">
            <span style="font-size: 1.5rem">📤</span>
            <span>Glissez votre image ici ou cliquez pour parcourir</span>
            <span class="media-dropzone-hint">JPG, JPEG, PNG, WEBP — 5 Mo max</span>
          </label>
        </div>
        <div v-else class="media-image-preview">
          <img :src="mediaUrl(coverImageUrl)!" alt="" />
          <div class="media-image-actions">
            <label for="promotion-image-replace" class="a-btn-sm">Remplacer</label>
            <input
              id="promotion-image-replace"
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
      </div>
    </div>
  </div>
</template>

<style scoped>
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
</style>
