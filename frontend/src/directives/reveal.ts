import type { Directive } from "vue";

/**
 * v-reveal: animates an element in once it scrolls into view.
 *
 * Pure CSS + IntersectionObserver (no GSAP), so it costs nothing to use on
 * every page. Styles live in base.css (.rv, .rv-*).
 *
 *   v-reveal                     → fade + rise (default, unchanged behaviour)
 *   v-reveal="'fade'"            → fade only
 *   v-reveal="'left' | 'right'"  → slide in from a side
 *   v-reveal="'scale'"           → fade + slight zoom
 *   v-reveal="'mask'"            → wipe in from the top (images, cards)
 *   v-reveal="'words'"           → words rise one by one from behind a mask
 *   v-reveal="{ type: 'words', delay: 200 }"
 *
 * 'words' rewrites the element's text nodes into spans: only use it on
 * static text (no {{ interpolation }}), e.g. section titles.
 * The legacy .d1–.d4 delay classes keep working with every type.
 */
export type RevealType = "up" | "fade" | "left" | "right" | "scale" | "mask" | "words";
export type RevealValue = RevealType | { type?: RevealType; delay?: number } | undefined;

function normalize(value: RevealValue): { type: RevealType; delay?: number } {
  if (!value) return { type: "up" };
  if (typeof value === "string") return { type: value };
  return { type: value.type ?? "up", delay: value.delay };
}

function wrapWords(root: Element): void {
  let index = 0;
  const walk = (node: Node) => {
    // Snapshot: we mutate childNodes while iterating.
    for (const child of Array.from(node.childNodes)) {
      if (child.nodeType === Node.TEXT_NODE) {
        const parts = (child.textContent ?? "").split(/(\s+)/);
        if (parts.every((p) => !p.trim())) continue;
        const frag = document.createDocumentFragment();
        for (const part of parts) {
          if (!part) continue;
          if (!part.trim()) {
            frag.appendChild(document.createTextNode(part));
            continue;
          }
          const outer = document.createElement("span");
          outer.className = "rv-w";
          const inner = document.createElement("span");
          inner.className = "rv-wi";
          inner.style.setProperty("--i", String(index++));
          inner.textContent = part;
          outer.appendChild(inner);
          frag.appendChild(outer);
        }
        child.replaceWith(frag);
      } else if (child.nodeType === Node.ELEMENT_NODE && (child as Element).tagName !== "BR") {
        walk(child);
      }
    }
  };
  walk(root);
}

function handleIntersect(entries: IntersectionObserverEntry[], obs: IntersectionObserver) {
  entries.forEach((entry) => {
    if (entry.isIntersecting) {
      entry.target.classList.add("vis");
      obs.unobserve(entry.target);
    }
  });
}

const observer =
  typeof IntersectionObserver !== "undefined"
    ? new IntersectionObserver(handleIntersect, { threshold: 0.12, rootMargin: "0px 0px -35px 0px" })
    : null;

export const vReveal: Directive<HTMLElement, RevealValue> = {
  mounted(el, binding) {
    const { type, delay } = normalize(binding.value);
    el.classList.add("rv");
    if (type !== "up") el.classList.add(`rv-${type}`);
    if (delay) el.style.setProperty("--rv-delay", `${delay}ms`);
    if (type === "words") wrapWords(el);
    if (observer) observer.observe(el);
    else el.classList.add("vis");
  },
  unmounted(el) {
    observer?.unobserve(el);
  },
};
