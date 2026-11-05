<script setup lang="ts">
import { onMounted, ref, watch } from "vue";
import { useRoute } from "vue-router";

import Alert from "@/components/common/Alert.vue";
import Breadcrumbs from "@/components/common/Breadcrumbs.vue";
import EmptyState from "@/components/common/EmptyState.vue";
import LoadingOverlay from "@/components/common/LoadingOverlay.vue";
import Spinner from "@/components/common/Spinner.vue";
import FooterBar from "@/components/layout/FooterBar.vue";
import NavBar from "@/components/layout/NavBar.vue";
import { alertDialog } from "@/composables/useDialog";
import { applySeo, resetSeo } from "@/composables/useHead";
import { useJobApplicationsStore } from "@/stores/jobApplications";
import { useJobOffersStore } from "@/stores/jobOffers";

const route = useRoute();
const jobs = useJobOffersStore();
const applications = useJobApplicationsStore();

const loading = ref(true);
const notFound = ref(false);

const EMPLOYMENT_TYPE_MAP: Record<string, string> = {
  CDI: "FULL_TIME",
  CDD: "TEMPORARY",
  Stage: "INTERN",
  Freelance: "CONTRACTOR",
};

async function load(slug: string) {
  loading.value = true;
  notFound.value = false;
  try {
    const offer = await jobs.fetchBySlug(slug);
    applySeo({
      title: offer.seo_title || `${offer.title} – Nous rejoindre – Clinique Saint Viateur`,
      description: offer.seo_description || offer.short_description || offer.title,
      canonical: window.location.href,
      jsonLd: {
        "@context": "https://schema.org",
        "@type": "JobPosting",
        title: offer.title,
        description: offer.description || offer.short_description || offer.title,
        datePosted: offer.created_at,
        ...(offer.application_deadline ? { validThrough: offer.application_deadline } : {}),
        employmentType: EMPLOYMENT_TYPE_MAP[offer.contract_type] || "OTHER",
        hiringOrganization: {
          "@type": "Organization",
          name: "Clinique Médicale Saint Viateur",
          sameAs: window.location.origin,
        },
        jobLocation: {
          "@type": "Place",
          address: { "@type": "PostalAddress", addressLocality: offer.location, addressCountry: "CI" },
        },
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

const firstName = ref("");
const lastName = ref("");
const email = ref("");
const phone = ref("");
const coverLetter = ref("");
const cvFile = ref<File | null>(null);
const consent = ref(false);
const submitting = ref(false);
const submitted = ref(false);
const submitError = ref("");

function onCvChange(e: Event) {
  cvFile.value = (e.target as HTMLInputElement).files?.[0] || null;
}

const EMAIL_RE = /^[^@\s]+@[^@\s]+\.[^@\s]+$/;

async function submitApplication() {
  submitError.value = "";
  if (!firstName.value.trim() || !lastName.value.trim() || !phone.value.trim()) {
    await alertDialog("Veuillez renseigner votre nom, prénom et téléphone.", { title: "Champs requis" });
    return;
  }
  if (!EMAIL_RE.test(email.value.trim())) {
    await alertDialog("Veuillez saisir une adresse email valide.", { title: "Email invalide" });
    return;
  }
  if (!cvFile.value) {
    await alertDialog("Veuillez joindre votre CV au format PDF.", { title: "CV requis" });
    return;
  }
  if (!consent.value) {
    await alertDialog("Vous devez accepter le traitement de vos données pour postuler.", { title: "Consentement requis" });
    return;
  }

  const formData = new FormData();
  formData.append("first_name", firstName.value.trim());
  formData.append("last_name", lastName.value.trim());
  formData.append("email", email.value.trim());
  formData.append("phone", phone.value.trim());
  formData.append("cover_letter", coverLetter.value.trim());
  formData.append("consent", "true");
  formData.append("cv", cvFile.value);

  submitting.value = true;
  try {
    await applications.submit(jobs.current!.slug, formData);
    submitted.value = true;
  } catch (err: unknown) {
    const detail =
      (err as { response?: { data?: { detail?: string } } })?.response?.data?.detail ||
      "Une erreur est survenue. Vérifiez votre fichier (PDF, 5 Mo max) et réessayez.";
    submitError.value = detail;
  } finally {
    submitting.value = false;
  }
}
</script>

<template>
  <NavBar />

  <div v-if="loading" class="detail-loading"><Spinner :size="30" /></div>

  <template v-else-if="notFound || !jobs.current">
    <section class="section" style="padding-top: 128px">
      <div class="section-inner">
        <EmptyState icon="💼" title="Offre introuvable" message="Cette offre n'existe plus ou n'est plus ouverte aux candidatures.">
          <RouterLink to="/nous-rejoindre" class="btn-primary" style="margin-top: 16px; display: inline-flex">
            ← Retour aux offres
          </RouterLink>
        </EmptyState>
      </div>
    </section>
  </template>

  <template v-else>
    <section class="job-hero">
      <div class="section-inner">
        <Breadcrumbs
          :items="[
            { label: 'Accueil', to: '/' },
            { label: 'Nous rejoindre', to: '/nous-rejoindre' },
            { label: jobs.current.title },
          ]"
        />
        <div class="job-hero-tags">
          <span class="job-contract">{{ jobs.current.contract_type }}</span>
          <span v-if="jobs.current.department" class="job-dept">{{ jobs.current.department }}</span>
        </div>
        <h1>{{ jobs.current.title }}</h1>
        <div class="job-meta">
          <span>📍 {{ jobs.current.location }}</span>
          <span v-if="jobs.current.experience_level">🎓 {{ jobs.current.experience_level }}</span>
          <span v-if="jobs.current.application_deadline">
            ⏳ Candidatures jusqu'au {{ new Date(jobs.current.application_deadline).toLocaleDateString("fr-FR") }}
          </span>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="section-inner job-grid">
        <div class="job-body">
          <p v-if="jobs.current.short_description" class="job-lead">{{ jobs.current.short_description }}</p>

          <div v-if="jobs.current.description" class="job-block" v-html="jobs.current.description"></div>

          <div v-if="jobs.current.missions" class="job-block">
            <h2>Missions</h2>
            <p style="white-space: pre-line">{{ jobs.current.missions }}</p>
          </div>
          <div v-if="jobs.current.profile_requirements" class="job-block">
            <h2>Profil recherché</h2>
            <p style="white-space: pre-line">{{ jobs.current.profile_requirements }}</p>
          </div>
          <div v-if="jobs.current.skills" class="job-block">
            <h2>Compétences</h2>
            <p style="white-space: pre-line">{{ jobs.current.skills }}</p>
          </div>
        </div>

        <aside class="job-side">
          <div v-if="!submitted" class="job-apply-card">
            <h3>Postuler à cette offre</h3>
            <div class="job-form" :class="{ 'is-sending': submitting }">
              <div class="form-row">
                <div class="fg"><label>Prénom</label><input v-model="firstName" type="text" /></div>
                <div class="fg"><label>Nom</label><input v-model="lastName" type="text" /></div>
              </div>
              <div class="fg"><label>Email</label><input v-model="email" type="email" /></div>
              <div class="fg"><label>Téléphone</label><input v-model="phone" type="tel" placeholder="+225 …" /></div>
              <div class="fg"><label>Lettre de motivation</label><textarea v-model="coverLetter" placeholder="Quelques mots sur votre motivation…"></textarea></div>
              <div class="fg">
                <label>CV (PDF, 5 Mo max)</label>
                <input type="file" accept="application/pdf" @change="onCvChange" />
              </div>
              <label class="job-consent">
                <input type="checkbox" v-model="consent" />
                <span>J'accepte que mes données soient traitées dans le cadre de ma candidature.</span>
              </label>
              <button class="btn-submit" :disabled="submitting" @click="submitApplication">Envoyer ma candidature →</button>
              <LoadingOverlay v-if="submitting" message="Envoi de votre candidature…" />
            </div>
            <Alert v-if="submitError" variant="error">{{ submitError }}</Alert>
          </div>

          <div v-else class="job-apply-card job-success">
            <div class="job-success-icon">✓</div>
            <h3>Candidature envoyée !</h3>
            <p>Merci, votre candidature a bien été transmise. Notre équipe RH reviendra vers vous prochainement.</p>
          </div>
        </aside>
      </div>
    </section>
  </template>

  <FooterBar />
</template>

<style scoped>
.detail-loading {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
}
.job-hero {
  padding-top: 128px;
  padding-bottom: 40px;
  background: linear-gradient(155deg, var(--navy) 0%, #8f1620 100%);
}
.job-hero :deep(.crumb-link),
.job-hero :deep(.crumb-sep) {
  color: rgba(255, 255, 255, 0.5);
}
.job-hero :deep(.crumb-current) {
  color: #fff;
}
.job-hero-tags {
  display: flex;
  gap: 8px;
  margin-bottom: 14px;
}
.job-contract {
  background: var(--teal);
  color: #fff;
  font-size: 0.65rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  padding: 4px 12px;
  border-radius: 100px;
}
.job-dept {
  background: rgba(255, 255, 255, 0.12);
  color: #fff;
  font-size: 0.65rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  padding: 4px 12px;
  border-radius: 100px;
}
.job-hero h1 {
  font-family: "Cormorant Garamond", serif;
  font-size: clamp(1.7rem, 3.2vw, 2.4rem);
  color: #fff;
  margin-bottom: 14px;
}
.job-meta {
  display: flex;
  gap: 20px;
  flex-wrap: wrap;
  font-size: 0.82rem;
  color: rgba(255, 255, 255, 0.62);
}
.job-grid {
  display: grid;
  grid-template-columns: 1.6fr 1fr;
  gap: 48px;
  align-items: start;
}
.job-lead {
  font-size: 1rem;
  color: var(--heading);
  line-height: 1.7;
  margin-bottom: 24px;
}
.job-block {
  margin-bottom: 28px;
  font-size: 0.92rem;
  line-height: 1.8;
  color: var(--text);
}
.job-block h2 {
  font-size: 1.1rem;
  color: var(--heading);
  margin-bottom: 12px;
  font-family: "Cormorant Garamond", serif;
}
.job-block :deep(p) {
  margin-bottom: 12px;
}
.job-block :deep(ul),
.job-block :deep(ol) {
  padding-left: 22px;
  margin-bottom: 12px;
}
.job-side {
  position: sticky;
  top: 90px;
}
.job-apply-card {
  background: var(--surface);
  border: 1px solid var(--border-soft);
  border-radius: 15px;
  padding: 24px;
}
.job-apply-card h3 {
  font-size: 1.05rem;
  color: var(--heading);
  margin-bottom: 18px;
}
.job-form {
  position: relative;
}
.job-form.is-sending .fg,
.job-form.is-sending .btn-submit,
.job-form.is-sending .job-consent {
  pointer-events: none;
  opacity: 0.45;
}
.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
}
.fg {
  margin-bottom: 13px;
}
.fg label {
  display: block;
  font-size: 0.66rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--heading);
  margin-bottom: 5px;
}
.fg input,
.fg textarea {
  width: 100%;
  padding: 10px 13px;
  border: 1px solid var(--border-soft);
  border-radius: 7px;
  font-size: 0.85rem;
  color: var(--text);
  background: var(--bg);
  outline: none;
  transition: border-color 0.2s;
}
.fg input:focus,
.fg textarea:focus {
  border-color: var(--blue);
}
.fg textarea {
  resize: vertical;
  min-height: 76px;
}
.job-consent {
  display: flex;
  align-items: flex-start;
  gap: 8px;
  font-size: 0.78rem;
  color: var(--muted);
  line-height: 1.5;
  margin-bottom: 16px;
  cursor: pointer;
}
.job-consent input {
  margin-top: 3px;
}
.btn-submit {
  width: 100%;
  background: var(--blue);
  color: #fff;
  border: none;
  padding: 12px;
  border-radius: 8px;
  font-size: 0.88rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s, transform 0.15s;
}
.btn-submit:hover {
  background: var(--navy);
}
.btn-submit:active:not(:disabled) {
  transform: scale(0.98);
}
.job-success {
  text-align: center;
  padding: 34px 20px;
}
.job-success-icon {
  width: 54px;
  height: 54px;
  border-radius: 50%;
  background: var(--green);
  color: #fff;
  font-size: 1.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 16px;
}
.job-success p {
  font-size: 0.86rem;
  color: var(--muted);
  line-height: 1.6;
}

@media (max-width: 980px) {
  .job-grid {
    grid-template-columns: 1fr;
  }
  .job-side {
    position: static;
  }
}
@media (max-width: 640px) {
  .form-row {
    grid-template-columns: 1fr;
  }
}
</style>
