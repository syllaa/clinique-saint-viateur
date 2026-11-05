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

const DEFAULT_TITLE = "Clinique Médicale Saint Viateur – Riviera Sideci, Cocody, Abidjan";
const DEFAULT_DESCRIPTION =
  "Clinique Médicale Saint Viateur – Établissement privé de santé à Cocody, Abidjan. Soins 24h/24, urgences, gynécologie, chirurgie, pédiatrie et plus.";

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

export function setCanonical(url: string) {
  let el = document.head.querySelector<HTMLLinkElement>('link[rel="canonical"]');
  if (!el) {
    el = document.createElement("link");
    el.setAttribute("rel", "canonical");
    document.head.appendChild(el);
  }
  el.setAttribute("href", url);
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
  setTitle(options.title);
  setOgMeta("og:title", options.title);
  setOgMeta("og:type", "website");
  if (options.description) {
    setMeta("description", options.description);
    setOgMeta("og:description", options.description);
  }
  if (options.ogImage) setOgMeta("og:image", options.ogImage);
  if (options.canonical) {
    setCanonical(options.canonical);
    setOgMeta("og:url", options.canonical);
  }
  if (options.jsonLd) setJsonLd(options.jsonLd);
  else clearJsonLd();
}

/** Restore the generic homepage title/description (e.g. on 404 or list pages). */
export function resetSeo() {
  setTitle(DEFAULT_TITLE);
  setMeta("description", DEFAULT_DESCRIPTION);
  clearJsonLd();
}
