<script setup lang="ts">
import {
  Activity,
  CalendarCheck,
  ClipboardList,
  Clock,
  HeartPulse,
  Phone,
  Quote,
  ShieldCheck,
  Sparkles,
  Stethoscope,
  Syringe,
  UserRound,
  Users,
} from "@lucide/vue";
import { computed, onMounted, ref, watch } from "vue";
import { useRoute } from "vue-router";

import Breadcrumbs from "@/components/common/Breadcrumbs.vue";
import EmptyState from "@/components/common/EmptyState.vue";
import Spinner from "@/components/common/Spinner.vue";
import SpecialtyMedia from "@/components/specialties/SpecialtyMedia.vue";
import { TESTIMONIALS } from "@/constants/testimonials";
import { applySeo, resetSeo } from "@/composables/useHead";
import { mediaUrl } from "@/services/api";
import { useScrollScene } from "@/motion/useScrollScene";
import { useSpecialtiesStore } from "@/stores/specialties";

const route = useRoute();

// Cover photo drifts slower than the page while the hero scrolls away.
const heroRef = ref<HTMLElement | null>(null);
useScrollScene(heroRef, ({ gsap }, hero) => {
  const img = hero.querySelector(".spd-hero-bg img");
  if (!img) return;
  gsap.fromTo(img, { yPercent: -5, scale: 1.1 }, {
    yPercent: 10,
    scale: 1,
    ease: "none",
    scrollTrigger: { trigger: hero, start: "top top", end: "bottom top", scrub: true },
  });
});
const specialties = useSpecialtiesStore();
const loading = ref(true);
const notFound = ref(false);

const servicesList = computed(() =>
  (specialties.current?.services_offered || "")
    .split("\n")
    .map((line) => line.trim())
    .filter(Boolean),
);

const INTERVENTION_ICONS = [Stethoscope, Activity, HeartPulse, ShieldCheck, Syringe, ClipboardList];

// "Titre — description" lines render as a card grid; a plain line without the
// separator still works, it just renders with a title and no description.
const interventionItems = computed(() =>
  servicesList.value.map((line, i) => {
    const sep = line.match(/\s[—–-]\s/);
    const title = sep ? line.slice(0, sep.index).trim() : line;
    const desc = sep ? line.slice((sep.index ?? 0) + sep[0].length).trim() : "";
    return { title, desc, icon: INTERVENTION_ICONS[i % INTERVENTION_ICONS.length] };
  }),
);

const heroImageUrl = computed(() => {
  const s = specialties.current;
  if (!s || s.media_type !== "image") return null;
  return mediaUrl(s.cover_image_url);
});

// Only surfaced when the specialty's own admin-entered hours actually say so —
// never assumed, so it can't misrepresent a non-24/7 specialty.
const isAvailable24_7 = computed(() => {
  const s = specialties.current;
  if (!s) return false;
  return /24\s*h\s*\/\s*24/i.test(`${s.consultation_hours ?? ""} ${s.full_description ?? ""}`);
});

const trustPoints = [
  { icon: Sparkles, title: "Équipements modernes", desc: "Un plateau technique régulièrement mis à niveau pour des soins précis et sûrs." },
  { icon: Users, title: "Équipe qualifiée", desc: "Des praticiens expérimentés, formés et disponibles pour répondre à vos besoins." },
  { icon: ShieldCheck, title: "Hygiène certifiée", desc: "Des protocoles de stérilisation stricts, conformes aux normes en vigueur." },
];

const careSteps = [
  { icon: CalendarCheck, title: "Consultation", desc: "Un premier échange avec le praticien pour évaluer votre situation." },
  { icon: ClipboardList, title: "Bilan & examens", desc: "Les examens complémentaires nécessaires sont réalisés sur place." },
  { icon: Stethoscope, title: "Prise en charge", desc: "Le traitement ou l'intervention est planifié et réalisé par notre équipe." },
  { icon: HeartPulse, title: "Suivi", desc: "Un accompagnement après votre passage pour assurer votre rétablissement." },
];

const introStats = [
  { n: "79K+", l: "Patients satisfaits" },
  { n: "24/7", l: "Urgences en permanence" },
  { n: "10+", l: "Spécialités médicales" },
  { n: "3ᵉ", l: "Prix national d'excellence" },
];

const testimonial = computed(() => {
  const id = specialties.current?.id ?? 0;
  return TESTIMONIALS[id % TESTIMONIALS.length];
});

async function load(slug: string) {
  loading.value = true;
  notFound.value = false;
  try {
    const specialty = await specialties.fetchBySlug(slug);
    applySeo({
      title: specialty.seo_title || `${specialty.name} – Clinique Saint Viateur`,
      description: specialty.seo_description || specialty.description,
      ogImage: mediaUrl(specialty.cover_image_url) || undefined,
      canonical: window.location.href,
      jsonLd: {
        "@context": "https://schema.org",
        "@type": "MedicalSpecialty",
        name: specialty.name,
        description: specialty.description,
        url: window.location.href,
      },
    });
  } catch {
    notFound.value = true;
    resetSeo();
  } finally {
    loading.value = false;
  }
}

onMounted(() => load(route.params.slug as string));
watch(
  () => route.params.slug,
  (slug) => slug && load(slug as string),
);
</script>

<template>

  <div v-if="loading" class="detail-loading" role="status" aria-live="polite"><Spinner :size="30" /><span class="sr-only">Chargement…</span></div>

  <template v-else-if="notFound || !specialties.current">
    <section class="section" style="padding-top: 128px">
      <div class="section-inner">
        <EmptyState :icon="Stethoscope" title="Spécialité introuvable" message="Cette spécialité n'existe pas ou n'est plus disponible.">
          <RouterLink to="/specialites" class="btn-primary" style="margin-top: 16px; display: inline-flex">
            ← Retour aux spécialités
          </RouterLink>
        </EmptyState>
      </div>
    </section>
  </template>

  <template v-else>
    <section ref="heroRef" class="spd-hero" :class="{ 'has-image': heroImageUrl }">
      <div v-if="heroImageUrl" class="spd-hero-bg">
        <img :src="heroImageUrl" :alt="specialties.current.image_alt || specialties.current.name" />
        <div class="spd-hero-overlay"></div>
      </div>

      <div class="section-inner spd-hero-inner">
        <Breadcrumbs
          :items="[
            { label: 'Accueil', to: '/' },
            { label: 'Spécialités', to: '/specialites' },
            { label: specialties.current.name },
          ]"
        />
        <SpecialtyMedia
          v-if="!heroImageUrl"
          class="spd-media"
          size="hero"
          :media-type="specialties.current.media_type"
          :icon-name="specialties.current.icon_name"
          :image-url="specialties.current.cover_image_url"
          :image-alt="specialties.current.image_alt"
          :name="specialties.current.name"
        />
        <span v-if="isAvailable24_7" v-reveal class="spd-badge"><Clock :size="14" aria-hidden="true" /> Disponible 24h/24</span>
        <h1 v-reveal class="d1">{{ specialties.current.name }}</h1>
        <p v-reveal class="d2">{{ specialties.current.description }}</p>
        <div v-reveal class="spd-hero-btns d3">
          <a href="tel:+2252722590417" class="btn-primary"><Phone :size="16" aria-hidden="true" /> Prendre rendez-vous</a>
          <RouterLink to="/#contact" class="btn-outline-light">Nous contacter</RouterLink>
        </div>
      </div>
    </section>

    <!-- INTRO -->
    <section v-if="specialties.current.full_description" class="section">
      <div class="section-inner spd-intro">
        <div v-reveal class="spd-intro-text">
          <p class="section-kicker">Présentation</p>
          <p style="white-space: pre-line">{{ specialties.current.full_description }}</p>
        </div>
        <div class="spd-intro-stats">
          <div v-for="(st, i) in introStats" :key="i" v-reveal="{ type: 'scale', delay: i * 90 }" class="spd-stat">
            <div class="spd-stat-n">{{ st.n }}</div>
            <div class="spd-stat-l">{{ st.l }}</div>
          </div>
        </div>
      </div>
    </section>

    <!-- INTERVENTIONS -->
    <section v-if="interventionItems.length" class="section" style="background: var(--bg-alt)">
      <div class="section-inner">
        <p v-reveal class="section-kicker">Nos services</p>
        <h2 v-reveal="'words'" class="section-title d1">Ce que nous proposons</h2>
        <div class="spd-svc-grid">
          <div v-for="(item, i) in interventionItems" :key="i" v-reveal="{ type: 'up', delay: (i % 3) * 90 }" class="spd-svc-card">
            <div class="spd-svc-icon"><component :is="item.icon" :size="22" :stroke-width="1.75" /></div>
            <h3>{{ item.title }}</h3>
            <p v-if="item.desc">{{ item.desc }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- TRUST -->
    <section class="section spd-trust">
      <div class="section-inner">
        <p v-reveal class="section-kicker" style="color: var(--sky-light)">Notre engagement</p>
        <h2 v-reveal="'words'" class="section-title d1" style="color: #fff">Un environnement médical de confiance</h2>
        <div class="spd-trust-grid">
          <div v-for="(pt, i) in trustPoints" :key="i" v-reveal="{ type: 'up', delay: (i % 3) * 110 }" class="spd-trust-card">
            <div class="spd-trust-icon"><component :is="pt.icon" :size="24" :stroke-width="1.75" /></div>
            <h3>{{ pt.title }}</h3>
            <p>{{ pt.desc }}</p>
          </div>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="section-inner spd-grid">
        <div class="spd-main">
          <div v-if="specialties.current.symptoms_text" class="spd-block">
            <h2>Symptômes & motifs de consultation</h2>
            <p style="white-space: pre-line">{{ specialties.current.symptoms_text }}</p>
          </div>

          <div v-if="specialties.current.doctors.length" class="spd-block">
            <h2>Médecins associés</h2>
            <div class="spd-doctors">
              <div v-for="d in specialties.current.doctors" :key="d.id" class="spd-doctor">
                <img v-if="mediaUrl(d.photo_url)" :src="mediaUrl(d.photo_url)!" :alt="d.name" class="spd-doctor-photo" />
                <div v-else class="spd-doctor-photo spd-doctor-placeholder"><UserRound :size="34" aria-hidden="true" /></div>
                <div>
                  <div class="spd-doctor-name">{{ d.name }}</div>
                  <div v-if="d.title" class="spd-doctor-title">{{ d.title }}</div>
                </div>
              </div>
            </div>
          </div>

          <div v-if="specialties.current.faqs.length" class="spd-block">
            <h2>Questions fréquentes</h2>
            <details v-for="f in specialties.current.faqs" :key="f.id" class="spd-faq faq-smooth">
              <summary>{{ f.question }}</summary>
              <p>{{ f.answer }}</p>
            </details>
          </div>
        </div>

        <aside class="spd-side">
          <div v-if="specialties.current.consultation_hours" class="spd-card">
            <h3>Horaires de consultation</h3>
            <p>{{ specialties.current.consultation_hours }}</p>
          </div>
          <div v-if="specialties.current.practical_info" class="spd-card">
            <h3>Informations pratiques</h3>
            <p style="white-space: pre-line">{{ specialties.current.practical_info }}</p>
          </div>
          <div class="spd-card spd-card-cta">
            <h3>Besoin d'un rendez-vous ?</h3>
            <a href="tel:+2252722590417" class="spd-phone-link"><Phone :size="15" :stroke-width="2" /> 27 22 59 04 17</a>
            <a href="tel:+2250101466576" class="spd-phone-link"><Phone :size="15" :stroke-width="2" /> 01 01 46 65 76</a>
            <a href="tel:+2250707095549" class="spd-phone-link"><Phone :size="15" :stroke-width="2" /> 07 07 09 55 49</a>
            <a href="tel:+2252722590417" class="btn-primary spd-cta-btn"><Phone :size="16" aria-hidden="true" /> Prendre rendez-vous</a>
            <RouterLink to="/#contact" class="btn-outline-light spd-cta-btn">Nous contacter</RouterLink>
          </div>
        </aside>
      </div>
    </section>

    <!-- CARE TIMELINE -->
    <section class="section" style="background: var(--bg-alt)">
      <div class="section-inner">
        <p v-reveal class="section-kicker">Votre parcours</p>
        <h2 v-reveal="'words'" class="section-title d1">Avant votre prise en charge</h2>
        <div class="spd-timeline">
          <div v-for="(step, i) in careSteps" :key="i" v-reveal="{ type: 'up', delay: i * 120 }" class="spd-step">
            <div class="spd-step-icon"><component :is="step.icon" :size="20" :stroke-width="1.75" /></div>
            <div class="spd-step-n">{{ i + 1 }}</div>
            <h3>{{ step.title }}</h3>
            <p>{{ step.desc }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- TESTIMONIAL -->
    <section class="section">
      <div class="section-inner">
        <div v-reveal class="spd-testi">
          <Quote :size="28" :stroke-width="1.5" class="spd-testi-quote" />
          <div class="spd-testi-stars">{{ testimonial.stars }}</div>
          <p class="spd-testi-text">{{ testimonial.text }}</p>
          <div class="spd-testi-author">{{ testimonial.author }}</div>
          <div class="spd-testi-meta">{{ testimonial.meta }}</div>
        </div>
      </div>
    </section>

    <!-- BOTTOM CTA -->
    <section class="spd-cta-banner">
      <div class="section-inner spd-cta-banner-inner">
        <div>
          <h2>Besoin de prendre rendez-vous ?</h2>
          <p>Notre équipe vous répond rapidement pour organiser votre consultation.</p>
        </div>
        <a href="tel:+2252722590417" class="btn-primary"><Phone :size="16" aria-hidden="true" /> Appeler la clinique</a>
      </div>
    </section>
  </template>

</template>

<style scoped>
/* Dark placeholder shaped like the hero: no white flash before it appears. */
.detail-loading {
  min-height: 480px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(155deg, var(--brand-900) 0%, var(--brand-700) 100%);
  color: var(--brand-200);
}
.spd-hero {
  position: relative;
  padding-top: 128px;
  padding-bottom: 56px;
  background: linear-gradient(155deg, var(--navy) 0%, #8f1620 100%);
  overflow: hidden;
  display: flex;
  align-items: flex-end;
  min-height: 480px;
}
.spd-hero.has-image {
  min-height: 580px;
}
.spd-hero-bg {
  position: absolute;
  inset: 0;
  z-index: 0;
}
.spd-hero-bg img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center;
  display: block;
}
.spd-hero-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(180deg, rgba(56, 10, 14, 0.32) 0%, rgba(58, 10, 15, 0.55) 45%, rgba(30, 5, 9, 0.94) 100%);
}
.spd-hero-inner {
  position: relative;
  z-index: 1;
  width: 100%;
}
.spd-hero :deep(.crumb-link),
.spd-hero :deep(.crumb-sep) {
  color: rgba(255, 255, 255, 0.5);
}
.spd-hero :deep(.crumb-current) {
  color: #fff;
}
.spd-media {
  margin-bottom: 18px;
}
.spd-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: rgba(243, 170, 180, 0.14);
  border: 1px solid rgba(243, 170, 180, 0.45);
  color: var(--brand-200);
  font-size: 0.72rem;
  font-weight: 700;
  letter-spacing: 0.04em;
  padding: 6px 14px;
  border-radius: 100px;
  margin-bottom: 16px;
}
.spd-hero-inner h1 {
  font-family: "Cormorant Garamond", serif;
  font-size: clamp(2.1rem, 4vw, 3.1rem);
  color: #fff;
  margin-bottom: 12px;
}
.spd-hero-inner p {
  color: rgba(255, 255, 255, 0.68);
  max-width: 560px;
  font-size: 0.98rem;
  line-height: 1.7;
  margin-bottom: 26px;
}
.spd-hero-btns {
  display: flex;
  gap: 14px;
  flex-wrap: wrap;
}

.spd-grid {
  display: grid;
  grid-template-columns: 1.7fr 1fr;
  gap: 48px;
  align-items: start;
}
.spd-block {
  margin-bottom: 36px;
}
.spd-block h2 {
  font-size: 1.15rem;
  color: var(--heading);
  margin-bottom: 14px;
  font-family: "Cormorant Garamond", serif;
}
.spd-block p {
  color: var(--muted);
  font-size: 0.92rem;
  line-height: 1.8;
}
/* ─── INTRO (text + stat cards) ─── */
.spd-intro {
  display: grid;
  grid-template-columns: 1.5fr 1fr;
  gap: 48px;
  align-items: center;
}
.spd-intro-text p {
  color: var(--muted);
  font-size: 0.98rem;
  line-height: 1.85;
}
.spd-intro-stats {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 13px;
}
.spd-stat {
  background: var(--surface);
  border: 1px solid var(--border-soft);
  border-radius: 13px;
  padding: 22px 16px;
  text-align: center;
  transition: border-color 0.25s, transform 0.25s;
}
.spd-stat:hover {
  border-color: var(--brand-400);
  transform: translateY(-3px);
}
.spd-stat-n {
  font-family: "Cormorant Garamond", serif;
  font-size: 1.9rem;
  color: var(--heading);
  line-height: 1;
}
.spd-stat-l {
  font-size: 0.7rem;
  color: var(--muted);
  margin-top: 7px;
  line-height: 1.4;
}

/* ─── SERVICES / INTERVENTIONS GRID ─── */
.spd-svc-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: 18px;
}
.spd-svc-card {
  background: var(--surface);
  border: 1px solid var(--border-soft);
  border-radius: 14px;
  padding: 24px 22px;
  transition: transform 0.3s cubic-bezier(0.22, 0.68, 0, 1.2), box-shadow 0.3s, border-color 0.3s;
}
.spd-svc-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 18px 40px rgba(122, 15, 26, 0.12);
  border-color: var(--brand-400);
}
.spd-svc-icon {
  width: 46px;
  height: 46px;
  border-radius: 11px;
  background: var(--bg-alt);
  color: var(--blue);
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 14px;
}
.spd-svc-card h3 {
  font-size: 0.98rem;
  color: var(--heading);
  margin-bottom: 6px;
  font-weight: 600;
}
.spd-svc-card p {
  font-size: 0.84rem;
  color: var(--muted);
  line-height: 1.65;
}

/* ─── TRUST ─── */
.spd-trust {
  background: var(--navy);
}
.spd-trust-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 22px;
}
.spd-trust-card {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.09);
  border-radius: 14px;
  padding: 26px 22px;
  transition: border-color 0.25s, transform 0.25s;
}
.spd-trust-card:hover {
  border-color: var(--brand-400);
  transform: translateY(-4px);
}
.spd-trust-icon {
  width: 46px;
  height: 46px;
  border-radius: 11px;
  background: rgba(243, 170, 180, 0.14);
  color: var(--brand-200);
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 16px;
}
.spd-trust-card h3 {
  font-family: "Cormorant Garamond", serif;
  font-size: 1.15rem;
  color: #fff;
  margin-bottom: 8px;
}
.spd-trust-card p {
  font-size: 0.86rem;
  color: rgba(255, 255, 255, 0.6);
  line-height: 1.65;
}

.spd-doctors {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 14px;
}
.spd-doctor {
  display: flex;
  align-items: center;
  gap: 12px;
  background: var(--surface);
  border: 1px solid var(--border-soft);
  border-radius: 12px;
  padding: 14px;
}
.spd-doctor-photo {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  object-fit: cover;
  flex-shrink: 0;
}
.spd-doctor-placeholder {
  background: var(--bg-alt);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.3rem;
}
.spd-doctor-name {
  font-size: 0.86rem;
  font-weight: 600;
  color: var(--heading);
}
.spd-doctor-title {
  font-size: 0.76rem;
  color: var(--muted);
  margin-top: 2px;
}
.spd-faq {
  border: 1px solid var(--border-soft);
  border-radius: 10px;
  padding: 14px 16px;
  margin-bottom: 10px;
  background: var(--surface);
}
.spd-faq summary {
  cursor: pointer;
  font-weight: 600;
  font-size: 0.88rem;
  color: var(--heading);
}
.spd-faq p {
  margin-top: 10px;
  font-size: 0.86rem;
  color: var(--muted);
  line-height: 1.65;
}
.spd-side {
  display: flex;
  flex-direction: column;
  gap: 16px;
  position: sticky;
  top: 90px;
}
.spd-card {
  background: var(--surface);
  border: 1px solid var(--border-soft);
  border-radius: 13px;
  padding: 20px;
}
.spd-card h3 {
  font-size: 0.95rem;
  color: var(--heading);
  margin-bottom: 10px;
}
.spd-card p {
  font-size: 0.86rem;
  color: var(--muted);
  line-height: 1.65;
}
.spd-card-cta {
  display: flex;
  flex-direction: column;
  gap: 10px;
  background: var(--bg-alt);
}
.spd-phone-link {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.86rem;
  font-weight: 600;
  color: var(--heading);
  text-decoration: none;
  transition: color 0.2s;
}
.spd-phone-link:hover {
  color: var(--blue);
}
.spd-cta-btn {
  justify-content: center;
  text-align: center;
  margin-top: 4px;
}
.spd-cta-btn.btn-outline-light {
  color: var(--heading);
  border-color: var(--border-soft);
}
.spd-cta-btn.btn-outline-light:hover {
  background: var(--surface);
}

/* ─── CARE TIMELINE ─── */
.spd-timeline {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 22px;
}
.spd-step {
  position: relative;
  background: var(--surface);
  border: 1px solid var(--border-soft);
  border-radius: 14px;
  padding: 26px 20px 22px;
  transition: border-color 0.25s, transform 0.25s;
}
.spd-step:hover {
  border-color: var(--brand-400);
  transform: translateY(-4px);
}
.spd-step-icon {
  width: 42px;
  height: 42px;
  border-radius: 10px;
  background: var(--bg-alt);
  color: var(--blue);
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 14px;
}
.spd-step-n {
  position: absolute;
  top: 18px;
  right: 20px;
  font-family: "Cormorant Garamond", serif;
  font-size: 1.5rem;
  color: var(--border-soft);
  line-height: 1;
}
.spd-step h3 {
  font-size: 0.95rem;
  color: var(--heading);
  margin-bottom: 6px;
  font-weight: 600;
}
.spd-step p {
  font-size: 0.82rem;
  color: var(--muted);
  line-height: 1.6;
}

/* ─── TESTIMONIAL ─── */
.spd-testi {
  max-width: 680px;
  margin: 0 auto;
  text-align: center;
  background: var(--surface);
  border: 1px solid var(--border-soft);
  border-radius: 18px;
  padding: 44px 40px;
}
.spd-testi-quote {
  color: var(--brand-400);
  margin-bottom: 10px;
}
.spd-testi-stars {
  color: var(--gold);
  font-size: 0.9rem;
  margin-bottom: 14px;
}
.spd-testi-text {
  font-family: "Cormorant Garamond", serif;
  font-size: 1.3rem;
  color: var(--heading);
  line-height: 1.55;
  margin-bottom: 20px;
}
.spd-testi-author {
  font-size: 0.9rem;
  font-weight: 700;
  color: var(--heading);
}
.spd-testi-meta {
  font-size: 0.78rem;
  color: var(--muted);
  margin-top: 3px;
}

/* ─── BOTTOM CTA BANNER ─── */
.spd-cta-banner {
  background: linear-gradient(120deg, var(--navy) 0%, #8f1620 100%);
  padding: 56px 5vw;
}
.spd-cta-banner-inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 24px;
  flex-wrap: wrap;
}
.spd-cta-banner-inner h2 {
  font-family: "Cormorant Garamond", serif;
  font-size: 1.7rem;
  color: #fff;
  margin-bottom: 6px;
}
.spd-cta-banner-inner p {
  color: rgba(255, 255, 255, 0.62);
  font-size: 0.92rem;
}

@media (max-width: 980px) {
  .spd-grid {
    grid-template-columns: 1fr;
  }
  .spd-side {
    position: static;
  }
  .spd-intro {
    grid-template-columns: 1fr;
  }
  .spd-trust-grid {
    grid-template-columns: 1fr 1fr;
  }
  .spd-timeline {
    grid-template-columns: 1fr 1fr;
  }
}
@media (max-width: 640px) {
  .spd-intro-stats {
    grid-template-columns: 1fr 1fr;
  }
  .spd-trust-grid,
  .spd-timeline {
    grid-template-columns: 1fr;
  }
  .spd-cta-banner-inner {
    flex-direction: column;
    align-items: flex-start;
  }
  .spd-testi {
    padding: 32px 22px;
  }
}
.spd-doctor-placeholder {
  color: var(--brand-400);
}
</style>
