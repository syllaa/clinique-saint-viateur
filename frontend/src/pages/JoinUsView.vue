<script setup lang="ts">
import { Briefcase, Clock, Mail, MapPin, Phone } from "@lucide/vue";
import { onMounted, ref } from "vue";

import AmbientVideo from "@/components/common/AmbientVideo.vue";
import HoneypotField from "@/components/common/HoneypotField.vue";
import PageHeader from "@/components/common/PageHeader.vue";
import SkeletonGrid from "@/components/common/SkeletonGrid.vue";
import EmptyState from "@/components/common/EmptyState.vue";
import LoadError from "@/components/common/LoadError.vue";
import LoadingOverlay from "@/components/common/LoadingOverlay.vue";
import JobOfferCard from "@/components/jobs/JobOfferCard.vue";
import teamPhoto from "@/assets/images/team/team-staff-group-large.webp";
import { alertDialog } from "@/composables/useDialog";
import { applySeo } from "@/composables/useHead";
import { siteService } from "@/services/siteService";
import { useJobOffersStore } from "@/stores/jobOffers";
import { apiErrorMessage } from "@/utils/apiError";

const jobs = useJobOffersStore();
const jobsLoading = ref(true);
const jobsError = ref(false);

const mapsKey = import.meta.env.VITE_GOOGLE_MAPS_API_KEY as string | undefined;
const mapsQuery = "Clinique Medicale Saint Viateur, Route Akouédo, Riviera Sideci, Cocody, Abidjan";

onMounted(async () => {
  applySeo({
    title: "Nous rejoindre – Contact & Carrières – Clinique Saint Viateur",
    description:
      "Contactez la Clinique Saint Viateur ou découvrez nos offres d'emploi à Cocody, Abidjan.",
    canonical: window.location.href,
  });
  await loadJobs();
});

async function loadJobs() {
  jobsLoading.value = true;
  jobsError.value = false;
  try {
    await jobs.fetchAll();
  } catch {
    jobsError.value = true;
  } finally {
    jobsLoading.value = false;
  }
}

const name = ref("");
const email = ref("");
const phone = ref("");
const subject = ref("");
const message = ref("");
const sending = ref(false);
const sent = ref(false);

const honeypot = ref("");

async function submitContact() {
  if (!name.value.trim() || !message.value.trim()) {
    await alertDialog("Veuillez remplir au moins votre nom et votre message.", { title: "Formulaire incomplet" });
    return;
  }
  sending.value = true;
  try {
    await siteService.sendMessage({
      name: name.value.trim(),
      email: email.value.trim() || undefined,
      phone: phone.value.trim() || undefined,
      subject: subject.value.trim() || "Nous rejoindre",
      content: message.value.trim(),
      urgency: "programme",
      wants_hospitalization_info: false,
      website: honeypot.value,
    });
    sent.value = true;
    name.value = "";
    email.value = "";
    phone.value = "";
    subject.value = "";
    message.value = "";
  } catch (err) {
    await alertDialog(
      apiErrorMessage(err, "Votre message n'a pas pu être envoyé. Réessayez, ou appelez-nous au 27 22 59 04 17."),
      { title: "Envoi impossible" },
    );
  } finally {
    sending.value = false;
  }
}
</script>

<template>

  <PageHeader
    kicker="Nous rejoindre"
    title="Contactez-nous & rejoignez notre équipe"
    lead="Une question, un besoin d'orientation ou l'envie de rejoindre nos équipes soignantes ? Nous sommes à votre écoute."
    :crumbs="[{ label: 'Accueil', to: '/' }, { label: 'Nous rejoindre' }]"
  />

  <section class="section join-hero">
    <div class="section-inner">

      <div class="join-grid">
        <div>
          <h2 class="sr-only">Nos coordonnées</h2>
          <div class="join-cards">
            <div v-reveal class="ccard">
              <div class="ccard-icon"><MapPin :size="20" aria-hidden="true" /></div>
              <div><h3>Adresse</h3><p>Route Akouédo, Riviera Sideci – Cocody<br />22 BP 289, Abidjan 22, Côte d'Ivoire</p></div>
            </div>
            <div v-reveal class="ccard">
              <div class="ccard-icon"><Phone :size="20" aria-hidden="true" /></div>
              <div>
                <h3>Téléphone</h3>
                <a href="tel:+2252722590417">+225 27 22 59 04 17</a>
              </div>
            </div>
            <div v-reveal class="ccard">
              <div class="ccard-icon"><Mail :size="20" aria-hidden="true" /></div>
              <div><h3>Email</h3><a href="mailto:cliniquestviateur@aviso.ci">cliniquestviateur@aviso.ci</a></div>
            </div>
            <div v-reveal class="ccard">
              <div class="ccard-icon"><Clock :size="20" aria-hidden="true" /></div>
              <div><h3>Horaires</h3><p>Lun–Ven 08h–20h · Sam 08h–12h<br />Urgences 24h/24, 7j/7</p></div>
            </div>
          </div>

          <div v-reveal class="join-map">
            <iframe
              v-if="mapsKey"
              class="join-map-frame"
              :src="`https://www.google.com/maps/embed/v1/place?key=${mapsKey}&q=${encodeURIComponent(mapsQuery)}`"
              loading="lazy"
              referrerpolicy="no-referrer-when-downgrade"
              allowfullscreen
            ></iframe>
            <div v-else class="join-map-fallback">
              <p class="meta-item"><MapPin :size="15" aria-hidden="true" /> Route Akouédo, Riviera Sideci – Cocody, Abidjan</p>
              <a
                href="https://maps.google.com/?q=Clinique+Medicale+Saint+Viateur+Cocody+Abidjan"
                target="_blank"
                rel="noopener"
                class="btn-primary"
              >
                Itinéraire Google Maps →
              </a>
            </div>
          </div>
        </div>

        <div v-reveal class="join-form-wrap">
          <h3>Envoyer un message</h3>
          <div class="join-form" :class="{ 'is-sending': sending }">
            <div class="form-row">
              <div class="fg"><label>Nom complet</label><input v-model="name" type="text" placeholder="Votre nom…" /></div>
              <div class="fg"><label>Téléphone</label><input v-model="phone" type="tel" placeholder="+225 …" /></div>
            </div>
            <div class="fg"><label>Email</label><input v-model="email" type="email" placeholder="votre@email.com" /></div>
            <div class="fg"><label>Sujet</label><input v-model="subject" type="text" placeholder="Objet de votre message…" /></div>
            <div class="fg"><label>Message</label><textarea v-model="message" placeholder="Votre message…"></textarea></div>
            <HoneypotField v-model="honeypot" />
            <button class="btn-submit" :disabled="sending" @click="submitContact">Envoyer le message →</button>
            <LoadingOverlay v-if="sending" message="Envoi en cours…" />
          </div>
          <div v-if="sent" class="form-ok">✓ Votre message a été envoyé. Nous vous répondrons dans les 24h.</div>
        </div>
      </div>
    </div>
  </section>

  <section class="section join-jobs" style="background: var(--bg-alt)">
    <div class="section-inner">
      <div class="jobs-intro">
        <div>
          <p v-reveal class="section-kicker">Carrières</p>
          <h2 v-reveal="'words'" class="section-title d1">Rejoignez notre équipe</h2>
          <p v-reveal class="section-lead d2">
            Découvrez nos opportunités de carrière et participez à une prise en charge médicale d'excellence.
          </p>
        </div>
        <div v-reveal="'mask'" class="jobs-photo">
          <AmbientVideo class="jobs-media" media="recrutement" :poster="teamPhoto" poster-alt="L'équipe de la Clinique Médicale Saint Viateur" />
        </div>
      </div>

      <SkeletonGrid v-if="jobsLoading" :count="3" :min-width="300" :media="false" />
      <LoadError v-else-if="jobsError" title="Impossible de charger les offres d'emploi" @retry="loadJobs" />
      <div v-else-if="jobs.items.length" class="jobs-grid">
        <JobOfferCard v-for="(o, i) in jobs.items" :key="o.id" v-reveal="{ type: 'up', delay: (i % 3) * 90 }" :offer="o" />
      </div>
      <EmptyState
        v-else
        :icon="Briefcase"
        title="Aucune offre d'emploi actuellement"
        message="Revenez bientôt, de nouvelles opportunités sont publiées régulièrement."
      />
    </div>
  </section>

</template>

<style scoped>
.join-hero {
  background: var(--bg-alt);
}
.join-grid {
  display: grid;
  grid-template-columns: 1.3fr 1fr;
  gap: 48px;
  align-items: start;
}
.join-cards {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 22px;
}
.ccard {
  display: flex;
  align-items: flex-start;
  gap: 15px;
  background: var(--surface);
  border: 1px solid var(--border-soft);
  border-radius: 11px;
  padding: 18px 20px;
}
.ccard-icon {
  width: 42px;
  height: 42px;
  background: var(--bg-alt);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
  flex-shrink: 0;
}
.ccard h3 {
  font-family: var(--font-sans);
  font-size: 0.72rem;
  font-weight: 600;
  color: var(--heading);
  text-transform: uppercase;
  letter-spacing: 0.09em;
  margin-bottom: 4px;
}
.ccard a,
.ccard p {
  font-size: 0.86rem;
  color: var(--muted);
  text-decoration: none;
  display: block;
  line-height: 1.65;
}
.ccard a:hover {
  color: var(--blue);
}
.join-map {
  border-radius: 15px;
  overflow: hidden;
  border: 1px solid var(--border-soft);
  min-height: 280px;
}
.join-map-frame {
  width: 100%;
  height: 280px;
  border: none;
  display: block;
}
.join-map-fallback {
  height: 280px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 16px;
  background: var(--surface);
  text-align: center;
  padding: 20px;
}
.join-map-fallback p {
  color: var(--muted);
  font-size: 0.9rem;
}
.join-form-wrap {
  background: var(--surface);
  border: 1px solid var(--border-soft);
  border-radius: 15px;
  padding: 28px;
}
.join-form-wrap h3 {
  font-size: 1.25rem;
  color: var(--heading);
  margin-bottom: 20px;
}
.join-form {
  position: relative;
}
.join-form.is-sending .fg,
.join-form.is-sending .btn-submit {
  pointer-events: none;
  opacity: 0.45;
}
.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}
.fg {
  margin-bottom: 14px;
}
.fg label {
  display: block;
  font-size: 0.68rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.09em;
  color: var(--heading);
  margin-bottom: 6px;
}
.fg input,
.fg textarea {
  width: 100%;
  padding: 11px 14px;
  border: 1px solid var(--border-soft);
  border-radius: 8px;
  font-size: 0.88rem;
  color: var(--text);
  background: var(--bg);
  outline: none;
  transition: border-color 0.2s, box-shadow 0.2s;
}
.fg input:focus,
.fg textarea:focus {
  border-color: var(--blue);
  box-shadow: 0 0 0 3px rgba(200, 16, 46, 0.1);
}
.fg textarea {
  resize: vertical;
  min-height: 96px;
}
.form-ok {
  margin-top: 12px;
  background: #fde8ea;
  border: 1px solid #f0b0b8;
  border-radius: 8px;
  padding: 13px;
  color: var(--green);
  font-size: 0.88rem;
  text-align: center;
}
.jobs-intro {
  display: grid;
  grid-template-columns: 1.2fr 1fr;
  gap: 40px;
  align-items: center;
  margin-bottom: 36px;
}
.jobs-photo {
  border-radius: 15px;
  overflow: hidden;
  border: 1px solid var(--border-soft);
  aspect-ratio: 16 / 10;
  box-shadow: 0 16px 40px rgba(0, 0, 0, 0.1);
}
.jobs-media {
  width: 100%;
  height: 100%;
}
.jobs-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 18px;
}

@media (max-width: 980px) {
  .join-grid {
    grid-template-columns: 1fr;
  }
  .jobs-intro {
    grid-template-columns: 1fr;
  }
}
@media (max-width: 640px) {
  .form-row {
    grid-template-columns: 1fr;
  }
}
.ccard-icon {
  color: var(--blue);
}
</style>
