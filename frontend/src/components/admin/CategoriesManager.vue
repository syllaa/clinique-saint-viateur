<script setup lang="ts">
import { onMounted, ref } from "vue";

import Spinner from "@/components/common/Spinner.vue";
import { alertDialog, confirmDialog } from "@/composables/useDialog";
import { useBlogCategoriesStore } from "@/stores/blogCategories";

const categories = useBlogCategoriesStore();

const name = ref("");
const adding = ref(false);
const removingId = ref<number | null>(null);
const togglingId = ref<number | null>(null);

onMounted(() => {
  categories.fetchAdminAll();
});

async function add() {
  if (!name.value.trim()) {
    await alertDialog("Nom requis.", { title: "Champ requis" });
    return;
  }
  adding.value = true;
  try {
    await categories.create({ name: name.value.trim(), position: categories.adminItems.length });
    name.value = "";
  } finally {
    adding.value = false;
  }
}

async function toggle(id: number) {
  togglingId.value = id;
  try {
    await categories.toggleActive(id);
  } finally {
    togglingId.value = null;
  }
}

async function remove(id: number) {
  const ok = await confirmDialog("Supprimer cette catégorie ?", {
    title: "Supprimer la catégorie",
    danger: true,
    confirmLabel: "Supprimer",
  });
  if (!ok) return;
  removingId.value = id;
  try {
    await categories.remove(id);
  } finally {
    removingId.value = null;
  }
}
</script>

<template>
  <div>
    <div class="a-sec-title">Catégories du blog</div>
    <div id="cats-admin-list">
      <div v-for="c in categories.adminItems" :key="c.id" class="art-item">
        <span class="art-title-txt" style="font-weight: 600">{{ c.name }}</span>
        <span style="font-size: 0.78rem; color: var(--a-muted); flex: 1">/{{ c.slug }}</span>
        <span class="msg-badge" :class="c.is_active ? 'mb-new' : 'mb-read'">
          {{ c.is_active ? "Active" : "Masquée" }}
        </span>
        <button class="a-btn-sm" :disabled="togglingId === c.id" @click="toggle(c.id)">
          <Spinner v-if="togglingId === c.id" :size="11" />
          <span v-else>{{ c.is_active ? "Masquer" : "Activer" }}</span>
        </button>
        <button class="a-btn-sm del" :disabled="removingId === c.id" @click="remove(c.id)">
          <Spinner v-if="removingId === c.id" :size="11" />
          <span v-else>✕</span>
        </button>
      </div>
    </div>
    <div class="editor-panel" style="margin-top: 16px">
      <div class="a-sec-title" style="margin-bottom: 12px">Ajouter une catégorie</div>
      <div style="display: grid; grid-template-columns: 1fr auto; gap: 12px; align-items: end">
        <div>
          <label class="al">Nom</label>
          <input class="ai" v-model="name" type="text" placeholder="Bien-être…" style="margin-bottom: 0" />
        </div>
        <button class="ab ab-gold" :disabled="adding" @click="add">
          <span class="btn-content"><Spinner v-if="adding" :size="14" />{{ adding ? "Ajout…" : "+ Ajouter" }}</span>
        </button>
      </div>
    </div>
  </div>
</template>
