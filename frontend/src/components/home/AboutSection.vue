<script setup lang="ts">
import { onBeforeUnmount, onMounted, ref } from "vue";

import facadePhoto from "@/assets/images/hero/hero-clinic-facade-street.webp";
import labPhoto from "@/assets/images/facility/facility-laboratory-room.webp";
import awardPhoto from "@/assets/images/team/team-award-founders.webp";
import teamPhoto from "@/assets/images/team/team-staff-group-large.webp";
import AmbientVideo from "@/components/common/AmbientVideo.vue";
import { useScrollScene } from "@/motion/useScrollScene";

/**
 * "Notre histoire" told in four chapters. On desktop the photo frame stays
 * pinned (CSS sticky) and cross-fades to the chapter being read; an ECG line
 * draws itself along the chapters as the visitor scrolls. On mobile, each
 * chapter simply shows its own photo. Only facts already published on the
 * site are used here.
 */
const CHAPTERS = [
  {
    label: "Notre ancrage",
    title: "Au cœur de Riviera Sideci",
    text: "Établissement privé de référence à Cocody, sur la route d'Akouédo, à proximité de Riviera 3 et du lycée Blaise-Pascal, la Clinique Médicale Saint Viateur accueille toute la population abidjanaise et au-delà.",
    img: facadePhoto,
    alt: "Façade de la Clinique Médicale Saint Viateur et son parking, route d'Akouédo",
  },
  {
    label: "Nos équipes",
    title: "Une médecine humaine",
    text: "Une équipe médicale pluridisciplinaire, qualifiée et expérimentée, et un accueil professionnel, bienveillant et accessible à tous. Les urgences et la réanimation fonctionnent 24h/24, 7j/7.",
    img: teamPhoto,
    alt: "Le personnel soignant de la clinique réuni en tenue, dans un couloir de l'établissement",
  },
  {
    label: "Notre plateau technique",
    title: "Des équipements modernes",
    text: "Laboratoire d'analyses complet, imagerie et échographie, bloc opératoire, cabinet dentaire : des équipements médicaux modernes pour poser un diagnostic précis et soigner sur place.",
    img: labPhoto,
    alt: "Laboratoire d'analyses de la clinique avec son automate et ses paillasses",
  },
  {
    label: "Une excellence reconnue",
    title: "3ᵉ Prix national d'excellence",
    text: "Lauréate du 3ᵉ Prix national d'excellence médicale en Côte d'Ivoire, la clinique a déjà accompagné plus de 79 897 patients qui lui font confiance.",
    img: awardPhoto,
    alt: "Deux médecins de la clinique en blouse présentant un trophée lors d'une remise de prix",
  },
];

const active = ref(0);
const chapterEls = ref<HTMLElement[]>([]);
const wrapRef = ref<HTMLElement | null>(null);
let io: IntersectionObserver | null = null;
let ro: ResizeObserver | null = null;

// ECG trace in real pixels: a flat line with one heartbeat at the vertical
// centre of each chapter. Rebuilt whenever the layout changes.
const ecgHeight = ref(1000);
const ecgPath = ref("M20 0 V1000");
function buildEcg() {
  const wrap = wrapRef.value;
  if (!wrap) return;
  const h = Math.max(wrap.offsetHeight, 1);
  let d = "M20 0";
  for (const el of chapterEls.value) {
    const y = el.offsetTop + el.offsetHeight / 2;
    d += ` V${(y - 30).toFixed(0)} L12 ${(y - 17).toFixed(0)} L32 ${(y - 7).toFixed(0)} L6 ${(y + 5).toFixed(0)} L26 ${(y + 15).toFixed(0)} L20 ${(y + 25).toFixed(0)}`;
  }
  ecgHeight.value = h;
  ecgPath.value = `${d} V${h}`;
}

onMounted(() => {
  // The chapter crossing the middle band of the viewport is the active one.
  io = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) active.value = Number((entry.target as HTMLElement).dataset.index);
      });
    },
    { rootMargin: "-45% 0px -45% 0px" },
  );
  chapterEls.value.forEach((el) => io?.observe(el));

  buildEcg();
  ro = new ResizeObserver(buildEcg);
  if (wrapRef.value) ro.observe(wrapRef.value);
});
onBeforeUnmount(() => {
  io?.disconnect();
  ro?.disconnect();
});

const storyRef = ref<HTMLElement | null>(null);
useScrollScene(storyRef, ({ gsap }, story) => {
  // pathLength="1" on the path: dash values stay valid even if `d` is rebuilt.
  //
  // GSAP's CSS plugin does not tween stroke-dashoffset reliably on a path
  // with pathLength (it sees no change and drops the property), so a plain
  // value is tweened and written to the style on each update.
  const ecg = story.querySelector<SVGPathElement>(".story-ecg path");
  if (!ecg) return;
  const draw = { offset: 1 };
  ecg.style.strokeDasharray = "1";
  ecg.style.strokeDashoffset = "1";
  gsap.to(draw, {
    offset: 0,
    ease: "none",
    scrollTrigger: { trigger: story, start: "top 65%", end: "bottom 70%", scrub: 0.6 },
    onUpdate: () => {
      ecg.style.strokeDashoffset = draw.offset.toFixed(4);
    },
  });
  return () => {
    ecg.style.removeProperty("stroke-dasharray");
    ecg.style.removeProperty("stroke-dashoffset");
  };
});
</script>

<template>
  <section id="about" class="section about-section" aria-labelledby="about-title">
    <!-- Optional background film (src/assets/media/histoire.*): renders nothing until provided. -->
    <AmbientVideo class="about-ambient" media="histoire" />
    <div class="section-inner about-content">
      <header class="about-head">
        <p v-reveal class="section-kicker">Notre histoire</p>
        <h2 id="about-title" v-reveal="'words'" class="section-title d1">Une clinique moderne,<br />une médecine humaine</h2>
      </header>

      <div ref="storyRef" class="story">
        <div class="story-frame" aria-hidden="true">
          <div class="story-frame-inner">
            <img
              v-for="(c, i) in CHAPTERS"
              :key="c.title"
              :src="c.img"
              alt=""
              loading="lazy"
              decoding="async"
              :class="{ active: i === active }"
            />
            <div class="story-frame-caption">
              <span class="story-frame-n">0{{ active + 1 }}</span>
              <span>{{ CHAPTERS[active].label }}</span>
            </div>
            <div class="story-progress">
              <span v-for="(c, i) in CHAPTERS" :key="c.title" :class="{ on: i <= active }"></span>
            </div>
          </div>
        </div>

        <div ref="wrapRef" class="story-chapters-wrap">
          <svg class="story-ecg" :viewBox="`0 0 40 ${ecgHeight}`" :height="ecgHeight" aria-hidden="true">
            <path
              :d="ecgPath"
              pathLength="1"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
            />
          </svg>
          <ol class="story-chapters">
            <li
              v-for="(c, i) in CHAPTERS"
              :key="c.title"
              ref="chapterEls"
              :data-index="i"
              class="chapter"
              :class="{ active: i === active }"
            >
              <figure class="chapter-figure">
                <img :src="c.img" :alt="c.alt" loading="lazy" decoding="async" />
              </figure>
              <p v-reveal class="chapter-label"><span>0{{ i + 1 }}</span> {{ c.label }}</p>
              <h3 v-reveal class="chapter-title d1">{{ c.title }}</h3>
              <p v-reveal class="chapter-text d2">{{ c.text }}</p>
            </li>
          </ol>
        </div>
      </div>

      <div class="about-stats">
        <div v-reveal class="astat"><div class="astat-n" v-count-up="{ target: 79, suffix: 'K+' }">0K+</div><div class="astat-l">Patients satisfaits</div></div>
        <div v-reveal class="astat d1"><div class="astat-n">24<span class="astat-small">/7</span></div><div class="astat-l">Urgences en permanence</div></div>
        <div v-reveal class="astat d2"><div class="astat-n" v-count-up="{ target: 10, suffix: '+' }">0+</div><div class="astat-l">Spécialités médicales</div></div>
        <div v-reveal class="astat d3"><div class="astat-n">3<sup>e</sup></div><div class="astat-l">Prix national d'excellence</div></div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.about-section {
  background:
    radial-gradient(ellipse 50% 40% at 15% 10%, rgba(224, 71, 90, 0.18), transparent 70%),
    var(--brand-700);
  color: #fff;
  position: relative;
  overflow: clip;
}
.about-ambient {
  position: absolute;
  inset: 0;
  opacity: 0.16;
  mix-blend-mode: luminosity;
  pointer-events: none;
}
.about-content {
  position: relative;
}
.about-head .section-kicker {
  color: var(--brand-200);
}
.about-head .section-title {
  color: #fff;
  font-size: clamp(2rem, 4vw, 3.2rem);
  margin-bottom: 48px;
}

/* ─── Story: sticky frame + chapters ─── */
.story {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 64px;
  align-items: start;
}
.story-frame {
  position: sticky;
  top: 120px;
}
.story-frame-inner {
  position: relative;
  aspect-ratio: 4 / 5;
  max-height: calc(100vh - 160px);
  width: 100%;
  border-radius: var(--radius-xl);
  overflow: hidden;
  box-shadow: 0 30px 80px rgba(0, 0, 0, 0.35);
  border: 1px solid rgba(255, 255, 255, 0.1);
  background: var(--brand-900);
}
.story-frame-inner img {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  opacity: 0;
  scale: 1.08;
  transition:
    opacity 0.9s var(--ease-out),
    scale 1.6s var(--ease-out);
}
.story-frame-inner img.active {
  opacity: 1;
  scale: 1;
}
.story-frame-inner::after {
  content: "";
  position: absolute;
  inset: 0;
  background: linear-gradient(to top, rgba(24, 8, 9, 0.75), transparent 45%);
  pointer-events: none;
}
.story-frame-caption {
  position: absolute;
  left: 24px;
  bottom: 22px;
  z-index: 1;
  display: flex;
  align-items: baseline;
  gap: 12px;
  font-size: 0.78rem;
  letter-spacing: 0.14em;
  text-transform: uppercase;
}
.story-frame-n {
  font-family: var(--font-serif);
  font-size: 2.4rem;
  letter-spacing: 0;
  color: var(--brand-200);
  line-height: 1;
}
.story-progress {
  position: absolute;
  right: 22px;
  bottom: 30px;
  z-index: 1;
  display: flex;
  gap: 6px;
}
.story-progress span {
  width: 22px;
  height: 3px;
  border-radius: 2px;
  background: rgba(255, 255, 255, 0.25);
  transition: background 0.5s;
}
.story-progress span.on {
  background: var(--brand-200);
}

.story-chapters-wrap {
  position: relative;
  padding-left: 56px;
}
.story-ecg {
  position: absolute;
  left: 0;
  top: 0;
  width: 40px;
  color: var(--brand-400);
  opacity: 0.85;
  overflow: visible;
}
.story-chapters {
  list-style: none;
}
.chapter {
  min-height: 62vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding: 24px 0;
  opacity: 0.4;
  transition: opacity 0.6s var(--ease-out);
}
.chapter.active {
  opacity: 1;
}
.chapter-figure {
  display: none;
}
.chapter-label {
  font-size: 0.72rem;
  font-weight: 600;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  color: var(--brand-200);
  margin-bottom: 12px;
}
.chapter-label span {
  font-family: var(--font-serif);
  font-size: 1.1rem;
  letter-spacing: 0;
  margin-right: 6px;
}
.chapter-title {
  font-size: clamp(1.7rem, 2.8vw, 2.4rem);
  color: #fff;
  line-height: 1.15;
  margin-bottom: 16px;
}
.chapter-text {
  font-size: 1rem;
  line-height: 1.85;
  color: rgba(255, 255, 255, 0.78);
  max-width: 470px;
}

/* ─── Stats ─── */
.about-stats {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 14px;
  margin-top: 72px;
}
.astat {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: var(--radius-lg);
  padding: 26px 18px;
  text-align: center;
  transition:
    background var(--dur-fast),
    border-color var(--dur-fast);
}
.astat:hover {
  background: rgba(255, 255, 255, 0.08);
  border-color: rgba(243, 170, 180, 0.3);
}
.astat-n {
  font-family: var(--font-serif);
  font-size: 2.6rem;
  color: var(--brand-200);
  line-height: 1;
}
.astat-n sup {
  font-size: 0.5em;
  vertical-align: super;
}
.astat-small {
  font-size: 1.3rem;
}
.astat-l {
  font-size: 0.74rem;
  color: rgba(255, 255, 255, 0.68);
  margin-top: 8px;
  line-height: 1.45;
}

/* ─── Tablet & mobile: linear story, one photo per chapter ─── */
@media (max-width: 980px) {
  .story {
    grid-template-columns: 1fr;
    gap: 0;
  }
  .story-frame {
    display: none;
  }
  .chapter {
    min-height: 0;
    opacity: 1;
    padding: 0 0 48px;
  }
  .chapter-figure {
    display: block;
    margin-bottom: 20px;
    border-radius: var(--radius-lg);
    overflow: hidden;
    aspect-ratio: 16 / 10;
  }
  .chapter-figure img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block;
  }
  .about-stats {
    grid-template-columns: 1fr 1fr;
    margin-top: 24px;
  }
}
@media (max-width: 640px) {
  .story-chapters-wrap {
    padding-left: 36px;
  }
  .story-ecg {
    left: -8px;
  }
}
/* Desktop keeps chapter photos for screen readers only (the frame is decorative). */
@media (min-width: 981px) {
  .chapter-figure {
    display: block;
    position: absolute;
    width: 1px;
    height: 1px;
    overflow: hidden;
    clip: rect(0, 0, 0, 0);
    white-space: nowrap;
  }
}
</style>
