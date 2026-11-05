<script setup lang="ts">
import { onBeforeUnmount, onMounted, ref } from "vue";
import { useRouter } from "vue-router";

import { useAdminAccess } from "@/composables/useAdminAccess";
import { useTheme } from "@/composables/useTheme";

const stuck = ref(false);
const router = useRouter();
const { isDark, toggle } = useTheme();
const { unlocked: adminUnlocked } = useAdminAccess();

function onScroll() {
  stuck.value = window.scrollY > 60;
}

onMounted(() => window.addEventListener("scroll", onScroll, { passive: true }));
onBeforeUnmount(() => window.removeEventListener("scroll", onScroll));

function goAdmin() {
  router.push({ name: "login" });
}
</script>

<template>
  <nav id="nav" :class="{ stuck }">
    <a href="#" class="nav-logo">
      <div class="nav-emblem">✚</div>
      <div class="nav-wordmark">
        Clinique Médicale Saint Viateur<span>Cocody · Abidjan · C.I.</span>
      </div>
    </a>
    <ul class="nav-links">
      <li><RouterLink to="/specialites">Spécialités</RouterLink></li>
      <li><RouterLink to="/#about">La clinique</RouterLink></li>
      <li><RouterLink to="/promotions">Offres</RouterLink></li>
      <li><RouterLink to="/blog">Actualités</RouterLink></li>
      <li><RouterLink to="/#temoignages">Avis patients</RouterLink></li>
      <li><RouterLink to="/#contact">Contact</RouterLink></li>
      <li><RouterLink to="/nous-rejoindre">Nous rejoindre</RouterLink></li>
    </ul>
    <div class="nav-actions">
      <button
        class="theme-toggle btn-nav-theme"
        :title="isDark(false) ? 'Passer en mode clair' : 'Passer en mode sombre'"
        @click="toggle(false)"
      >
        {{ isDark(false) ? "☀️" : "🌙" }}
      </button>
      <button v-if="adminUnlocked" class="btn-nav-admin" @click="goAdmin">⚙ Admin</button>
      <a href="tel:+2252722590417" class="btn-nav-cta">📞 Urgences</a>
    </div>
  </nav>
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
.nav-emblem {
  width: 38px;
  height: 38px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--gold), var(--gold-lt));
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  color: #fff;
  font-weight: 700;
  flex-shrink: 0;
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
@media (max-width: 980px) {
  .nav-links {
    display: none;
  }
}
</style>
