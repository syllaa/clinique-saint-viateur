<script setup lang="ts">
import { Clock, Mail, MapPin, Navigation, Phone, Siren, Trophy } from "@lucide/vue";
import { onMounted, ref } from "vue";

import BlogGrid from "@/components/blog/BlogGrid.vue";
import IconFacebook from "@/components/brand/IconFacebook.vue";
import LoadError from "@/components/common/LoadError.vue";
import LoadingOverlay from "@/components/common/LoadingOverlay.vue";
import Spinner from "@/components/common/Spinner.vue";
import HeroCanvas from "@/components/hero/HeroCanvas.vue";
import PromotionCarousel from "@/components/promotions/PromotionCarousel.vue";
import SpecialtyMedia from "@/components/specialties/SpecialtyMedia.vue";
import aboutPhoto from "@/assets/images/hero/hero-clinic-facade-street.webp";
import { alertDialog } from "@/composables/useDialog";
import { resetSeo } from "@/composables/useHead";
import { siteService } from "@/services/siteService";
import { usePromotionsStore } from "@/stores/promotions";
import { useSpecialtiesStore } from "@/stores/specialties";
import { TESTIMONIALS as testimonials } from "@/constants/testimonials";
import { magnetic } from "@/motion/animations";
import { useScrollScene } from "@/motion/useScrollScene";

const specialties = useSpecialtiesStore();

// Hero scene: CTAs follow the cursor slightly; the hero content drifts up and
// fades as the visitor scrolls past it (depth effect over the canvas).
const heroRef = ref<HTMLElement | null>(null);
useScrollScene(heroRef, (kit, hero) => {
  const cleanups = Array.from(hero.querySelectorAll<HTMLElement>(".hero-btns a")).map((btn) => magnetic(kit, btn, 0.22));
  kit.gsap.to(hero.querySelector(".hero-inner"), {
    yPercent: -10,
    autoAlpha: 0.25,
    ease: "none",
    scrollTrigger: { trigger: hero, start: "top top", end: "bottom top", scrub: true },
  });
  return () => cleanups.forEach((fn) => fn());
});
const promotions = usePromotionsStore();

const servicesError = ref(false);
const servicesRetrying = ref(false);

async function loadServices() {
  servicesError.value = false;
  servicesRetrying.value = true;
  try {
    await specialties.fetchAll();
  } catch {
    servicesError.value = true;
  } finally {
    servicesRetrying.value = false;
  }
}

onMounted(() => {
  loadServices();
  // The offers section simply stays hidden if this fails (it is v-if'd on items).
  promotions.fetchActive().catch(() => undefined);
  resetSeo();
});

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

async function submitForm() {
  if (!name.value.trim() || !serviceType.value || !message.value.trim()) {
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

  <!-- HERO -->
  <section id="hero" ref="heroRef">
    <HeroCanvas />
    <div class="hero-grad"></div>
    <div class="hero-grid"></div>
    <div class="ring"></div>
    <div class="ring"></div>
    <div class="ring"></div>
    <div class="hero-bottom-fade"></div>

    <div class="hero-inner">
      <div>
        <div v-reveal class="hero-badge"><span class="live-dot"></span> Ouvert 24h/24 · 7j/7 · 79 897 patients</div>
        <h1 v-reveal="'words'" class="hero-title d1">Des soins de qualité,<br />au cœur de la <em>Riviera</em><br />Sideci.</h1>
        <p v-reveal class="hero-sub d2">
          Établissement médical privé de référence à Cocody, Abidjan. Une équipe de professionnels expérimentés, des
          équipements modernes et une prise en charge complète pour toute la famille.
        </p>
        <div v-reveal class="hero-btns d3">
          <a href="tel:+2252722590417" class="btn-primary"><Phone :size="16" aria-hidden="true" /> Prendre rendez-vous</a>
          <a href="#services" class="btn-outline-light">Nos services →</a>
        </div>
        <div v-reveal class="hero-stats d4">
          <div class="hstat"><div class="hstat-n" v-count-up="{ target: 79, suffix: 'K+' }">0K+</div><div class="hstat-l">Patients fidèles</div></div>
          <div class="hstat"><div class="hstat-n" v-count-up="{ target: 10, suffix: '+' }">0+</div><div class="hstat-l">Spécialités</div></div>
          <div class="hstat"><div class="hstat-n">24/7</div><div class="hstat-l">Urgences & soins</div></div>
        </div>
      </div>

      <div class="hero-right">
        <div class="urgence-box">
          <div class="urgence-label"><span class="pulse-ring"></span> Urgences disponibles maintenant</div>
          <div class="urgence-phone">27 22 59 04 17</div>
          <div class="urgence-sub">Ligne principale · 24h/24 · 7j/7</div>
        </div>
        <div class="info-stack">
          <div class="icard">
            <div class="icard-icon"><MapPin :size="18" aria-hidden="true" /></div>
            <p><strong>Adresse</strong>Route Akouédo, Riviera Sideci – Cocody<br />22 BP 289, Abidjan 22</p>
          </div>
          <div class="icard">
            <div class="icard-icon"><Phone :size="18" aria-hidden="true" /></div>
            <p><strong>Autres lignes</strong>01 01 46 65 76 &nbsp;·&nbsp; 07 07 09 55 49 &nbsp;·&nbsp; 22 47 26 47</p>
          </div>
          <div class="icard">
            <div class="icard-icon"><Mail :size="18" aria-hidden="true" /></div>
            <p><strong>Email</strong>cliniquestviateur@aviso.ci</p>
          </div>
          <div class="icard">
            <div class="icard-icon"><IconFacebook :size="18" /></div>
            <p><strong>Facebook</strong>CliniqueMedicaleSaintViateur</p>
          </div>
        </div>
      </div>
    </div>

    <div class="scroll-hint">
      <div class="scroll-mouse"><div class="scroll-wheel"></div></div>
      <span>Défiler</span>
    </div>
  </section>

  <!-- STRIP -->
  <div class="strip">
    <div class="strip-item"><Clock :size="16" aria-hidden="true" /> Lun – Ven : 08h–20h</div>
    <div class="strip-item"><Clock :size="16" aria-hidden="true" /> Samedi : 08h–12h</div>
    <div class="strip-item"><Siren :size="16" aria-hidden="true" /> Urgences 24h/24 · 7j/7</div>
    <div class="strip-item"><MapPin :size="16" aria-hidden="true" /> Riviera Sideci, Cocody – Abidjan</div>
    <div class="strip-item"><Trophy :size="16" aria-hidden="true" /> 3ᵉ Prix national d'excellence médicale</div>
  </div>

  <!-- SERVICES -->
  <section id="services" class="section">
    <div class="section-inner">
      <p v-reveal class="section-kicker">Nos spécialités</p>
      <h2 v-reveal="'words'" class="section-title d1">Une gamme complète de soins médicaux</h2>
      <p v-reveal class="section-lead d2">
        De la médecine générale aux spécialités les plus pointues, la Clinique Saint Viateur vous accueille avec un
        plateau technique complet et des médecins qualifiés.
      </p>
      <div class="svc-grid">
        <RouterLink
          v-for="s in specialties.items"
          :key="s.id"
          :to="`/specialites/${s.slug}`"
          v-reveal
          class="svc-card"
        >
          <SpecialtyMedia
            class="svc-icon"
            :media-type="s.media_type"
            :icon-name="s.icon_name"
            :image-url="s.cover_image_url"
            :image-alt="s.image_alt"
            :name="s.name"
          />
          <h3>{{ s.name }}</h3>
          <p>{{ s.description }}</p>
        </RouterLink>
      </div>
      <LoadError
        v-if="servicesError && !specialties.items.length"
        title="Impossible de charger nos spécialités"
        :retrying="servicesRetrying"
        @retry="loadServices"
      />
      <div class="svc-more">
        <RouterLink to="/specialites" class="btn-outline">Voir toutes nos spécialités →</RouterLink>
      </div>
    </div>
  </section>

  <!-- OFFERS -->
  <section v-if="promotions.items.length" id="offres" class="section" style="background: var(--bg-alt)">
    <div class="section-inner">
      <p v-reveal class="section-kicker">Nos offres</p>
      <h2 v-reveal="'words'" class="section-title d1">Offres et promotions du moment</h2>
      <p v-reveal class="section-lead d2">
        Profitez de nos offres en cours et faites-nous savoir ce que vous en pensez.
      </p>
      <PromotionCarousel :items="promotions.items" />
      <div class="svc-more">
        <RouterLink to="/promotions" class="btn-outline">Voir toutes nos offres →</RouterLink>
      </div>
    </div>
  </section>

  <!-- ABOUT -->
  <section id="about" class="section about-section">
    <div class="section-inner about-inner">
      <div>
        <p v-reveal class="section-kicker" style="color: var(--sky-light)">Notre histoire</p>
        <h2 v-reveal="'words'" class="section-title d1" style="color: #fff">Une clinique moderne,<br />une médecine humaine</h2>
        <p v-reveal class="section-lead d2" style="color: rgba(255, 255, 255, 0.55); margin-bottom: 28px">
          Établissement privé de référence dans le quartier de Riviera Sideci à Cocody, la Clinique Médicale Saint
          Viateur conjugue expertise médicale, équipements de pointe et accueil chaleureux pour offrir les meilleurs
          soins à toute la population abidjanaise et au-delà.
        </p>
        <ul class="check-list">
          <li v-reveal class="check-item"><span class="check-icon">✓</span>Équipe médicale pluridisciplinaire qualifiée et expérimentée</li>
          <li v-reveal class="check-item"><span class="check-icon">✓</span>Équipements médicaux modernes et laboratoire complet</li>
          <li v-reveal class="check-item"><span class="check-icon">✓</span>Urgences et réanimation disponibles 24h/24, 7j/7</li>
          <li v-reveal class="check-item"><span class="check-icon">✓</span>Accueil professionnel, bienveillant et accessible à tous</li>
          <li v-reveal class="check-item"><span class="check-icon">✓</span>Lauréate du 3ᵉ Prix national d'excellence médicale en Côte d'Ivoire</li>
          <li v-reveal class="check-item"><span class="check-icon">✓</span>Plus de 79 897 patients nous font confiance</li>
        </ul>
      </div>
      <div class="about-visual">
        <div v-reveal="'mask'" class="about-photo">
          <img :src="aboutPhoto" alt="Façade de la Clinique Médicale Saint Viateur à Cocody" loading="lazy" />
        </div>
        <div class="about-stats">
          <div v-reveal class="astat"><div class="astat-n" v-count-up="{ target: 79, suffix: 'K+' }">0K+</div><div class="astat-l">Patients satisfaits</div></div>
          <div v-reveal class="astat gold"><div class="astat-n">24<span style="font-size: 1.1rem">/7</span></div><div class="astat-l">Urgences en permanence</div></div>
          <div v-reveal class="astat gold"><div class="astat-n" v-count-up="{ target: 10, suffix: '+' }">0+</div><div class="astat-l">Spécialités médicales</div></div>
          <div v-reveal class="astat"><div class="astat-n">3<sup>ᵉ</sup></div><div class="astat-l">Prix national d'excellence</div></div>
        </div>
      </div>
    </div>
  </section>

  <!-- BLOG -->
  <section id="blog" class="section" style="background: var(--bg-alt)">
    <div class="section-inner">
      <p v-reveal class="section-kicker">Notre blog médical</p>
      <h2 v-reveal="'words'" class="section-title d1">Actualités & Conseils santé</h2>
      <p v-reveal class="section-lead d2">
        Restez informé des actualités de la clinique, des conseils de prévention et des nouvelles médicales utiles
        pour votre santé et celle de votre famille.
      </p>
      <BlogGrid />
      <div class="svc-more">
        <RouterLink to="/blog" class="btn-outline">Voir tous les articles →</RouterLink>
      </div>
    </div>
  </section>

  <!-- TESTIMONIALS -->
  <section id="temoignages" class="section">
    <div class="section-inner">
      <p v-reveal class="section-kicker">Avis de nos patients</p>
      <h2 v-reveal="'words'" class="section-title d1">Ils nous font confiance</h2>
      <p v-reveal class="section-lead d2">
        La satisfaction de nos patients est notre première récompense. Voici quelques témoignages partagés par nos
        patients sur Facebook et lors de leur passage.
      </p>
      <div class="testi-grid">
        <div v-for="t in testimonials" :key="t.author" v-reveal class="testi-card">
          <div class="quote-mark">"</div>
          <div class="testi-stars">{{ t.stars }}</div>
          <p class="testi-text">{{ t.text }}</p>
          <div class="testi-author">{{ t.author }}</div>
          <div class="testi-meta">{{ t.meta }}</div>
        </div>
      </div>
    </div>
  </section>

  <!-- CONTACT -->
  <section id="contact" class="section" style="background: var(--bg-alt)">
    <div class="section-inner">
      <p v-reveal class="section-kicker">Nous rejoindre</p>
      <h2 v-reveal="'words'" class="section-title d1">Contact & Localisation</h2>
      <p v-reveal class="section-lead d2">
        Notre équipe est disponible pour vous accueillir, répondre à vos questions et vous orienter vers le bon
        praticien.
      </p>
      <div class="contact-grid">
        <div>
          <div class="contact-cards">
            <div v-reveal class="ccard">
              <div class="ccard-icon"><MapPin :size="20" aria-hidden="true" /></div>
              <div><h3>Adresse</h3><p>Route Akouédo, Riviera Sideci – Cocody<br />22 BP 289, Abidjan 22, Côte d'Ivoire</p></div>
            </div>
            <div v-reveal class="ccard">
              <div class="ccard-icon"><Phone :size="20" aria-hidden="true" /></div>
              <div>
                <h3>Téléphones</h3>
                <a href="tel:+2252722590417">+225 27 22 59 04 17 (principal)</a>
                <a href="tel:+2250101466576">+225 01 01 46 65 76</a>
                <a href="tel:+2250707095549">+225 07 07 09 55 49</a>
                <a href="tel:+2252247264700">+225 22 47 26 47</a>
              </div>
            </div>
            <div v-reveal class="ccard">
              <div class="ccard-icon"><Mail :size="20" aria-hidden="true" /></div>
              <div><h3>Email</h3><a href="mailto:cliniquestviateur@aviso.ci">cliniquestviateur@aviso.ci</a></div>
            </div>
            <div v-reveal class="ccard">
              <div class="ccard-icon"><IconFacebook :size="20" /></div>
              <div><h3>Facebook</h3><a href="https://www.facebook.com/CliniqueMedicaleSaintViateur/" target="_blank" rel="noopener">CliniqueMedicaleSaintViateur</a></div>
            </div>
          </div>
          <div v-reveal class="form-wrap">
            <div v-if="!sent" class="form-fields" :class="{ 'is-sending': sending }">
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
                    <input type="radio" value="urgence" v-model="urgency" />
                    <span class="radio-dot"></span>
                    Urgence
                  </label>
                  <label class="radio-card" :class="{ active: urgency === 'programme' }">
                    <input type="radio" value="programme" v-model="urgency" />
                    <span class="radio-dot"></span>
                    Rendez-vous programmé
                  </label>
                </div>
              </fieldset>
              <fieldset class="fg">
                <legend>Souhaitez-vous des informations sur les services d'hospitalisation ou de soins intensifs ?</legend>
                <div class="radio-group">
                  <label class="radio-card" :class="{ active: wantsHospitalizationInfo === 'oui' }">
                    <input type="radio" value="oui" v-model="wantsHospitalizationInfo" />
                    <span class="radio-dot"></span>
                    Oui
                  </label>
                  <label class="radio-card" :class="{ active: wantsHospitalizationInfo === 'non' }">
                    <input type="radio" value="non" v-model="wantsHospitalizationInfo" />
                    <span class="radio-dot"></span>
                    Non
                  </label>
                </div>
              </fieldset>
              <div class="fg">
                <label for="contact-message">Votre demande*</label>
                <textarea id="contact-message" v-model="message" required placeholder="Précisez votre besoin : localisation, délais…"></textarea>
              </div>
              <button class="btn-submit" :disabled="sending" @click="submitForm">
                <span class="btn-content">Envoyer le message →</span>
              </button>

              <LoadingOverlay v-if="sending" message="Envoi de votre demande…" />
            </div>

            <div v-else class="form-success">
              <div class="form-success-icon">✓</div>
              <h3>Message envoyé !</h3>
              <p>Merci, votre demande a bien été transmise. Nous vous répondrons dans les 24h.</p>
              <button class="btn-submit" type="button" :disabled="backLoading" @click="backToForm">
                <span class="btn-content"><Spinner v-if="backLoading" :size="14" />{{ backLoading ? "Retour…" : "← Retour au formulaire" }}</span>
              </button>
            </div>
          </div>
        </div>

        <div>
          <div v-reveal class="hours-card">
            <h3>Horaires d'ouverture <span class="open-now">Urgences 24h/24</span></h3>
            <table class="hours-table">
              <tr><td>Lundi</td><td>08:00 – 20:00</td></tr>
              <tr><td>Mardi</td><td>08:00 – 20:00</td></tr>
              <tr><td>Mercredi</td><td>08:00 – 20:00</td></tr>
              <tr><td>Jeudi</td><td>08:00 – 20:00</td></tr>
              <tr><td>Vendredi</td><td>08:00 – 20:00</td></tr>
              <tr><td>Samedi</td><td>08:00 – 12:00</td></tr>
              <tr><td>Dimanche</td><td style="color: rgba(255, 255, 255, 0.38)">Urgences seulement</td></tr>
            </table>
            <div class="urgences-note">
              <Siren :size="15" class="inline-icon" aria-hidden="true" /> Les urgences et la réanimation sont disponibles <strong>24 heures sur 24, 7 jours sur 7</strong> sans
              interruption.
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- MAP CTA -->
  <div class="map-banner">
    <div style="position: relative; z-index: 1">
      <h2 v-reveal>Venez nous rendre visite</h2>
      <p v-reveal class="d1">Route Akouédo, Riviera Sideci – Cocody, Abidjan · Proche Riviera 3 et Lycée Blaise-Pascal</p>
      <a
        v-reveal
        class="d2 btn-white"
        href="https://maps.google.com/?q=Clinique+Medicale+Saint+Viateur+Cocody+Abidjan"
        target="_blank"
        rel="noopener"
      >
        <Navigation :size="16" aria-hidden="true" /> Itinéraire Google Maps
      </a>
    </div>
  </div>

</template>

<style scoped>
/* ─── HERO ─── */
#hero {
  min-height: 100vh;
  position: relative;
  overflow: hidden;
  display: flex;
  align-items: center;
  padding: 100px 5vw 80px;
}
.hero-grad {
  position: absolute;
  inset: 0;
  z-index: 1;
  pointer-events: none;
  background: linear-gradient(155deg, rgba(24, 8, 9, 0.97) 0%, rgba(122, 15, 26, 0.9) 55%, rgba(143, 22, 32, 0.82) 100%);
}
.hero-grid {
  position: absolute;
  inset: 0;
  z-index: 1;
  pointer-events: none;
  background-image:
    linear-gradient(rgba(255, 255, 255, 0.025) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255, 255, 255, 0.025) 1px, transparent 1px);
  background-size: 55px 55px;
  mask-image: radial-gradient(ellipse 70% 80% at 40% 50%, black 0%, transparent 100%);
}
.hero-bottom-fade {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 130px;
  z-index: 2;
  pointer-events: none;
  background: linear-gradient(to top, var(--bg) 0%, transparent 75%);
}
.ring {
  position: absolute;
  border-radius: 50%;
  border: 1px solid rgba(200, 16, 46, 0.1);
  pointer-events: none;
  z-index: 1;
  top: 50%;
  left: 60%;
  transform: translate(-50%, -50%);
}
.ring:nth-child(4) {
  width: 550px;
  height: 550px;
}
.ring:nth-child(5) {
  width: 780px;
  height: 780px;
}
.ring:nth-child(6) {
  width: 1050px;
  height: 1050px;
}
.hero-inner {
  max-width: 1200px;
  margin: 0 auto;
  width: 100%;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 56px;
  align-items: center;
  position: relative;
  z-index: 5;
}
.hero-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: rgba(200, 16, 46, 0.1);
  border: 1px solid rgba(200, 16, 46, 0.3);
  color: var(--gold-lt);
  font-size: 0.7rem;
  font-weight: 600;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  padding: 6px 14px;
  border-radius: 100px;
  margin-bottom: 22px;
}
.live-dot,
.pulse-ring {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: var(--green);
  animation: livePulse 2.2s infinite;
}
@keyframes livePulse {
  0% {
    box-shadow: 0 0 0 0 rgba(30, 140, 90, 0.55);
  }
  70% {
    box-shadow: 0 0 0 8px rgba(30, 140, 90, 0);
  }
  100% {
    box-shadow: 0 0 0 0 rgba(30, 140, 90, 0);
  }
}
@media (prefers-reduced-motion: reduce) {
  .live-dot,
  .pulse-ring {
    animation: none;
  }
}
.hero-title {
  font-size: clamp(2.3rem, 3.8vw, 3.5rem);
  color: #fff;
  line-height: 1.1;
  margin-bottom: 18px;
}
.hero-title em {
  color: var(--sky-light);
  font-style: italic;
}
.hero-sub {
  color: rgba(255, 255, 255, 0.6);
  font-size: 0.97rem;
  max-width: 450px;
  line-height: 1.8;
  margin-bottom: 32px;
}
.hero-btns {
  display: flex;
  gap: 14px;
  flex-wrap: wrap;
}
.hero-stats {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
  margin-top: 40px;
}
.hstat {
  background: rgba(24, 8, 9, 0.55);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.12);
  border-radius: 10px;
  padding: 16px;
  text-align: center;
}
.hstat-n {
  font-family: "Cormorant Garamond", serif;
  font-size: 2rem;
  color: var(--gold-lt);
  line-height: 1;
}
.hstat-l {
  font-size: 0.68rem;
  color: rgba(255, 255, 255, 0.72);
  margin-top: 4px;
  letter-spacing: 0.05em;
}
.hero-right {
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.urgence-box {
  background: linear-gradient(135deg, var(--green), #5c0f18);
  border-radius: 14px;
  padding: 22px 26px;
  color: #fff;
  text-align: center;
}
.urgence-label {
  font-size: 0.66rem;
  letter-spacing: 0.16em;
  text-transform: uppercase;
  opacity: 0.75;
  margin-bottom: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}
.urgence-phone {
  font-family: "Cormorant Garamond", serif;
  font-size: 1.9rem;
  font-weight: 700;
  letter-spacing: 0.02em;
}
.urgence-sub {
  font-size: 0.73rem;
  opacity: 0.65;
  margin-top: 4px;
}
.info-stack {
  display: flex;
  flex-direction: column;
  gap: 9px;
}
.icard {
  display: flex;
  align-items: center;
  gap: 13px;
  background: rgba(24, 8, 9, 0.55);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.12);
  border-radius: 10px;
  padding: 13px 16px;
  color: #fff;
}
.icard-icon {
  font-size: 1.2rem;
  flex-shrink: 0;
  width: 24px;
  text-align: center;
}
.icard p {
  font-size: 0.8rem;
  line-height: 1.45;
  opacity: 0.88;
}
.icard p strong {
  display: block;
  font-size: 0.62rem;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  opacity: 0.48;
  margin-bottom: 2px;
  font-weight: 500;
}
.scroll-hint {
  position: absolute;
  bottom: 28px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 5;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  color: rgba(255, 255, 255, 0.35);
  font-size: 0.65rem;
  letter-spacing: 0.13em;
  text-transform: uppercase;
}
.scroll-mouse {
  width: 21px;
  height: 34px;
  border: 1.5px solid rgba(255, 255, 255, 0.22);
  border-radius: 11px;
  display: flex;
  justify-content: center;
  padding-top: 5px;
}
.scroll-wheel {
  width: 2.5px;
  height: 6px;
  background: rgba(255, 255, 255, 0.5);
  border-radius: 2px;
}

/* ─── TICKER ─── */
.strip {
  background: var(--blue);
  padding: 14px 5vw;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 36px;
  flex-wrap: wrap;
}
.strip-item {
  display: flex;
  align-items: center;
  gap: 9px;
  color: rgba(255, 255, 255, 0.88);
  font-size: 0.82rem;
}

/* ─── SERVICES ─── */
#services {
  background: var(--bg);
}
.svc-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(205px, 1fr));
  gap: 16px;
}
.svc-card {
  display: block;
  background: var(--surface);
  border-radius: 13px;
  padding: 26px 20px;
  border: 1px solid var(--border-soft);
  text-decoration: none;
  color: inherit;
  transition:
    transform 0.35s cubic-bezier(0.22, 0.68, 0, 1.2),
    box-shadow 0.35s,
    border-color 0.35s;
}
.svc-more {
  text-align: center;
  margin-top: 30px;
}
.svc-card:hover {
  transform: translateY(-7px);
  box-shadow: 0 18px 44px rgba(150, 12, 30, 0.11);
  border-color: #e8a8ae;
}
.svc-card:hover .svc-icon:not(.is-image) {
  transform: scale(1.12) rotate(-6deg);
  background: #fbe1e3;
}
.svc-card.rv.vis .svc-icon {
  animation: iconPop 0.6s cubic-bezier(0.34, 1.56, 0.64, 1) 0.15s backwards;
}
@keyframes iconPop {
  0% {
    transform: scale(0.4) rotate(-14deg);
    opacity: 0;
  }
  100% {
    transform: scale(1) rotate(0);
    opacity: 1;
  }
}
@media (prefers-reduced-motion: reduce) {
  .svc-card.rv.vis .svc-icon {
    animation: none;
  }
}
.svc-card h3 {
  font-family: "DM Sans", sans-serif;
  font-size: 0.92rem;
  font-weight: 600;
  color: var(--heading);
  margin-bottom: 6px;
}
.svc-card p {
  font-size: 0.78rem;
  color: var(--muted);
  line-height: 1.6;
}

/* ─── ABOUT ─── */
.about-section {
  background: var(--navy);
  position: relative;
  overflow: hidden;
}
.about-inner {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 72px;
  align-items: center;
  position: relative;
  z-index: 1;
}
.check-list {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 11px;
}
.check-item {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  color: rgba(255, 255, 255, 0.82);
  font-size: 0.87rem;
  line-height: 1.6;
  padding: 9px 13px;
  border-radius: 8px;
}
.check-icon {
  width: 22px;
  height: 22px;
  border-radius: 50%;
  background: var(--teal);
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.62rem;
  font-weight: 700;
  flex-shrink: 0;
}
.about-visual {
  display: flex;
  flex-direction: column;
  gap: 22px;
}
.about-photo {
  border-radius: 16px;
  overflow: hidden;
  border: 1px solid rgba(255, 255, 255, 0.09);
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.28);
  aspect-ratio: 16 / 10;
}
.about-photo img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center;
  display: block;
  animation: kenBurns 18s ease-in-out infinite alternate;
  transition: transform 0.6s cubic-bezier(0.22, 0.68, 0, 1);
}
.about-photo:hover img {
  transform: scale(1.1) !important;
  animation-play-state: paused;
}
@keyframes kenBurns {
  0% {
    transform: scale(1);
  }
  100% {
    transform: scale(1.07);
  }
}
@media (prefers-reduced-motion: reduce) {
  .about-photo img {
    animation: none;
  }
}
.about-stats {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 13px;
}
.astat {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.09);
  border-radius: 13px;
  padding: 24px 18px;
  text-align: center;
}
.astat-n {
  font-family: "Cormorant Garamond", serif;
  font-size: 2.2rem;
  color: var(--sky-light);
  line-height: 1;
}
.astat.gold .astat-n {
  color: var(--gold-lt);
}
.astat-l {
  font-size: 0.72rem;
  color: rgba(255, 255, 255, 0.42);
  margin-top: 7px;
  line-height: 1.45;
}

/* ─── TESTIMONIALS ─── */
.testi-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
}
.testi-card {
  background: var(--surface);
  border: 1px solid var(--border-soft);
  border-radius: 13px;
  padding: 24px;
  position: relative;
}
.testi-stars {
  color: var(--gold);
  font-size: 1rem;
  margin-bottom: 12px;
  letter-spacing: 2px;
}
.testi-text {
  font-size: 0.86rem;
  color: var(--muted);
  line-height: 1.7;
  margin-bottom: 14px;
  font-style: italic;
}
.testi-author {
  font-size: 0.8rem;
  font-weight: 600;
  color: var(--heading);
}
.testi-meta {
  font-size: 0.72rem;
  color: var(--muted);
  margin-top: 2px;
}
.quote-mark {
  position: absolute;
  top: 16px;
  right: 18px;
  font-family: "Cormorant Garamond", serif;
  font-size: 4rem;
  color: var(--offwhite);
  line-height: 1;
  pointer-events: none;
}

/* ─── CONTACT ─── */
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
}
.ccard-icon {
  width: 42px;
  height: 42px;
  background: var(--offwhite);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
  flex-shrink: 0;
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
.form-wrap {
  background: var(--surface);
  border: 1px solid var(--border-soft);
  border-radius: 15px;
  padding: 28px;
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
.radio-group label.radio-card {
  position: relative;
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
}
.form-fields {
  position: relative;
}
.form-fields.is-sending .fg,
.form-fields.is-sending .btn-submit {
  pointer-events: none;
  opacity: 0.45;
}
.form-success {
  text-align: center;
  padding: 26px 6px;
}
.form-success-icon {
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
.hours-card {
  background: var(--navy);
  border-radius: 15px;
  padding: 26px;
}
.hours-card h3 {
  color: #fff;
  font-size: 1.15rem;
  margin-bottom: 18px;
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
}
.open-now {
  background: var(--teal);
  color: #fff;
  font-size: 0.6rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  padding: 3px 9px;
  border-radius: 100px;
}
.hours-table {
  width: 100%;
  border-collapse: collapse;
}
.hours-table td {
  padding: 8px 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.06);
  font-size: 0.86rem;
  color: rgba(255, 255, 255, 0.72);
}
.hours-table tr:last-child td {
  border-bottom: none;
}
.hours-table td:last-child {
  text-align: right;
  color: rgba(255, 255, 255, 0.48);
}
.urgences-note {
  margin-top: 14px;
  background: rgba(200, 16, 46, 0.15);
  border: 1px solid rgba(200, 16, 46, 0.3);
  border-radius: 8px;
  padding: 11px 14px;
  font-size: 0.8rem;
  color: rgba(255, 255, 255, 0.78);
  line-height: 1.55;
}

/* ─── MAP CTA ─── */
.map-banner {
  background: linear-gradient(135deg, var(--navy), #5c0f18);
  padding: 72px 5vw;
  text-align: center;
  color: #fff;
}
.map-banner h2 {
  font-size: clamp(1.8rem, 3vw, 2.4rem);
  margin-bottom: 12px;
}
.map-banner p {
  opacity: 0.7;
  margin-bottom: 28px;
  font-size: 0.94rem;
}

@media (max-width: 980px) {
  .hero-inner,
  .about-inner,
  .contact-grid {
    grid-template-columns: 1fr;
  }
  .hero-stats {
    grid-template-columns: 1fr 1fr 1fr;
  }
}
@media (max-width: 640px) {
  .about-stats {
    grid-template-columns: 1fr 1fr;
  }
  /* Three compact tiles on one row rather than 2 + 1 orphan. */
  .hero-stats {
    gap: 8px;
  }
  .hstat {
    padding: 12px 6px;
  }
  .hstat-n {
    font-size: 1.6rem;
  }
  .hstat-l {
    font-size: 0.62rem;
    letter-spacing: 0.02em;
  }
  .svc-grid,
  .form-row,
  .radio-group {
    grid-template-columns: 1fr;
  }
}
/* ─── Lucide icons (étape 2) ─── */
.icard-icon {
  display: flex;
  justify-content: center;
  color: var(--brand-200);
}
.ccard-icon {
  color: var(--blue);
}
.strip-item svg {
  opacity: 0.9;
}
.astat-n sup {
  font-size: 0.5em;
  vertical-align: super;
}
.inline-icon {
  vertical-align: -2px;
  margin-right: 2px;
}
</style>
