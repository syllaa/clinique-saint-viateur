<script setup lang="ts">
import { Gift } from "@lucide/vue";
import { computed, ref } from "vue";

import { mediaUrl } from "@/services/api";
import type { PromotionListItem, ReactionType } from "@/services/promotionService";
import { usePromotionsStore } from "@/stores/promotions";

const props = defineProps<{ promotion: PromotionListItem }>();

const promotions = usePromotionsStore();
const reacting = ref<ReactionType | null>(null);

const REACTIONS: { type: ReactionType; emoji: string; label: string }[] = [
  { type: "like", emoji: "👍", label: "J'aime" },
  { type: "interested", emoji: "❤️", label: "Intéressé" },
  { type: "hot", emoji: "🔥", label: "Très intéressant" },
  { type: "not_interested", emoji: "👎", label: "Pas intéressé" },
];

const canReact = computed(() => props.promotion.is_published && !props.promotion.is_expired);

const formattedDate = computed(() =>
  new Date(props.promotion.valid_until).toLocaleDateString("fr-FR", { day: "numeric", month: "long", year: "numeric" }),
);

async function react(type: ReactionType) {
  if (!canReact.value || reacting.value) return;
  reacting.value = type;
  try {
    await promotions.react(props.promotion.id, type);
  } finally {
    reacting.value = null;
  }
}
</script>

<template>
  <article class="promo-card" :class="{ 'is-expired': !canReact }" v-reveal>
    <div class="promo-thumb">
      <img
        v-if="mediaUrl(promotion.cover_image_url)"
        :src="mediaUrl(promotion.cover_image_url)!"
        :alt="promotion.image_alt || promotion.title"
        loading="lazy"
        decoding="async"
      />
      <div v-else class="promo-thumb-fallback"><Gift :size="36" aria-hidden="true" /></div>
      <span v-if="promotion.value_label" class="promo-value">{{ promotion.value_label }}</span>
      <span v-if="!canReact" class="promo-expired-badge">Offre expirée</span>
    </div>

    <div class="promo-body">
      <span v-if="promotion.category" class="promo-category">{{ promotion.category }}</span>
      <h3>{{ promotion.title }}</h3>
      <p class="promo-desc">{{ promotion.short_description }}</p>
      <div class="promo-deadline">
        <span v-if="canReact">Valable jusqu'au {{ formattedDate }}</span>
        <span v-else class="promo-deadline-expired">Cette offre a expiré le {{ formattedDate }}</span>
      </div>
    </div>

    <div class="promo-reactions">
      <button
        v-for="r in REACTIONS"
        :key="r.type"
        type="button"
        class="promo-react-btn"
        :class="{ active: promotion.my_reaction === r.type }"
        :disabled="!canReact"
        :title="canReact ? r.label : 'Cette offre a expiré'"
        :aria-pressed="promotion.my_reaction === r.type"
        @click="react(r.type)"
      >
        <span class="promo-react-emoji">{{ r.emoji }}</span>
        <span class="promo-react-count">{{ promotion.reaction_counts[r.type] }}</span>
      </button>
    </div>
  </article>
</template>

<style scoped>
.promo-card {
  display: flex;
  flex-direction: column;
  background: var(--surface);
  border: 1px solid var(--border-soft);
  border-radius: 15px;
  overflow: hidden;
  transition:
    transform 0.32s cubic-bezier(0.22, 0.68, 0, 1.2),
    box-shadow 0.32s,
    border-color 0.32s;
}
.promo-card:not(.is-expired):hover {
  transform: translateY(-6px);
  box-shadow: 0 20px 46px rgba(150, 12, 30, 0.12);
  border-color: #e8a8ae;
}
.promo-card.is-expired {
  opacity: 0.72;
}
.promo-thumb {
  position: relative;
  height: 165px;
  background: linear-gradient(135deg, var(--navy), var(--blue));
  overflow: hidden;
}
.promo-thumb img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.55s cubic-bezier(0.22, 0.68, 0, 1);
}
.promo-card:not(.is-expired):hover .promo-thumb img {
  transform: scale(1.08);
}
.promo-thumb-fallback {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 3rem;
  opacity: 0.35;
}
.promo-value {
  position: absolute;
  top: 13px;
  left: 13px;
  background: var(--gold);
  color: #fff;
  font-size: 0.78rem;
  font-weight: 700;
  padding: 5px 12px;
  border-radius: 100px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.18);
}
.promo-expired-badge {
  position: absolute;
  top: 13px;
  right: 13px;
  background: rgba(20, 20, 20, 0.72);
  color: #fff;
  font-size: 0.66rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  padding: 4px 10px;
  border-radius: 100px;
}
.promo-body {
  padding: 18px 20px 6px;
  flex: 1;
}
.promo-category {
  display: inline-block;
  font-size: 0.66rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: var(--blue);
  margin-bottom: 8px;
}
.promo-body h3 {
  font-family: var(--font-serif);
  font-size: 1.15rem;
  color: var(--heading);
  line-height: 1.3;
  margin-bottom: 8px;
}
.promo-desc {
  font-size: 0.85rem;
  color: var(--muted);
  line-height: 1.6;
  margin-bottom: 12px;
}
.promo-deadline {
  font-size: 0.76rem;
  color: var(--muted);
  padding-bottom: 14px;
}
.promo-deadline-expired {
  color: var(--danger, #c62828);
  font-weight: 600;
}
.promo-reactions {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  border-top: 1px solid var(--border-soft);
}
.promo-react-btn {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  padding: 11px 4px;
  background: transparent;
  border: none;
  border-right: 1px solid var(--border-soft);
  cursor: pointer;
  transition:
    background 0.2s,
    transform 0.15s;
}
.promo-react-btn:last-child {
  border-right: none;
}
.promo-react-btn:hover:not(:disabled) {
  background: var(--bg-alt);
}
.promo-react-btn:active:not(:disabled) {
  transform: scale(0.94);
}
.promo-react-btn.active {
  background: #fbe1e3;
}
.promo-react-btn:disabled {
  cursor: not-allowed;
  opacity: 0.4;
}
.promo-react-emoji {
  font-size: 1.05rem;
  line-height: 1;
}
.promo-react-count {
  font-size: 0.68rem;
  font-weight: 700;
  color: var(--muted);
}
.promo-react-btn.active .promo-react-count {
  color: var(--blue);
}
.promo-thumb-fallback {
  color: var(--brand-600);
}
</style>
