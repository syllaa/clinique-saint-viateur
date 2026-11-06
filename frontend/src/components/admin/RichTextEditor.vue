<script setup lang="ts">
import Link from "@tiptap/extension-link";
import StarterKit from "@tiptap/starter-kit";
import { EditorContent, useEditor } from "@tiptap/vue-3";
import { watch } from "vue";

import { promptDialog } from "@/composables/useDialog";

const props = defineProps<{ modelValue: string }>();
const emit = defineEmits<{ (e: "update:modelValue", value: string): void }>();

const editor = useEditor({
  content: props.modelValue,
  // StarterKit (TipTap 3) already bundles Link: disable it so only the
  // configured one below is used (no click-to-open while editing).
  extensions: [StarterKit.configure({ link: false }), Link.configure({ openOnClick: false, autolink: true })],
  onUpdate: ({ editor }) => {
    emit("update:modelValue", editor.getHTML());
  },
});

watch(
  () => props.modelValue,
  (value) => {
    if (editor.value && value !== editor.value.getHTML()) {
      editor.value.commands.setContent(value, { emitUpdate: false });
    }
  },
);

async function setLink() {
  const previousUrl = editor.value?.getAttributes("link").href ?? "";
  const url = await promptDialog("Entrez l'adresse du lien à insérer.", {
    title: "Insérer un lien",
    defaultValue: previousUrl,
    placeholder: "https://exemple.com",
    confirmLabel: "Insérer",
  });
  if (url === null) return;
  if (url === "") {
    editor.value?.chain().focus().unsetLink().run();
    return;
  }
  editor.value?.chain().focus().extendMarkRange("link").setLink({ href: url }).run();
}
</script>

<template>
  <div class="rte">
    <div v-if="editor" class="rte-toolbar">
      <button
        type="button"
        class="rte-btn"
        :class="{ on: editor.isActive('bold') }"
        @click="editor.chain().focus().toggleBold().run()"
      >
        <strong>G</strong>
      </button>
      <button
        type="button"
        class="rte-btn"
        :class="{ on: editor.isActive('italic') }"
        @click="editor.chain().focus().toggleItalic().run()"
      >
        <em>I</em>
      </button>
      <span class="rte-sep"></span>
      <button
        type="button"
        class="rte-btn"
        :class="{ on: editor.isActive('heading', { level: 2 }) }"
        @click="editor.chain().focus().toggleHeading({ level: 2 }).run()"
      >
        H2
      </button>
      <button
        type="button"
        class="rte-btn"
        :class="{ on: editor.isActive('heading', { level: 3 }) }"
        @click="editor.chain().focus().toggleHeading({ level: 3 }).run()"
      >
        H3
      </button>
      <span class="rte-sep"></span>
      <button
        type="button"
        class="rte-btn"
        :class="{ on: editor.isActive('bulletList') }"
        @click="editor.chain().focus().toggleBulletList().run()"
      >
        • Liste
      </button>
      <button
        type="button"
        class="rte-btn"
        :class="{ on: editor.isActive('orderedList') }"
        @click="editor.chain().focus().toggleOrderedList().run()"
      >
        1. Liste
      </button>
      <button
        type="button"
        class="rte-btn"
        :class="{ on: editor.isActive('blockquote') }"
        @click="editor.chain().focus().toggleBlockquote().run()"
      >
        " Citation
      </button>
      <span class="rte-sep"></span>
      <button type="button" class="rte-btn" :class="{ on: editor.isActive('link') }" @click="setLink">🔗 Lien</button>
    </div>
    <EditorContent :editor="editor" class="rte-content" />
  </div>
</template>

<style scoped>
.rte {
  border: 1px solid var(--a-border);
  border-radius: 7px;
  overflow: hidden;
  margin-bottom: 14px;
  background: var(--a-tint);
}
.rte-toolbar {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 4px;
  padding: 8px;
  border-bottom: 1px solid var(--a-border);
  background: var(--a-panel);
}
.rte-btn {
  background: none;
  border: 1px solid transparent;
  color: var(--a-text-3);
  font-size: 0.74rem;
  padding: 5px 9px;
  border-radius: 5px;
  cursor: pointer;
  transition: all 0.15s;
}
.rte-btn:hover {
  background: var(--a-tint-strong);
  color: var(--a-text);
}
.rte-btn.on {
  background: rgba(224, 71, 90, 0.15);
  border-color: rgba(224, 71, 90, 0.3);
  color: var(--a-gold);
}
.rte-sep {
  width: 1px;
  height: 18px;
  background: var(--a-border);
  margin: 0 4px;
}
.rte-content {
  padding: 12px 14px;
  min-height: 220px;
  font-size: 0.88rem;
  color: var(--a-text);
}
.rte-content :deep(.ProseMirror) {
  outline: none;
  min-height: 200px;
  line-height: 1.7;
}
.rte-content :deep(h2) {
  font-size: 1.1rem;
  margin: 14px 0 8px;
  color: var(--a-text);
}
.rte-content :deep(h3) {
  font-size: 0.98rem;
  margin: 12px 0 6px;
  color: var(--a-text);
}
.rte-content :deep(p) {
  margin-bottom: 10px;
}
.rte-content :deep(ul),
.rte-content :deep(ol) {
  padding-left: 22px;
  margin-bottom: 10px;
}
.rte-content :deep(blockquote) {
  border-left: 3px solid var(--a-gold);
  padding-left: 12px;
  color: var(--a-muted);
  margin-bottom: 10px;
}
.rte-content :deep(a) {
  color: var(--a-gold);
  text-decoration: underline;
}
</style>
