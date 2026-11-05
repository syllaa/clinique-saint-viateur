<script setup lang="ts">
import type { JobOfferListItem } from "@/services/jobService";

defineProps<{ offer: JobOfferListItem }>();
</script>

<template>
  <RouterLink :to="`/nous-rejoindre/offres/${offer.slug}`" class="job-card" v-reveal>
    <div class="job-card-top">
      <span class="job-contract">{{ offer.contract_type }}</span>
      <span v-if="offer.department" class="job-dept">{{ offer.department }}</span>
    </div>
    <h3>{{ offer.title }}</h3>
    <p v-if="offer.short_description">{{ offer.short_description }}</p>
    <div class="job-card-meta">
      <span>📍 {{ offer.location }}</span>
      <span>📅 {{ new Date(offer.created_at).toLocaleDateString("fr-FR") }}</span>
    </div>
    <span class="job-more">Voir l'offre →</span>
  </RouterLink>
</template>

<style scoped>
.job-card {
  display: block;
  background: var(--surface);
  border: 1px solid var(--border-soft);
  border-radius: 13px;
  padding: 22px;
  text-decoration: none;
  color: inherit;
  transition:
    transform 0.3s cubic-bezier(0.22, 0.68, 0, 1.2),
    box-shadow 0.3s,
    border-color 0.3s;
}
.job-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 18px 44px rgba(150, 12, 30, 0.1);
  border-color: #e8a8ae;
}
.job-card-top {
  display: flex;
  gap: 8px;
  margin-bottom: 12px;
}
.job-contract {
  background: var(--teal);
  color: #fff;
  font-size: 0.62rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  padding: 4px 10px;
  border-radius: 100px;
}
.job-dept {
  background: var(--bg-alt);
  color: var(--muted);
  font-size: 0.62rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  padding: 4px 10px;
  border-radius: 100px;
}
.job-card h3 {
  font-family: "DM Sans", sans-serif;
  font-size: 1rem;
  font-weight: 600;
  color: var(--heading);
  margin-bottom: 8px;
}
.job-card p {
  font-size: 0.82rem;
  color: var(--muted);
  line-height: 1.6;
  margin-bottom: 14px;
}
.job-card-meta {
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
  font-size: 0.74rem;
  color: var(--muted);
  margin-bottom: 14px;
}
.job-more {
  font-size: 0.78rem;
  color: var(--blue);
  font-weight: 600;
  display: inline-flex;
  align-items: center;
  gap: 5px;
  transition: gap 0.2s;
}
.job-card:hover .job-more {
  gap: 9px;
}
</style>
