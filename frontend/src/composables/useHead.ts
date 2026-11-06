/**
 * Hand-rolled per-page SEO composable (no external dependency). Sets document.title,
 * meta description/OG tags, canonical link, and JSON-LD structured data.
 *
 * IMPORTANT LIMITATION: this is a client-rendered SPA with no SSR/prerendering.
 * These tags update correctly for crawlers that execute JS (Googlebot does), but
 * simple crawlers that only fetch raw HTML — Facebook/WhatsApp/Twitter link-preview
 * bots — will only ever see the static tags in index.html, never these per-page
 * ones. Social share previews for individual pages will show the generic homepage
 * title/description until/unless server-side rendering is added later.
 */

import { OPENING_HOURS } from "@/composables/useClinicHours";

const DEFAULT_TITLE = "Clinique Médicale Saint Viateur – Riviera Sideci, Cocody, Abidjan";
const DEFAULT_DESCRIPTION =
  "Clinique Médicale Saint Viateur – Établissement privé de santé à Cocody, Abidjan. Soins 24h/24, urgences, gynécologie, chirurgie, pédiatrie et plus.";

/** Public address of the site (frontend/.env VITE_SITE_URL), without trailing slash. */
export const SITE_URL: string = (import.meta.env.VITE_SITE_URL || window.location.origin).replace(/\/+$/, "");
const DEFAULT_OG_IMAGE = `${SITE_URL}/og-image.jpg`;

/** Absolute URL for a path or an already-absolute URL. */
function absolute(url: string): string {
  return /^https?:\/\//.test(url) ? url : `${SITE_URL}${url.startsWith("/") ? "" : "/"}${url}`;
}

function upsertMeta(attr: "name" | "property", key: string, content: string) {
  let el = document.head.querySelector<HTMLMetaElement>(`meta[${attr}="${key}"]`);
  if (!el) {
    el = document.createElement("meta");
    el.setAttribute(attr, key);
    document.head.appendChild(el);
  }
  el.setAttribute("content", content);
}

export function setTitle(title: string) {
  document.title = title;
}

export function setMeta(name: string, content: string) {
  upsertMeta("name", name, content);
}

export function setOgMeta(property: string, content: string) {
  upsertMeta("property", property, content);
}

/** Canonical = public site address + path only (no query string, no #hash). */
export function setCanonical(url: string) {
  const path = new URL(url, window.location.origin).pathname;
  const canonical = `${SITE_URL}${path}`;
  let el = document.head.querySelector<HTMLLinkElement>('link[rel="canonical"]');
  if (!el) {
    el = document.createElement("link");
    el.setAttribute("rel", "canonical");
    document.head.appendChild(el);
  }
  el.setAttribute("href", canonical);
  upsertMeta("property", "og:url", canonical);
}

export function setJsonLd(data: object) {
  let el = document.getElementById("page-jsonld") as HTMLScriptElement | null;
  if (!el) {
    el = document.createElement("script");
    el.id = "page-jsonld";
    el.type = "application/ld+json";
    document.head.appendChild(el);
  }
  el.textContent = JSON.stringify(data);
}

export function clearJsonLd() {
  document.getElementById("page-jsonld")?.remove();
}

export interface SeoOptions {
  title: string;
  description?: string;
  ogImage?: string;
  canonical?: string;
  jsonLd?: object;
}

/** Apply all SEO tags for the current page. Call again on route/slug change. */
export function applySeo(options: SeoOptions) {
  const description = options.description || DEFAULT_DESCRIPTION;
  const image = options.ogImage ? absolute(options.ogImage) : DEFAULT_OG_IMAGE;
  setTitle(options.title);
  setMeta("description", description);
  setOgMeta("og:title", options.title);
  setOgMeta("og:type", "website");
  setOgMeta("og:description", description);
  // Always (re)set: otherwise the previous page's image would linger.
  setOgMeta("og:image", image);
  setMeta("twitter:title", options.title);
  setMeta("twitter:description", description);
  setMeta("twitter:image", image);
  setCanonical(options.canonical || window.location.pathname);
  setMeta("robots", "index, follow");
  if (options.jsonLd) setJsonLd(options.jsonLd);
  else clearJsonLd();
}

/** Restore the generic homepage title/description (e.g. on 404 or list pages). */
export function resetSeo() {
  applySeo({ title: DEFAULT_TITLE, description: DEFAULT_DESCRIPTION });
}

const SCHEMA_DAYS = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];

/**
 * schema.org description of the clinic for the home page. Only facts already
 * published on the site are used (no invented geo coordinates, ratings,
 * founding date or specialty codes). Opening hours come from the same source
 * as the hours shown on the page (useClinicHours).
 */
export function clinicJsonLd(): object {
  // OPENING_HOURS is indexed like SCHEMA_DAYS (0 = Sunday).
  const consultationHours = OPENING_HOURS.flatMap((d, i) =>
    d.open && d.close
      ? [{ "@type": "OpeningHoursSpecification", dayOfWeek: `https://schema.org/${SCHEMA_DAYS[i]}`, opens: d.open, closes: d.close }]
      : [],
  );
  return {
    "@context": "https://schema.org",
    "@type": "MedicalClinic",
    "@id": `${SITE_URL}/#clinique`,
    name: "Clinique Médicale Saint Viateur",
    url: `${SITE_URL}/`,
    image: DEFAULT_OG_IMAGE,
    logo: `${SITE_URL}/icon-192.png`,
    description: DEFAULT_DESCRIPTION,
    telephone: "+225 27 22 59 04 17",
    email: "cliniquestviateur@aviso.ci",
    address: {
      "@type": "PostalAddress",
      streetAddress: "Route Akouédo, Riviera Sideci",
      addressLocality: "Cocody, Abidjan",
      postOfficeBoxNumber: "22 BP 289 Abidjan 22",
      addressCountry: "CI",
    },
    openingHoursSpecification: consultationHours,
    sameAs: ["https://www.facebook.com/CliniqueMedicaleSaintViateur/"],
    award: "3e Prix national d'excellence médicale (Côte d'Ivoire)",
    department: {
      "@type": "EmergencyService",
      name: "Urgences et réanimation",
      telephone: "+225 27 22 59 04 17",
      openingHoursSpecification: {
        "@type": "OpeningHoursSpecification",
        dayOfWeek: SCHEMA_DAYS.map((d) => `https://schema.org/${d}`),
        opens: "00:00",
        closes: "23:59",
      },
    },
  };
}
