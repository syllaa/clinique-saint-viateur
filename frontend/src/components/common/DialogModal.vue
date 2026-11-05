<script setup lang="ts">
import { nextTick, onBeforeUnmount, ref, watch } from "vue";

import { resolveDialog, resolvePrompt, useDialogState } from "@/composables/useDialog";

const state = useDialogState();
const inputEl = ref<HTMLInputElement | null>(null);

function dismiss() {
  if (state.kind === "prompt") resolvePrompt(false);
  else resolveDialog(false);
}

function handleKeydown(e: KeyboardEvent) {
  if (!state.open) return;
  if (state.kind === "prompt") {
    if (e.key === "Escape") resolvePrompt(false);
    if (e.key === "Enter") resolvePrompt(true);
    return;
  }
  if (e.key === "Escape") resolveDialog(false);
  if (e.key === "Enter") resolveDialog(true);
}

watch(
  () => state.open,
  (open) => {
    if (open) {
      window.addEventListener("keydown", handleKeydown);
      if (state.kind === "prompt") nextTick(() => inputEl.value?.focus());
    } else {
      window.removeEventListener("keydown", handleKeydown);
    }
  },
);

onBeforeUnmount(() => window.removeEventListener("keydown", handleKeydown));
</script>

<template>
  <Teleport to="body">
    <Transition name="dlg">
      <div v-if="state.open" class="dlg-overlay" @click.self="dismiss">
        <div class="dlg-card" :class="{ danger: state.danger }">
          <div class="dlg-icon">
            {{ state.danger ? "⚠" : state.kind === "confirm" ? "❓" : state.kind === "prompt" ? "🔗" : "ℹ" }}
          </div>
          <h3 v-if="state.title">{{ state.title }}</h3>
          <p>{{ state.message }}</p>
          <input
            v-if="state.kind === 'prompt'"
            ref="inputEl"
            v-model="state.inputValue"
            type="text"
            class="dlg-input"
            :placeholder="state.inputPlaceholder"
          />
          <div class="dlg-actions">
            <button
              v-if="state.kind === 'confirm' || state.kind === 'prompt'"
              class="dlg-btn dlg-cancel"
              @click="dismiss"
            >
              {{ state.cancelLabel }}
            </button>
            <button
              v-if="state.kind === 'prompt'"
              class="dlg-btn dlg-primary"
              @click="resolvePrompt(true)"
            >
              {{ state.confirmLabel }}
            </button>
            <button
              v-else
              class="dlg-btn"
              :class="state.danger ? 'dlg-danger' : 'dlg-primary'"
              @click="resolveDialog(true)"
            >
              {{ state.confirmLabel }}
            </button>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<style scoped>
.dlg-overlay {
  position: fixed;
  inset: 0;
  z-index: 100000;
  background: rgba(26, 10, 13, 0.55);
  backdrop-filter: blur(2px);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}
.dlg-card {
  background: #fff;
  border-radius: 16px;
  padding: 30px 28px 24px;
  width: 380px;
  max-width: 100%;
  box-shadow: 0 24px 60px rgba(26, 10, 13, 0.35);
  text-align: center;
}
.dlg-icon {
  width: 46px;
  height: 46px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 14px;
  font-size: 1.3rem;
  background: rgba(200, 16, 46, 0.1);
  color: var(--blue, #c8102e);
}
.dlg-card.danger .dlg-icon {
  background: rgba(179, 18, 31, 0.12);
  color: var(--red-alert, #b3121f);
}
.dlg-card h3 {
  font-family: "Cormorant Garamond", serif;
  font-size: 1.2rem;
  color: var(--navy, #7a0f1a);
  margin-bottom: 8px;
}
.dlg-card p {
  font-size: 0.9rem;
  color: var(--muted, #6b5457);
  line-height: 1.6;
  margin-bottom: 22px;
  white-space: pre-line;
}
.dlg-input {
  width: 100%;
  padding: 11px 14px;
  border: 1px solid #f2d7d9;
  border-radius: 8px;
  font-size: 0.88rem;
  font-family: inherit;
  color: var(--text, #1a1414);
  background: #ffffff;
  outline: none;
  margin-bottom: 22px;
  transition:
    border-color 0.2s,
    box-shadow 0.2s;
}
.dlg-input:focus {
  border-color: var(--blue, #c8102e);
  box-shadow: 0 0 0 3px rgba(200, 16, 46, 0.1);
}
.dlg-actions {
  display: flex;
  gap: 10px;
  justify-content: center;
}
.dlg-btn {
  flex: 1;
  padding: 11px 18px;
  border-radius: 8px;
  font-size: 0.85rem;
  font-weight: 600;
  border: none;
  cursor: pointer;
  transition: all 0.2s;
  font-family: inherit;
}
.dlg-cancel {
  background: rgba(107, 84, 87, 0.1);
  color: var(--muted, #6b5457);
}
.dlg-cancel:hover {
  background: rgba(107, 84, 87, 0.18);
}
.dlg-primary {
  background: var(--blue, #c8102e);
  color: #fff;
}
.dlg-primary:hover {
  background: var(--navy, #7a0f1a);
}
.dlg-danger {
  background: var(--red-alert, #b3121f);
  color: #fff;
}
.dlg-danger:hover {
  background: #8f0e19;
}

.dlg-enter-active,
.dlg-leave-active {
  transition: opacity 0.18s ease;
}
.dlg-enter-from,
.dlg-leave-to {
  opacity: 0;
}
.dlg-enter-active .dlg-card {
  animation: dlg-pop 0.22s cubic-bezier(0.22, 0.68, 0, 1.2);
}
@keyframes dlg-pop {
  from {
    opacity: 0;
    transform: scale(0.92) translateY(8px);
  }
}

@media (prefers-reduced-motion: reduce) {
  .dlg-enter-active,
  .dlg-leave-active,
  .dlg-enter-active .dlg-card {
    animation: none !important;
    transition: none !important;
  }
}
</style>
