<script setup lang="ts">
import { ref } from "vue";

import consultation from "@/assets/images/facility/facility-consultation-room.webp";
import dental from "@/assets/images/facility/facility-dental-room.webp";
import exam from "@/assets/images/facility/facility-exam-room.webp";
import waitingArea from "@/assets/images/facility/facility-laboratory-analyzer.webp";
import laboratory from "@/assets/images/facility/facility-laboratory-room.webp";
import lobby from "@/assets/images/facility/facility-lobby-staircase.webp";
import reception from "@/assets/images/facility/facility-reception-desk.webp";
import ultrasound from "@/assets/images/facility/facility-ultrasound-room.webp";
import analyzer from "@/assets/images/facility/facility-waiting-room.webp";
import { HEADER_OFFSET } from "@/motion/tokens";
import { useScrollScene } from "@/motion/useScrollScene";

// Captions describe what each photo actually shows (several source file
// names don't match their content, e.g. "waiting-room" is a lab analyzer).
const PHOTOS = [
  { src: reception, title: "L'accueil", alt: "Comptoir d'accueil vitré de la clinique avec deux membres du personnel en blouse blanche" },
  { src: lobby, title: "Le hall d'attente", alt: "Hall d'attente lumineux avec rangées de sièges et escalier vers l'étage" },
  { src: consultation, title: "Salle de consultation", alt: "Salle de consultation avec table d'examen et chariot de soins" },
  { src: ultrasound, title: "Échographie", alt: "Salle d'échographie avec son échographe et sa table d'examen" },
  { src: laboratory, title: "Le laboratoire", alt: "Laboratoire d'analyses avec automate et paillasses" },
  { src: analyzer, title: "Analyses biologiques", alt: "Automate d'analyses sanguines et tubes de prélèvement au laboratoire" },
  { src: dental, title: "Cabinet dentaire", alt: "Cabinet dentaire équipé d'un fauteuil et de son unité de soins" },
  { src: exam, title: "Salle d'examen", alt: "Salle d'examen avec table recouverte d'un drap vert" },
  { src: waitingArea, title: "Espaces d'attente", alt: "Espace d'attente avec sièges alignés près du comptoir d'accueil" },
];

const sectionRef = ref<HTMLElement | null>(null);

useScrollScene(sectionRef, ({ gsap }, section) => {
  const mm = gsap.matchMedia();
  // Desktop: the section pins and the photo strip travels horizontally with
  // the vertical scroll. Below 981px the native swipeable strip is kept.
  mm.add("(min-width: 981px)", () => {
    const track = section.querySelector<HTMLElement>(".gallery-track");
    const viewport = section.querySelector<HTMLElement>(".gallery-viewport");
    if (!track || !viewport) return;
    const distance = () => Math.max(track.scrollWidth - viewport.clientWidth, 0);
    gsap.to(track, {
      x: () => -distance(),
      ease: "none",
      scrollTrigger: {
        trigger: section,
        // Pin just below the fixed nav + jobs ticker.
        start: `top ${HEADER_OFFSET}px`,
        end: () => `+=${distance()}`,
        pin: true,
        scrub: 0.8,
        invalidateOnRefresh: true,
      },
    });
    // Each photo slowly settles as it travels (subtle depth).
    gsap.utils.toArray<HTMLElement>(".gallery-card img", section).forEach((img) => {
      gsap.fromTo(img, { scale: 1.15 }, { scale: 1, ease: "none", scrollTrigger: { trigger: section, start: `top ${HEADER_OFFSET}px`, end: () => `+=${distance()}`, scrub: true } });
    });
    viewport.classList.add("is-pinned");
    return () => viewport.classList.remove("is-pinned");
  });
  return () => mm.revert();
});
</script>

<template>
  <section ref="sectionRef" id="galerie" class="gallery" aria-labelledby="gallery-title">
    <div class="gallery-head section-inner">
      <div>
        <p v-reveal class="section-kicker">Visite de l'établissement</p>
        <h2 id="gallery-title" v-reveal="'words'" class="section-title d1">Un cadre pensé pour vos soins</h2>
      </div>
      <p v-reveal class="gallery-lead d2">
        Accueil, consultations, imagerie, laboratoire, soins dentaires : découvrez les espaces où nos équipes vous
        reçoivent chaque jour.
      </p>
    </div>

    <div class="gallery-viewport" tabindex="0" role="region" aria-label="Photos de l'établissement (faire défiler horizontalement)">
      <ul class="gallery-track">
        <li v-for="(p, i) in PHOTOS" :key="p.title" class="gallery-card">
          <figure>
            <div class="gallery-img">
              <img :src="p.src" :alt="p.alt" width="1024" height="768" loading="lazy" decoding="async" />
            </div>
            <figcaption>
              <span class="gallery-n">{{ String(i + 1).padStart(2, "0") }}</span>
              {{ p.title }}
            </figcaption>
          </figure>
        </li>
      </ul>
    </div>
  </section>
</template>

<style scoped>
.gallery {
  background: var(--bg);
  padding: var(--space-8) 0;
  overflow: hidden;
}
.gallery-head {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 32px;
  padding: 0 5vw;
  margin-bottom: 40px;
}
.gallery-head .section-title {
  margin-bottom: 0;
}
.gallery-lead {
  max-width: 380px;
  color: var(--muted);
  font-size: 0.92rem;
  line-height: 1.75;
}
.gallery-viewport {
  overflow-x: auto;
  scroll-snap-type: x mandatory;
  scrollbar-width: none;
  padding: 0 5vw 8px;
  scroll-padding: 0 5vw;
}
.gallery-viewport::-webkit-scrollbar {
  display: none;
}
.gallery-viewport:focus-visible {
  outline-offset: -4px;
}
/* While GSAP pins the section, it owns the horizontal movement. */
.gallery-viewport.is-pinned {
  overflow: visible;
  scroll-snap-type: none;
}
.gallery-track {
  display: flex;
  gap: 22px;
  list-style: none;
  width: max-content;
  will-change: transform;
}
.gallery-card {
  scroll-snap-align: start;
  /* Bounded by the viewport height too, so the pinned section always fits
     on a 1366×768 laptop under the fixed header. */
  width: clamp(260px, min(34vw, 48vh), 480px);
  flex-shrink: 0;
}
.gallery-card:nth-child(even) {
  margin-top: 40px;
}
@media (max-height: 760px) {
  .gallery-card:nth-child(even) {
    margin-top: 0;
  }
}
.gallery-img {
  border-radius: var(--radius-xl);
  overflow: hidden;
  aspect-ratio: 4 / 3;
  background: var(--bg-alt);
  box-shadow: var(--shadow-md);
}
.gallery-img img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
  transition: scale 0.8s var(--ease-out);
}
.gallery-card:hover .gallery-img img {
  scale: 1.05;
}
figcaption {
  display: flex;
  align-items: baseline;
  gap: 10px;
  margin-top: 14px;
  font-size: 0.95rem;
  font-weight: 600;
  color: var(--heading);
}
.gallery-n {
  font-family: "Cormorant Garamond", serif;
  font-size: 1.4rem;
  color: var(--brand-400);
}

@media (max-width: 980px) {
  .gallery-head {
    flex-direction: column;
    align-items: flex-start;
    gap: 14px;
  }
  .gallery-card {
    width: min(78vw, 360px);
  }
  .gallery-card:nth-child(even) {
    margin-top: 0;
  }
}
@media (max-width: 640px) {
  .gallery {
    padding: var(--space-8) 0;
  }
  .gallery-head,
  .gallery-viewport {
    padding-left: 16px;
    padding-right: 16px;
  }
}
</style>
