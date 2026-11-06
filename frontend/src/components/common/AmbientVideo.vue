<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref, watch } from "vue";

import { type VideoSlot, type VideoSources, videoFor } from "@/media/videos";
import { reducedMotion } from "@/motion/motionPreferences";

/**
 * Decorative background video with a poster image.
 *
 * - The poster <img> is always rendered first: it is the fallback, the LCP
 *   candidate and what reduced-motion / data-saver visitors see.
 * - The <video> is only added when a file exists for the slot (see
 *   media/videos.ts), motion is allowed and the visitor is not saving data.
 * - It loads nothing until it scrolls into view (preload="none"), plays only
 *   while visible and the tab is active, fades in once frames are ready, and
 *   silently falls back to the poster on any error.
 * - It is muted, looped, has no controls and is hidden from assistive tech:
 *   it must never carry information that isn't also in the page text.
 */
const props = withDefaults(
  defineProps<{
    /** Which video slot to play (files resolved by media/videos.ts)… */
    media?: VideoSlot;
    /** …or a direct URL (e.g. a specialty video uploaded from the admin). */
    src?: string | null;
    poster?: string;
    posterSrcset?: string;
    posterSizes?: string;
    posterAlt?: string;
    posterWidth?: number;
    posterHeight?: number;
    /** "high" for an above-the-fold poster (hero). */
    posterPriority?: "high" | "low" | "auto";
  }>(),
  {
    media: undefined,
    src: undefined,
    poster: undefined,
    posterSrcset: undefined,
    posterSizes: undefined,
    posterAlt: "",
    posterWidth: undefined,
    posterHeight: undefined,
    posterPriority: "auto",
  },
);

function sourcesFromUrl(url: string): VideoSources {
  return url.toLowerCase().endsWith(".webm") ? { webm: url } : { mp4: url };
}
const sources = props.src ? sourcesFromUrl(props.src) : props.media ? videoFor(props.media) : null;

function savingData(): boolean {
  const connection = (navigator as Navigator & { connection?: { saveData?: boolean } }).connection;
  return !!connection?.saveData || !!window.matchMedia?.("(prefers-reduced-data: reduce)").matches;
}

const allowed = computed(() => !!sources && !reducedMotion.value && !savingData());
const failed = ref(false);
const ready = ref(false);
const showVideo = computed(() => allowed.value && !failed.value);

const root = ref<HTMLElement | null>(null);
const videoEl = ref<HTMLVideoElement | null>(null);
let visible = false;
let io: IntersectionObserver | null = null;

function sync() {
  const video = videoEl.value;
  if (!video) return;
  if (visible && !document.hidden && showVideo.value) {
    video.play().catch(() => {
      /* autoplay refused (rare for muted video): the poster stays */
    });
  } else {
    video.pause();
  }
}

onMounted(() => {
  if (!root.value) return;
  io = new IntersectionObserver(
    ([entry]) => {
      visible = entry.isIntersecting;
      sync();
    },
    { threshold: 0.15 },
  );
  io.observe(root.value);
  document.addEventListener("visibilitychange", sync);
});

onBeforeUnmount(() => {
  io?.disconnect();
  document.removeEventListener("visibilitychange", sync);
  videoEl.value?.pause();
});

// Turning reduced motion on mid-visit stops the video at once.
watch(showVideo, () => requestAnimationFrame(sync));

// Browsers try <source> elements in order; only the last one failing means
// the video can't play at all.
function onSourceError(e: Event) {
  if (e.target === videoEl.value?.querySelector("source:last-of-type")) failed.value = true;
}
function onError() {
  failed.value = true;
}
</script>

<template>
  <div v-if="poster || showVideo" ref="root" class="ambient" :class="{ 'is-playing': ready && showVideo }">
    <img
      v-if="poster"
      class="ambient-poster"
      :src="poster"
      :srcset="posterSrcset"
      :sizes="posterSizes"
      :alt="posterAlt"
      :width="posterWidth"
      :height="posterHeight"
      :fetchpriority="posterPriority"
      :loading="posterPriority === 'high' ? 'eager' : 'lazy'"
      decoding="async"
    />
    <video
      v-if="showVideo && sources"
      ref="videoEl"
      class="ambient-video"
      muted
      loop
      playsinline
      preload="none"
      disablepictureinpicture
      disableremoteplayback
      aria-hidden="true"
      tabindex="-1"
      @playing="ready = true"
      @error="onError"
    >
      <!-- Portrait/light versions first for small screens, then desktop. -->
      <source v-if="sources.mobileWebm" :src="sources.mobileWebm" type="video/webm" media="(max-width: 640px)" @error="onSourceError" />
      <source v-if="sources.mobileMp4" :src="sources.mobileMp4" type="video/mp4" media="(max-width: 640px)" @error="onSourceError" />
      <source v-if="sources.webm" :src="sources.webm" type="video/webm" @error="onSourceError" />
      <source v-if="sources.mp4" :src="sources.mp4" type="video/mp4" @error="onSourceError" />
    </video>
  </div>
</template>

<style scoped>
.ambient {
  position: relative;
  overflow: hidden;
}
.ambient-poster,
.ambient-video {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: inherit;
  display: block;
}
.ambient-video {
  opacity: 0;
  transition: opacity 1.2s var(--ease-out);
}
.ambient.is-playing .ambient-video {
  opacity: 1;
}
</style>
