/**
 * Ambient video registry.
 *
 * Videos are picked up automatically at build time from src/assets/media/:
 *
 *   <slot>.webm          desktop, AV1 or VP9 (preferred)
 *   <slot>.mp4           desktop, H.264 (fallback, Safari/old browsers)
 *   <slot>-mobile.webm   portrait/small version, ≤ 640 px wide screens
 *   <slot>-mobile.mp4
 *
 * A slot with no file simply has no video: components then show their
 * poster image (or nothing), and no request is ever made for a missing file.
 * See docs/medias-a-generer.md for the brief, prompts and encoding commands.
 */
export type VideoSlot = "hero" | "histoire" | "urgences" | "recrutement";

export interface VideoSources {
  webm?: string;
  mp4?: string;
  mobileWebm?: string;
  mobileMp4?: string;
}

const files = import.meta.glob<string>("../assets/media/*.{webm,mp4}", {
  eager: true,
  query: "?url",
  import: "default",
});

function file(name: string): string | undefined {
  return files[`../assets/media/${name}`];
}

export function videoFor(slot: VideoSlot): VideoSources | null {
  const sources: VideoSources = {
    webm: file(`${slot}.webm`),
    mp4: file(`${slot}.mp4`),
    mobileWebm: file(`${slot}-mobile.webm`),
    mobileMp4: file(`${slot}-mobile.mp4`),
  };
  return Object.values(sources).some(Boolean) ? sources : null;
}
