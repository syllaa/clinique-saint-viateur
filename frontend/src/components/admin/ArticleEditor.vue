<script setup lang="ts">
import { computed, onMounted, ref } from "vue";

import EmojiPicker from "@/components/admin/EmojiPicker.vue";
import RichTextEditor from "@/components/admin/RichTextEditor.vue";
import Spinner from "@/components/common/Spinner.vue";
import { alertDialog, confirmDialog } from "@/composables/useDialog";
import { mediaUrl } from "@/services/api";
import { uploadService } from "@/services/uploadService";
import { useArticlesStore } from "@/stores/articles";
import { useBlogCategoriesStore } from "@/stores/blogCategories";

const articles = useArticlesStore();
const categories = useBlogCategoriesStore();

const editingId = ref<number | null>(null);
const isEdit = computed(() => editingId.value !== null);

const title = ref("");
const excerpt = ref("");
const content = ref("");
const categoryId = ref<number | null>(null);
const author = ref("Clinique Saint Viateur");
const icon = ref("📋");
const coverImageUrl = ref<string | null>(null);
const practicalInfo = ref("");
const includedItems = ref("");
const benefits = ref("");
const secondaryImageUrl = ref<string | null>(null);
const secondaryImageAlt = ref("");
const seoTitle = ref("");
const seoDescription = ref("");
const status = ref<"published" | "draft">("published");

const uploadingImage = ref(false);
const uploadingSecondaryImage = ref(false);
const showOk = ref(false);
const pendingAction = ref<"publish" | "draft" | null>(null);
const removingId = ref<number | null>(null);

const newFaqQuestion = ref("");
const newFaqAnswer = ref("");
const addingFaq = ref(false);
const removingFaqId = ref<number | null>(null);

onMounted(() => {
  articles.fetchAll();
  categories.fetchAll();
});

const previewTitle = computed(() => title.value || "Titre de l'article…");

function resetForm() {
  editingId.value = null;
  title.value = "";
  excerpt.value = "";
  content.value = "";
  categoryId.value = null;
  author.value = "Clinique Saint Viateur";
  icon.value = "📋";
  coverImageUrl.value = null;
  practicalInfo.value = "";
  includedItems.value = "";
  benefits.value = "";
  secondaryImageUrl.value = null;
  secondaryImageAlt.value = "";
  seoTitle.value = "";
  seoDescription.value = "";
  status.value = "published";
}

async function editArticle(id: number) {
  const article = await articles.fetchByIdAdmin(id);
  if (!article) return;
  editingId.value = article.id;
  title.value = article.title;
  excerpt.value = article.excerpt;
  content.value = article.content;
  categoryId.value = article.category.id;
  author.value = article.author;
  icon.value = article.icon;
  coverImageUrl.value = article.cover_image_url;
  practicalInfo.value = article.practical_info || "";
  includedItems.value = article.included_items || "";
  benefits.value = article.benefits || "";
  secondaryImageUrl.value = article.secondary_image_url;
  secondaryImageAlt.value = article.secondary_image_alt || "";
  seoTitle.value = article.seo_title || "";
  seoDescription.value = article.seo_description || "";
  status.value = article.status;
  window.scrollTo({ top: 0, behavior: "smooth" });
}

async function onImageChange(e: Event) {
  const file = (e.target as HTMLInputElement).files?.[0];
  if (!file) return;
  uploadingImage.value = true;
  try {
    coverImageUrl.value = await uploadService.uploadImage(file);
  } catch {
    await alertDialog("Échec de l'envoi de l'image (format ou taille non autorisés).", {
      title: "Erreur d'upload",
    });
  } finally {
    uploadingImage.value = false;
  }
}

async function onSecondaryImageChange(e: Event) {
  const file = (e.target as HTMLInputElement).files?.[0];
  if (!file) return;
  uploadingSecondaryImage.value = true;
  try {
    secondaryImageUrl.value = await uploadService.uploadImage(file);
  } catch {
    await alertDialog("Échec de l'envoi de l'image (format ou taille non autorisés).", {
      title: "Erreur d'upload",
    });
  } finally {
    uploadingSecondaryImage.value = false;
  }
}

async function removeSecondaryImage() {
  const ok = await confirmDialog("Voulez-vous vraiment supprimer cette image ?", {
    title: "Supprimer l'image",
    danger: true,
    confirmLabel: "Supprimer",
  });
  if (!ok) return;
  secondaryImageUrl.value = null;
  secondaryImageAlt.value = "";
}

async function save(asDraft = false) {
  if (!title.value.trim()) {
    await alertDialog("Veuillez saisir un titre.", { title: "Champ requis" });
    return;
  }
  if (!categoryId.value) {
    await alertDialog("Veuillez choisir une catégorie.", { title: "Champ requis" });
    return;
  }
  pendingAction.value = asDraft ? "draft" : "publish";
  try {
    const payload = {
      title: title.value.trim(),
      excerpt: excerpt.value.trim(),
      content: content.value,
      category_id: categoryId.value,
      author: author.value.trim() || "Clinique Saint Viateur",
      icon: icon.value.trim() || "📋",
      cover_image_url: coverImageUrl.value,
      practical_info: practicalInfo.value.trim() || null,
      included_items: includedItems.value.trim() || null,
      benefits: benefits.value.trim() || null,
      secondary_image_url: secondaryImageUrl.value,
      secondary_image_alt: secondaryImageAlt.value.trim() || null,
      seo_title: seoTitle.value.trim() || null,
      seo_description: seoDescription.value.trim() || null,
      status: asDraft ? "draft" : status.value,
    };
    if (isEdit.value && editingId.value) {
      await articles.update(editingId.value, payload);
    } else {
      const created = await articles.create(payload);
      editingId.value = created.id;
    }
    await articles.fetchAll();
    showOk.value = true;
    setTimeout(() => (showOk.value = false), 3200);
  } finally {
    pendingAction.value = null;
  }
}

async function removeArticle(id: number) {
  removingId.value = id;
  try {
    await articles.remove(id);
    if (editingId.value === id) resetForm();
  } finally {
    removingId.value = null;
  }
}

async function addFaqRow() {
  if (!editingId.value || !newFaqQuestion.value.trim() || !newFaqAnswer.value.trim()) return;
  addingFaq.value = true;
  try {
    await articles.addFaq(editingId.value, {
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
    await articles.removeFaq(id);
  } finally {
    removingFaqId.value = null;
  }
}
</script>

<template>
  <div>
    <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 14px">
      <div class="a-sec-title" style="margin: 0">Articles publiés</div>
    </div>
    <div id="arts-list">
      <div v-for="a in articles.adminItems" :key="a.id" class="art-item">
        <span style="font-size: 1.3rem">{{ a.icon }}</span>
        <span class="art-cat">{{ a.category.name }}</span>
        <span class="art-title-txt">{{ a.title }}</span>
        <span class="art-date-txt">{{ new Date(a.created_at).toLocaleDateString("fr-FR") }}</span>
        <button class="a-btn-sm" @click="editArticle(a.id)">Modifier</button>
        <button class="a-btn-sm del" :disabled="removingId === a.id" @click="removeArticle(a.id)">
          <Spinner v-if="removingId === a.id" :size="11" />
          <span v-else>✕</span>
        </button>
      </div>
    </div>

    <div style="display: flex; align-items: center; justify-content: space-between; margin-top: 26px">
      <div class="a-sec-title" style="margin: 0">{{ isEdit ? "Modifier l'article" : "Rédiger un article" }}</div>
      <button v-if="isEdit" class="back-link" style="margin-top: 0" @click="resetForm">← Nouvel article</button>
    </div>
    <div class="editor-layout">
      <div class="editor-panel">
        <label class="al">Titre de l'article</label>
        <input class="ai" v-model="title" type="text" placeholder="Ex : Campagne de dépistage gratuit à la clinique…" />
        <label class="al">Résumé (extrait)</label>
        <input class="ai" v-model="excerpt" type="text" placeholder="En une phrase, de quoi parle l'article…" />
        <label class="al">Contenu complet</label>
        <RichTextEditor v-model="content" />

        <label class="al" style="margin-top: 14px">Informations pratiques (optionnel — une par ligne, avec emoji)</label>
        <textarea
          class="ai a-textarea"
          style="min-height: 90px"
          v-model="practicalInfo"
          placeholder="📅 29 septembre 2026&#10;🕐 8h – 16h&#10;📍 Route Akouédo, Riviera Sideci, Cocody&#10;👥 Tout public"
        ></textarea>

        <label class="al">L'essentiel (optionnel — une ligne par élément, avec emoji)</label>
        <textarea
          class="ai a-textarea"
          style="min-height: 90px"
          v-model="includedItems"
          placeholder="🩸 Tension artérielle&#10;📈 ECG&#10;🧪 Mesure du cholestérol"
        ></textarea>

        <label class="al">Les bénéfices (optionnel — une ligne par bénéfice, avec emoji)</label>
        <textarea
          class="ai a-textarea"
          style="min-height: 90px"
          v-model="benefits"
          placeholder="✅ Dépistage précoce&#10;🎁 Gratuité&#10;💬 Conseils personnalisés"
        ></textarea>

        <div v-if="isEdit" style="margin-top: 8px; padding-top: 18px; border-top: 1px solid var(--a-border)">
          <div class="a-sec-title">Questions fréquentes</div>
          <div v-for="f in articles.current?.faqs ?? []" :key="f.id" class="art-item" style="align-items: flex-start">
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
          <button class="ab ab-gold" :disabled="pendingAction !== null" @click="save(false)">
            <span class="btn-content"
              ><Spinner v-if="pendingAction === 'publish'" :size="14" />{{
                pendingAction === "publish" ? "Enregistrement…" : isEdit ? "✓ Enregistrer" : "✓ Publier"
              }}</span
            >
          </button>
          <button v-if="!isEdit" class="ab ab-sec" :disabled="pendingAction !== null" @click="save(true)">
            <span class="btn-content"><Spinner v-if="pendingAction === 'draft'" :size="14" />{{ pendingAction === "draft" ? "Enregistrement…" : "Brouillon" }}</span>
          </button>
        </div>
        <div v-if="showOk" class="art-success">✓ Article enregistré.</div>
        <p v-if="!isEdit" style="font-size: 0.74rem; color: var(--a-muted); margin-top: 10px">
          Enregistrez d'abord l'article pour pouvoir y ajouter des questions fréquentes.
        </p>
      </div>
      <div class="editor-sidebar">
        <label class="al">Catégorie</label>
        <select class="ai" v-model="categoryId">
          <option :value="null" disabled>Sélectionnez une catégorie</option>
          <option v-for="c in categories.items" :key="c.id" :value="c.id">{{ c.name }}</option>
        </select>
        <label class="al">Auteur</label>
        <input class="ai" v-model="author" type="text" />
        <label class="al">Icône</label>
        <EmojiPicker v-model="icon" />

        <label class="al">Image de couverture</label>
        <input type="file" accept="image/png,image/jpeg,image/webp" @change="onImageChange" style="margin-bottom: 10px" />
        <div v-if="uploadingImage" style="margin-bottom: 10px"><Spinner :size="16" /></div>
        <img
          v-if="coverImageUrl"
          :src="mediaUrl(coverImageUrl)!"
          alt=""
          style="width: 100%; border-radius: 8px; margin-bottom: 14px; display: block"
        />

        <div style="padding-top: 13px; border-top: 1px solid var(--a-border); margin-top: 4px">
          <div class="a-sec-title" style="margin-bottom: 10px">Image secondaire (optionnelle)</div>
          <div v-if="!secondaryImageUrl" class="media-dropzone">
            <input
              id="article-secondary-image-input"
              type="file"
              accept="image/jpeg,image/jpg,image/png,image/webp"
              style="display: none"
              @change="onSecondaryImageChange"
            />
            <label for="article-secondary-image-input" class="media-dropzone-label">
              <span style="font-size: 1.4rem">📤</span>
              <span>Cliquez pour parcourir</span>
              <span class="media-dropzone-hint">JPG, PNG, WEBP — 5 Mo max</span>
            </label>
          </div>
          <div v-else class="media-image-preview">
            <img :src="mediaUrl(secondaryImageUrl)!" alt="" />
            <div class="media-image-actions">
              <label for="article-secondary-image-replace" class="a-btn-sm">Remplacer</label>
              <input
                id="article-secondary-image-replace"
                type="file"
                accept="image/jpeg,image/jpg,image/png,image/webp"
                style="display: none"
                @change="onSecondaryImageChange"
              />
              <button class="a-btn-sm del" type="button" @click="removeSecondaryImage">Supprimer</button>
            </div>
          </div>
          <div v-if="uploadingSecondaryImage" class="media-uploading"><Spinner :size="14" /> Envoi en cours…</div>
          <label class="al" style="margin-top: 8px">Texte alternatif</label>
          <input class="ai" v-model="secondaryImageAlt" type="text" placeholder="Décrivez l'image (accessibilité)…" />
        </div>

        <label class="al" style="margin-top: 14px">Statut</label>
        <select class="ai" v-model="status">
          <option value="published">Publié</option>
          <option value="draft">Brouillon</option>
        </select>

        <div style="padding-top: 13px; border-top: 1px solid var(--a-border); margin-top: 4px">
          <div class="a-sec-title" style="margin-bottom: 10px">SEO</div>
          <label class="al">Titre SEO</label>
          <input class="ai" v-model="seoTitle" type="text" />
          <label class="al">Meta description</label>
          <textarea class="ai a-textarea" style="min-height: 70px" v-model="seoDescription"></textarea>
        </div>

        <div style="padding-top: 13px; border-top: 1px solid var(--a-border); margin-top: 4px">
          <div class="a-sec-title" style="margin-bottom: 10px">Aperçu de la carte</div>
          <div style="background: var(--a-tint); border: 1px solid var(--a-border); border-radius: 9px; padding: 13px">
            <div style="font-size: 2rem; margin-bottom: 8px">{{ icon || "📋" }}</div>
            <div style="font-size: 0.62rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; color: var(--a-gold); margin-bottom: 5px">
              {{ categories.items.find((c) => c.id === categoryId)?.name || "Catégorie" }}
            </div>
            <div style="font-size: 0.86rem; color: var(--a-text); font-weight: 500; line-height: 1.4">
              {{ previewTitle }}
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.media-dropzone {
  border: 1.5px dashed var(--a-border);
  border-radius: 10px;
  padding: 22px 14px;
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
