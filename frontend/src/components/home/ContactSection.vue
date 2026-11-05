<script setup lang="ts">
import { Check, Mail, MapPin, Phone, Send, Siren } from "@lucide/vue";
import { ref } from "vue";

import IconFacebook from "@/components/brand/IconFacebook.vue";
import LoadingOverlay from "@/components/common/LoadingOverlay.vue";
import Spinner from "@/components/common/Spinner.vue";
import { alertDialog } from "@/composables/useDialog";
import { OPENING_HOURS_WEEK, useClinicHours } from "@/composables/useClinicHours";
import { siteService } from "@/services/siteService";
import { useSpecialtiesStore } from "@/stores/specialties";

const specialties = useSpecialtiesStore();
const { todayName, consultationsOpen, statusLabel } = useClinicHours();

const name = ref("");
const phone = ref("");
const email = ref("");
const serviceType = ref("");
const urgency = ref<"urgence" | "programme">("urgence");
const wantsHospitalizationInfo = ref<"oui" | "non">("non");
const message = ref("");
const sent = ref(false);
const sending = ref(false);
const backLoading = ref(false);
const shake = ref(false);

async function submitForm() {
  if (!name.value.trim() || !serviceType.value || !message.value.trim()) {
    shake.value = false;
    requestAnimationFrame(() => (shake.value = true));
    await alertDialog("Veuillez remplir au moins votre nom, le service recherché et votre demande.", {
      title: "Formulaire incomplet",
    });
    return;
  }
  sending.value = true;
  try {
    await siteService.sendMessage({
      name: name.value.trim(),
      email: email.value.trim() || undefined,
      phone: phone.value.trim() || undefined,
      subject: serviceType.value,
      content: message.value.trim(),
      urgency: urgency.value,
      wants_hospitalization_info: wantsHospitalizationInfo.value === "oui",
    });
    sent.value = true;
    name.value = "";
    phone.value = "";
    email.value = "";
    serviceType.value = "";
    urgency.value = "urgence";
    wantsHospitalizationInfo.value = "non";
    message.value = "";
  } finally {
    sending.value = false;
  }
}

async function backToForm() {
  backLoading.value = true;
  await new Promise((resolve) => setTimeout(resolve, 450));
  sent.value = false;
  backLoading.value = false;
}
</script>

<template>
  <section id="contact" class="section contact-section" aria-labelledby="contact-title">
    <div class="section-inner">
      <p v-reveal class="section-kicker">Nous rejoindre</p>
      <h2 id="contact-title" v-reveal="'words'" class="section-title d1">Contact & Localisation</h2>
      <p v-reveal class="section-lead d2">
        Notre équipe est disponible pour vous accueillir, répondre à vos questions et vous orienter vers le bon
        praticien.
      </p>
      <div class="contact-grid">
        <div>
          <div class="contact-cards">
            <div v-reveal="'left'" class="ccard">
              <div class="ccard-icon"><MapPin :size="20" aria-hidden="true" /></div>
              <div><h3>Adresse</h3><p>Route Akouédo, Riviera Sideci – Cocody<br />22 BP 289, Abidjan 22, Côte d'Ivoire</p></div>
            </div>
            <div v-reveal="'left'" class="ccard d1">
              <div class="ccard-icon"><Phone :size="20" aria-hidden="true" /></div>
              <div>
                <h3>Téléphones</h3>
                <a href="tel:+2252722590417">+225 27 22 59 04 17 (principal)</a>
                <a href="tel:+2250101466576">+225 01 01 46 65 76</a>
                <a href="tel:+2250707095549">+225 07 07 09 55 49</a>
                <a href="tel:+2252247264700">+225 22 47 26 47</a>
              </div>
            </div>
            <div v-reveal="'left'" class="ccard d2">
              <div class="ccard-icon"><Mail :size="20" aria-hidden="true" /></div>
              <div><h3>Email</h3><a href="mailto:cliniquestviateur@aviso.ci">cliniquestviateur@aviso.ci</a></div>
            </div>
            <div v-reveal="'left'" class="ccard d3">
              <div class="ccard-icon"><IconFacebook :size="20" /></div>
              <div>
                <h3>Facebook</h3>
                <a href="https://www.facebook.com/CliniqueMedicaleSaintViateur/" target="_blank" rel="noopener">
                  CliniqueMedicaleSaintViateur<span class="sr-only"> (s'ouvre dans un nouvel onglet)</span>
                </a>
              </div>
            </div>
          </div>

          <div v-reveal class="form-wrap" :class="{ shake }" @animationend="shake = false">
            <Transition name="form-swap" mode="out-in">
              <form v-if="!sent" key="form" class="form-fields" :class="{ 'is-sending': sending }" novalidate @submit.prevent="submitForm">
                <h3>Envoyer un message</h3>
                <div class="form-row">
                  <div class="fg">
                    <label for="contact-name">Nom complet*</label>
                    <input id="contact-name" v-model="name" type="text" autocomplete="name" required placeholder="Votre nom…" />
                  </div>
                  <div class="fg">
                    <label for="contact-phone">Téléphone</label>
                    <input id="contact-phone" v-model="phone" type="tel" autocomplete="tel" placeholder="+225 …" />
                  </div>
                </div>
                <div class="fg">
                  <label for="contact-email">Email</label>
                  <input id="contact-email" v-model="email" type="email" autocomplete="email" placeholder="votre@email.com" />
                </div>
                <div class="fg">
                  <label for="contact-service">Quel type de service médical recherchez-vous ?*</label>
                  <select id="contact-service" v-model="serviceType" required>
                    <option value="" disabled>Sélectionnez un service médical</option>
                    <option v-for="s in specialties.items" :key="s.id" :value="s.name">{{ s.name }}</option>
                  </select>
                </div>
                <fieldset class="fg">
                  <legend>Avez-vous besoin d'une consultation urgente ou d'un rendez-vous programmé ?</legend>
                  <div class="radio-group">
                    <label class="radio-card" :class="{ active: urgency === 'urgence' }">
                      <input v-model="urgency" type="radio" value="urgence" />
                      <span class="radio-dot"></span>
                      Urgence
                    </label>
                    <label class="radio-card" :class="{ active: urgency === 'programme' }">
                      <input v-model="urgency" type="radio" value="programme" />
                      <span class="radio-dot"></span>
                      Rendez-vous programmé
                    </label>
                  </div>
                </fieldset>
                <fieldset class="fg">
                  <legend>Souhaitez-vous des informations sur les services d'hospitalisation ou de soins intensifs ?</legend>
                  <div class="radio-group">
                    <label class="radio-card" :class="{ active: wantsHospitalizationInfo === 'oui' }">
                      <input v-model="wantsHospitalizationInfo" type="radio" value="oui" />
                      <span class="radio-dot"></span>
                      Oui
                    </label>
                    <label class="radio-card" :class="{ active: wantsHospitalizationInfo === 'non' }">
                      <input v-model="wantsHospitalizationInfo" type="radio" value="non" />
                      <span class="radio-dot"></span>
                      Non
                    </label>
                  </div>
                </fieldset>
                <div class="fg">
                  <label for="contact-message">Votre demande*</label>
                  <textarea id="contact-message" v-model="message" required placeholder="Précisez votre besoin : localisation, délais…"></textarea>
                </div>
                <button class="btn-submit" type="submit" :disabled="sending">
                  <span class="btn-content"><Send :size="16" aria-hidden="true" /> Envoyer le message</span>
                </button>

                <LoadingOverlay v-if="sending" message="Envoi de votre demande…" />
              </form>

              <div v-else key="success" class="form-success" role="status">
                <!-- The check mark draws itself (stroke animation). -->
                <div class="form-success-icon" aria-hidden="true">
                  <svg viewBox="0 0 52 52">
                    <circle cx="26" cy="26" r="24" pathLength="1" />
                    <path d="M15 27 l7 7 l15 -16" pathLength="1" />
                  </svg>
                </div>
                <h3>Message envoyé !</h3>
                <p>Merci, votre demande a bien été transmise. Nous vous répondrons dans les 24h.</p>
                <button class="btn-submit" type="button" :disabled="backLoading" @click="backToForm">
                  <span class="btn-content"><Spinner v-if="backLoading" :size="14" />{{ backLoading ? "Retour…" : "← Retour au formulaire" }}</span>
                </button>
              </div>
            </Transition>
          </div>
        </div>

        <div>
          <div v-reveal="'right'" class="hours-card">
            <h3>Horaires d'ouverture <span class="open-now">Urgences 24h/24</span></h3>
            <p class="hours-status" :class="{ open: consultationsOpen }" role="status">
              <span class="hours-dot" aria-hidden="true"></span>{{ statusLabel }}
            </p>
            <table class="hours-table">
              <caption class="sr-only">Horaires des consultations</caption>
              <tbody>
                <tr v-for="d in OPENING_HOURS_WEEK" :key="d.day" :class="{ today: d.day === todayName }">
                  <th scope="row">
                    {{ d.day }}<span v-if="d.day === todayName" class="today-tag">Aujourd'hui</span>
                  </th>
                  <td>{{ d.open ? `${d.open} – ${d.close}` : "Urgences seulement" }}</td>
                </tr>
              </tbody>
            </table>
            <div class="urgences-note">
              <Siren :size="15" class="inline-icon" aria-hidden="true" /> Les urgences et la réanimation sont disponibles
              <strong>24 heures sur 24, 7 jours sur 7</strong> sans interruption.
            </div>
            <a href="tel:+2252722590417" class="hours-call"><Phone :size="16" aria-hidden="true" /> Appeler le 27 22 59 04 17</a>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.contact-section {
  background: var(--bg-alt);
}
.contact-grid {
  display: grid;
  grid-template-columns: 1.3fr 1fr;
  gap: 48px;
  align-items: start;
}
.contact-cards {
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
  transition:
    border-color var(--dur-fast),
    translate var(--dur-base) var(--ease-out);
}
.ccard:hover {
  border-color: #e8a8ae;
  translate: 4px 0;
}
.ccard-icon {
  width: 42px;
  height: 42px;
  background: var(--offwhite);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  color: var(--blue);
}
.ccard h3 {
  font-family: "DM Sans", sans-serif;
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

/* ─── Form ─── */
.form-wrap {
  background: var(--surface);
  border: 1px solid var(--border-soft);
  border-radius: 15px;
  padding: 28px;
}
.form-wrap.shake {
  animation: shake 0.5s var(--ease-out);
}
@keyframes shake {
  20%,
  60% {
    translate: -8px 0;
  }
  40%,
  80% {
    translate: 8px 0;
  }
}
.form-wrap h3 {
  font-size: 1.25rem;
  color: var(--heading);
  margin-bottom: 20px;
}
.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}
.fg {
  margin-bottom: 14px;
}
fieldset.fg {
  border: 0;
  min-width: 0;
}
.fg label,
.fg legend {
  display: block;
  padding: 0;
  font-size: 0.68rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.09em;
  color: var(--heading);
  margin-bottom: 6px;
}
.fg input,
.fg select,
.fg textarea {
  width: 100%;
  padding: 11px 14px;
  border: 1px solid var(--border-soft);
  border-radius: 8px;
  font-size: 0.88rem;
  color: var(--text);
  background: var(--bg);
  outline: none;
  transition:
    border-color 0.2s,
    box-shadow 0.2s;
}
.fg input:focus,
.fg select:focus,
.fg textarea:focus {
  border-color: var(--blue);
  box-shadow: 0 0 0 3px rgba(200, 16, 46, 0.1);
}
.fg textarea {
  resize: vertical;
  min-height: 96px;
}
.radio-group {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
}
.radio-group label.radio-card {
  position: relative;
  display: flex;
  align-items: center;
  gap: 9px;
  padding: 11px 14px;
  border: 1px solid var(--border-soft);
  border-radius: 8px;
  background: var(--bg);
  font-size: 0.85rem;
  font-weight: 500;
  text-transform: none;
  letter-spacing: normal;
  margin-bottom: 0;
  color: var(--text);
  cursor: pointer;
  transition:
    border-color 0.2s,
    box-shadow 0.2s;
}
/* Visually hidden but still focusable/operable with the keyboard (arrow keys). */
.radio-card input {
  position: absolute;
  width: 1px;
  height: 1px;
  opacity: 0;
  pointer-events: none;
}
.radio-card:has(input:focus-visible) {
  outline: 2px solid var(--blue);
  outline-offset: 2px;
}
.radio-dot {
  display: inline-block;
  width: 15px;
  height: 15px;
  border-radius: 50%;
  border: 1.5px solid #e8c3c6;
  flex-shrink: 0;
  position: relative;
  transition: border-color 0.2s;
}
.radio-card.active {
  border-color: var(--blue);
  box-shadow: 0 0 0 3px rgba(200, 16, 46, 0.1);
}
.radio-card.active .radio-dot {
  border-color: var(--blue);
}
.radio-card.active .radio-dot::after {
  content: "";
  position: absolute;
  inset: 3px;
  border-radius: 50%;
  background: var(--blue);
  animation: dotIn 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
}
@keyframes dotIn {
  from {
    scale: 0;
  }
}
.form-fields {
  position: relative;
}
.form-fields.is-sending .fg,
.form-fields.is-sending .btn-submit {
  pointer-events: none;
  opacity: 0.45;
}
.form-swap-enter-active,
.form-swap-leave-active {
  transition:
    opacity 0.35s var(--ease-out),
    translate 0.35s var(--ease-out);
}
.form-swap-enter-from {
  opacity: 0;
  translate: 0 16px;
}
.form-swap-leave-to {
  opacity: 0;
  translate: 0 -16px;
}
.form-success {
  text-align: center;
  padding: 26px 6px;
}
.form-success-icon {
  width: 64px;
  height: 64px;
  margin: 0 auto 18px;
}
.form-success-icon svg {
  width: 100%;
  height: 100%;
  fill: none;
  stroke-linecap: round;
  stroke-linejoin: round;
}
.form-success-icon circle {
  stroke: var(--brand-600);
  stroke-width: 2.5;
  stroke-dasharray: 1;
  stroke-dashoffset: 1;
  animation: draw 0.7s var(--ease-out) 0.1s forwards;
}
.form-success-icon path {
  stroke: var(--brand-600);
  stroke-width: 3.5;
  stroke-dasharray: 1;
  stroke-dashoffset: 1;
  animation: draw 0.45s var(--ease-out) 0.65s forwards;
}
@keyframes draw {
  to {
    stroke-dashoffset: 0;
  }
}
.form-success h3 {
  color: var(--heading);
  font-size: 1.2rem;
  margin-bottom: 8px;
}
.form-success p {
  color: var(--muted);
  font-size: 0.88rem;
  line-height: 1.6;
  margin-bottom: 22px;
}
.form-success .btn-submit {
  max-width: 260px;
  margin: 0 auto;
}

/* ─── Hours ─── */
.hours-card {
  background: var(--brand-700);
  border-radius: 15px;
  padding: 26px;
  position: sticky;
  top: 120px;
}
.hours-card h3 {
  color: #fff;
  font-size: 1.15rem;
  margin-bottom: 12px;
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
}
.open-now {
  background: var(--brand-600);
  color: #fff;
  font-family: "DM Sans", sans-serif;
  font-size: 0.6rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  padding: 3px 9px;
  border-radius: 100px;
}
.hours-status {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.8rem;
  color: #fde68a;
  margin-bottom: 14px;
}
.hours-status.open {
  color: #86efac;
}
.hours-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: currentColor;
  box-shadow: 0 0 0 4px rgba(255, 255, 255, 0.08);
}
.hours-table {
  width: 100%;
  border-collapse: collapse;
}
.hours-table th,
.hours-table td {
  padding: 8px 6px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.07);
  font-size: 0.86rem;
  font-weight: 400;
  color: rgba(255, 255, 255, 0.75);
  text-align: left;
}
.hours-table tr:last-child th,
.hours-table tr:last-child td {
  border-bottom: none;
}
.hours-table td {
  text-align: right;
  color: rgba(255, 255, 255, 0.62);
}
.hours-table tr.today th,
.hours-table tr.today td {
  color: #fff;
  font-weight: 600;
  background: rgba(255, 255, 255, 0.07);
}
.hours-table tr.today th {
  border-radius: 6px 0 0 6px;
}
.hours-table tr.today td {
  border-radius: 0 6px 6px 0;
}
.today-tag {
  margin-left: 8px;
  font-size: 0.6rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--brand-200);
}
.urgences-note {
  margin-top: 14px;
  background: rgba(200, 16, 46, 0.18);
  border: 1px solid rgba(200, 16, 46, 0.35);
  border-radius: 8px;
  padding: 11px 14px;
  font-size: 0.8rem;
  color: rgba(255, 255, 255, 0.82);
  line-height: 1.55;
}
.inline-icon {
  vertical-align: -2px;
  margin-right: 2px;
}
.hours-call {
  margin-top: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 12px;
  border-radius: 8px;
  background: #fff;
  color: var(--brand-700);
  font-weight: 700;
  font-size: 0.88rem;
  text-decoration: none;
  transition:
    translate var(--dur-fast) var(--ease-out),
    box-shadow var(--dur-fast);
}
.hours-call:hover {
  translate: 0 -2px;
  box-shadow: 0 10px 24px rgba(0, 0, 0, 0.25);
}

@media (max-width: 980px) {
  .contact-grid {
    grid-template-columns: 1fr;
  }
  .hours-card {
    position: static;
  }
}
@media (max-width: 640px) {
  .form-wrap {
    padding: 20px;
  }
  .form-row,
  .radio-group {
    grid-template-columns: 1fr;
  }
}
</style>
