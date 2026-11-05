<script setup lang="ts">
import { Menu, Moon, Phone, Settings, Sun, X } from "@lucide/vue";
import { computed, onBeforeUnmount, onMounted, ref, watch } from "vue";
import { useRoute, useRouter } from "vue-router";

import BrandMark from "@/components/brand/BrandMark.vue";
import { useAdminAccess } from "@/composables/useAdminAccess";
import { useTheme } from "@/composables/useTheme";
import { lockScroll } from "@/motion/useLenis";

const LINKS = [
  { to: "/specialites", label: "Spécialités" },
  { to: "/#about", label: "La clinique" },
  { to: "/promotions", label: "Offres" },
  { to: "/blog", label: "Actualités" },
  { to: "/#temoignages", label: "Avis patients" },
  { to: "/#contact", label: "Contact" },
  { to: "/nous-rejoindre", label: "Nous rejoindre" },
];

const stuck = ref(false);
const menuOpen = ref(false);
const menuButton = ref<HTMLButtonElement | null>(null);
const route = useRoute();
const router = useRouter();
const { isDark, toggle } = useTheme();
const { unlocked: adminUnlocked } = useAdminAccess();

// Transparent only over the home page's dark hero; every other page starts on
// a light surface where white nav text would be invisible.
const solid = computed(() => stuck.value || route.name !== "home");

const themeLabel = computed(() => (isDark(false) ? "Passer en mode clair" : "Passer en mode sombre"));

function onScroll() {
  stuck.value = window.scrollY > 60;
}

function closeMenu(returnFocus = false) {
  if (!menuOpen.value) return;
  menuOpen.value = false;
  if (returnFocus) menuButton.value?.focus();
}

function onKeydown(e: KeyboardEvent) {
  if (e.key === "Escape") closeMenu(true);
}

// Lock page scroll behind the open mobile menu.
watch(menuOpen, (open) => {
  document.body.style.overflow = open ? "hidden" : "";
  lockScroll(open);
});

// Any navigation (including same-page anchors) closes the menu.
watch(
  () => route.fullPath,
  () => closeMenu(),
);

onMounted(() => {
  window.addEventListener("scroll", onScroll, { passive: true });
  window.addEventListener("keydown", onKeydown);
  onScroll();
});
onBeforeUnmount(() => {
  window.removeEventListener("scroll", onScroll);
  window.removeEventListener("keydown", onKeydown);
  document.body.style.overflow = "";
  lockScroll(false);
});

function goAdmin() {
  closeMenu();
  router.push({ name: "login" });
}
</script>

<template>
  <nav id="nav" :class="{ stuck: solid, 'menu-open': menuOpen }" aria-label="Navigation principale">
    <RouterLink to="/" class="nav-logo" aria-label="Clinique Médicale Saint Viateur — Accueil">
      <BrandMark :size="38" />
      <div class="nav-wordmark">
        Clinique Médicale Saint Viateur<span>Cocody · Abidjan · C.I.</span>
      </div>
    </RouterLink>
    <ul class="nav-links">
      <li v-for="link in LINKS" :key="link.to"><RouterLink :to="link.to">{{ link.label }}</RouterLink></li>
    </ul>
    <div class="nav-actions">
      <button
        type="button"
        class="theme-toggle btn-nav-theme"
        :aria-label="themeLabel"
        :title="themeLabel"
        @click="toggle(false)"
      >
        <Sun v-if="isDark(false)" :size="16" aria-hidden="true" />
        <Moon v-else :size="16" aria-hidden="true" />
      </button>
      <button v-if="adminUnlocked" type="button" class="btn-nav-admin" @click="goAdmin">
        <Settings :size="13" aria-hidden="true" /> Admin
      </button>
      <a href="tel:+2252722590417" class="btn-nav-cta" aria-label="Urgences : appeler le 27 22 59 04 17">
        <Phone :size="15" aria-hidden="true" /><span class="cta-label">Urgences</span>
      </a>
      <button
        ref="menuButton"
        type="button"
        class="btn-nav-burger"
        :aria-expanded="menuOpen"
        aria-controls="nav-mobile-panel"
        :aria-label="menuOpen ? 'Fermer le menu' : 'Ouvrir le menu'"
        @click="menuOpen = !menuOpen"
      >
        <X v-if="menuOpen" :size="22" aria-hidden="true" />
        <Menu v-else :size="22" aria-hidden="true" />
      </button>
    </div>
  </nav>

  <Transition name="nav-backdrop">
    <div v-if="menuOpen" class="nav-backdrop" aria-hidden="true" @click="closeMenu()"></div>
  </Transition>
  <Transition name="nav-panel">
    <div v-if="menuOpen" id="nav-mobile-panel" class="nav-mobile-panel" data-lenis-prevent>
      <ul>
        <li v-for="(link, i) in LINKS" :key="link.to" :style="{ '--i': i }">
          <RouterLink :to="link.to" @click="closeMenu()">{{ link.label }}</RouterLink>
        </li>
      </ul>
      <a href="tel:+2252722590417" class="nav-mobile-call">
        <Phone :size="18" aria-hidden="true" />
        <span><strong>Urgences 24h/24</strong>27 22 59 04 17</span>
      </a>
    </div>
  </Transition>
</template>

<style scoped>
#nav {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 500;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 5vw;
  height: 68px;
  background: transparent;
  transition:
    background 0.4s,
    box-shadow 0.4s,
    backdrop-filter 0.4s;
}
#nav.stuck {
  background: rgba(24, 8, 9, 0.96);
  backdrop-filter: blur(14px);
  box-shadow: 0 1px 28px rgba(0, 0, 0, 0.35);
}
.nav-logo {
  display: flex;
  align-items: center;
  gap: 11px;
  text-decoration: none;
}
.nav-wordmark {
  color: #fff;
  font-family: "Cormorant Garamond", serif;
  font-size: 1.05rem;
  line-height: 1.2;
}
.nav-wordmark span {
  display: block;
  font-family: "DM Sans", sans-serif;
  font-size: 0.62rem;
  letter-spacing: 0.15em;
  text-transform: uppercase;
  color: var(--sky-light);
  font-weight: 400;
}
.nav-links {
  display: flex;
  gap: 30px;
  list-style: none;
}
.nav-links a {
  color: rgba(255, 255, 255, 0.78);
  text-decoration: none;
  font-size: 0.85rem;
  font-weight: 500;
  transition: color 0.2s;
}
.nav-links a:hover {
  color: #fff;
}
.nav-actions {
  display: flex;
  gap: 10px;
  align-items: center;
}
.btn-nav-theme {
  background: transparent;
  border: 1px solid rgba(255, 255, 255, 0.18);
  border-radius: 4px;
  width: 32px;
  height: 32px;
  font-size: 0.9rem;
  line-height: 1;
}
.btn-nav-theme:hover {
  border-color: rgba(255, 255, 255, 0.5);
  background: rgba(255, 255, 255, 0.06);
}
.btn-nav-admin {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  background: transparent;
  border: 1px solid rgba(255, 255, 255, 0.18);
  color: rgba(255, 255, 255, 0.5);
  padding: 7px 13px;
  border-radius: 4px;
  font-size: 0.72rem;
  cursor: pointer;
  transition: all 0.2s;
}
.btn-nav-admin:hover {
  border-color: rgba(255, 255, 255, 0.5);
  color: #fff;
}
.btn-nav-cta {
  background: var(--gold);
  color: #fff;
  padding: 9px 22px;
  border-radius: 4px;
  text-decoration: none;
  font-size: 0.83rem;
  font-weight: 600;
  letter-spacing: 0.03em;
  transition:
    background 0.2s,
    transform 0.15s,
    box-shadow 0.2s;
}
.btn-nav-cta:hover {
  background: var(--gold-lt);
  transform: translateY(-1px);
  box-shadow: 0 5px 18px rgba(200, 16, 46, 0.4);
}
.btn-nav-theme {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  color: #fff;
}
.btn-nav-cta {
  display: inline-flex;
  align-items: center;
  gap: 7px;
}

/* ─── Mobile menu ─── */
.btn-nav-burger {
  display: none;
  align-items: center;
  justify-content: center;
  width: 42px;
  height: 42px;
  background: transparent;
  border: 1px solid rgba(255, 255, 255, 0.22);
  border-radius: 6px;
  color: #fff;
  cursor: pointer;
}
.btn-nav-burger:hover {
  background: rgba(255, 255, 255, 0.08);
}
#nav.menu-open {
  background: rgba(24, 8, 9, 0.98);
}
.nav-backdrop {
  position: fixed;
  inset: 0;
  z-index: 498;
  background: rgba(10, 3, 4, 0.55);
  backdrop-filter: blur(3px);
}
.nav-mobile-panel {
  position: fixed;
  top: 68px;
  right: 0;
  bottom: 0;
  z-index: 499;
  width: min(360px, 100%);
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  gap: 24px;
  padding: 28px 24px calc(24px + env(safe-area-inset-bottom));
  background: #1d0a0c;
  border-left: 1px solid rgba(255, 255, 255, 0.08);
  overflow-y: auto;
}
.nav-mobile-panel ul {
  list-style: none;
  display: flex;
  flex-direction: column;
}
.nav-mobile-panel li a {
  display: block;
  padding: 14px 4px;
  color: rgba(255, 255, 255, 0.86);
  text-decoration: none;
  font-family: "Cormorant Garamond", serif;
  font-size: 1.45rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.07);
  transition: color 0.2s, padding-left 0.2s;
}
/* Vue Router ignores the #hash when matching, so "/#about" would count as
   active on the home page: only highlight real page links. */
.nav-mobile-panel li a:hover,
.nav-mobile-panel li a.router-link-exact-active:not([href*="#"]) {
  color: #fff;
  padding-left: 10px;
}
.nav-mobile-call {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 16px 18px;
  border-radius: 10px;
  background: var(--gold);
  color: #fff;
  text-decoration: none;
}
.nav-mobile-call span {
  display: flex;
  flex-direction: column;
  font-size: 1.1rem;
  font-weight: 600;
  letter-spacing: 0.02em;
}
.nav-mobile-call strong {
  font-size: 0.68rem;
  font-weight: 600;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  opacity: 0.85;
}

/* Transitions */
.nav-backdrop-enter-active,
.nav-backdrop-leave-active {
  transition: opacity 0.3s ease;
}
.nav-backdrop-enter-from,
.nav-backdrop-leave-to {
  opacity: 0;
}
.nav-panel-enter-active,
.nav-panel-leave-active {
  transition: transform 0.38s cubic-bezier(0.22, 1, 0.36, 1);
}
.nav-panel-enter-from,
.nav-panel-leave-to {
  transform: translateX(100%);
}
.nav-panel-enter-active li {
  animation: nav-item-in 0.45s cubic-bezier(0.22, 1, 0.36, 1) both;
  animation-delay: calc(0.08s + var(--i) * 0.04s);
}
@keyframes nav-item-in {
  from {
    opacity: 0;
    transform: translateX(24px);
  }
}
@media (prefers-reduced-motion: reduce) {
  .nav-panel-enter-active,
  .nav-panel-leave-active,
  .nav-backdrop-enter-active,
  .nav-backdrop-leave-active {
    transition: none;
  }
  .nav-panel-enter-active li {
    animation: none;
  }
}

@media (max-width: 980px) {
  .nav-links {
    display: none;
  }
  .btn-nav-burger {
    display: inline-flex;
  }
}
@media (max-width: 560px) {
  #nav {
    padding: 0 16px;
  }
  .nav-wordmark {
    font-size: 0.92rem;
  }
  .nav-wordmark span {
    display: none;
  }
  .btn-nav-cta {
    padding: 9px 12px;
  }
  .cta-label {
    display: none;
  }
}
@media (min-width: 981px) {
  .nav-mobile-panel,
  .nav-backdrop {
    display: none;
  }
}
</style>
