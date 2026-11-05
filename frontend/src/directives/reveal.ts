import type { Directive } from "vue";

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

/** v-reveal: fades/slides an element in once it scrolls into view (mirrors the original .rv scroll-reveal). */
export const vReveal: Directive<HTMLElement> = {
  mounted(el) {
    el.classList.add("rv");
    observer?.observe(el);
  },
  unmounted(el) {
    observer?.unobserve(el);
  },
};
