<script setup lang="ts">
import { computed } from "vue";
import { useRouter } from "vue-router";

import { useAdmin, type AdminTab } from "@/composables/useAdmin";
import { useTheme } from "@/composables/useTheme";
import { useAuthStore } from "@/stores/auth";
import { useJobApplicationsStore } from "@/stores/jobApplications";
import { useMessagesStore } from "@/stores/messages";
import { usePromotionsStore } from "@/stores/promotions";

const { activeTab, setTab } = useAdmin();
const messages = useMessagesStore();
const applications = useJobApplicationsStore();
const promotions = usePromotionsStore();
const auth = useAuthStore();
const router = useRouter();
const { isDark, toggle } = useTheme();

const newApplicationsCount = computed(() => applications.items.filter((a) => a.status === "nouvelle").length);
const activePromotionsCount = computed(
  () => promotions.adminItems.filter((p) => p.is_published && !p.is_expired).length,
);

function logout() {
  auth.logout();
  router.push({ name: "home" });
}
</script>

<template>
  <aside class="a-sidebar">
    <div class="a-logo">
      <div class="a-logo-em">✚</div>
      <div class="a-logo-txt">Saint Viateur<small>Administration</small></div>
    </div>
    <nav class="a-nav">
      <div class="a-nav-sec">Tableau de bord</div>
      <div class="a-nav-item" :class="{ on: activeTab === 'dashboard' }" @click="setTab('dashboard' as AdminTab)">
        <span class="a-nav-icon">📊</span>Vue d'ensemble
      </div>
      <div class="a-nav-item" :class="{ on: activeTab === 'messages' }" @click="setTab('messages' as AdminTab)">
        <span class="a-nav-icon">✉️</span>Messages
        <span v-if="messages.unreadCount > 0" class="a-nav-badge">{{ messages.unreadCount }}</span>
      </div>
      <div class="a-nav-sec">Contenu</div>
      <div class="a-nav-item" :class="{ on: activeTab === 'articles' }" @click="setTab('articles' as AdminTab)">
        <span class="a-nav-icon">📰</span>Articles publiés
      </div>
      <div class="a-nav-item" :class="{ on: activeTab === 'rediger' }" @click="setTab('rediger' as AdminTab)">
        <span class="a-nav-icon">✏️</span>Rédiger un article
      </div>
      <div
        class="a-nav-item"
        :class="{ on: activeTab === 'blog-categories' }"
        @click="setTab('blog-categories' as AdminTab)"
      >
        <span class="a-nav-icon">🏷️</span>Catégories du blog
      </div>
      <div class="a-nav-sec">Spécialités</div>
      <div
        class="a-nav-item"
        :class="{ on: activeTab === 'specialties-list' || activeTab === 'specialties-editor' }"
        @click="setTab('specialties-list' as AdminTab)"
      >
        <span class="a-nav-icon">🩺</span>Spécialités médicales
      </div>
      <div class="a-nav-sec">Recrutement</div>
      <div
        class="a-nav-item"
        :class="{ on: activeTab === 'jobs-list' || activeTab === 'jobs-editor' }"
        @click="setTab('jobs-list' as AdminTab)"
      >
        <span class="a-nav-icon">💼</span>Offres d'emploi
      </div>
      <div
        class="a-nav-item"
        :class="{ on: activeTab === 'jobs-applications' }"
        @click="setTab('jobs-applications' as AdminTab)"
      >
        <span class="a-nav-icon">📥</span>Candidatures
        <span v-if="newApplicationsCount > 0" class="a-nav-badge">{{ newApplicationsCount }}</span>
      </div>
      <div class="a-nav-sec">Promotions</div>
      <div
        class="a-nav-item"
        :class="{ on: activeTab === 'promotions-list' || activeTab === 'promotions-editor' }"
        @click="setTab('promotions-list' as AdminTab)"
      >
        <span class="a-nav-icon">🎁</span>Offres promotionnelles
        <span v-if="activePromotionsCount > 0" class="a-nav-badge">{{ activePromotionsCount }}</span>
      </div>
      <div class="a-nav-sec">Système</div>
      <div class="a-nav-item" :class="{ on: activeTab === 'backups' }" @click="setTab('backups' as AdminTab)">
        <span class="a-nav-icon">🗄</span>Sauvegardes
      </div>
      <div class="a-nav-item" :class="{ on: activeTab === 'security' }" @click="setTab('security' as AdminTab)">
        <span class="a-nav-icon">🔒</span>Sécurité
        <span v-if="auth.weakPassword" class="a-nav-badge" title="Mot de passe à changer">!</span>
      </div>
    </nav>
    <div class="a-sidebar-foot">
      <button class="back-link theme-toggle-link" @click="toggle(true)">
        {{ isDark(true) ? "☀️ Mode clair" : "🌙 Mode sombre" }}
      </button>
      <button class="back-link" @click="logout">← Se déconnecter</button>
    </div>
  </aside>
</template>

<style scoped>
.a-sidebar {
  width: 248px;
  background: var(--a-panel);
  border-right: 1px solid var(--a-border);
  display: flex;
  flex-direction: column;
  flex-shrink: 0;
}
.a-logo {
  padding: 20px 18px 16px;
  border-bottom: 1px solid var(--a-border);
  display: flex;
  align-items: center;
  gap: 10px;
}
.a-logo-em {
  width: 34px;
  height: 34px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--a-gold), #c8102e);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-size: 16px;
  font-weight: 700;
}
.a-logo-txt {
  font-size: 0.78rem;
  font-weight: 600;
  color: var(--a-text);
  line-height: 1.3;
}
.a-logo-txt small {
  display: block;
  font-size: 0.6rem;
  color: var(--a-muted);
  font-weight: 400;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}
.a-nav {
  flex: 1;
  padding: 14px 0;
  overflow-y: auto;
}
.a-nav-sec {
  font-size: 0.58rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.18em;
  color: var(--a-muted);
  padding: 12px 18px 5px;
  opacity: 0.55;
}
.a-nav-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 9px 18px;
  font-size: 0.82rem;
  color: var(--a-text-3);
  cursor: pointer;
  transition: all 0.2s;
  border-left: 2px solid transparent;
}
.a-nav-item:hover {
  color: var(--a-text);
  background: var(--a-tint);
}
.a-nav-item.on {
  color: var(--a-gold);
  background: rgba(224, 71, 90, 0.07);
  border-left-color: var(--a-gold);
}
.a-nav-icon {
  font-size: 0.95rem;
  width: 20px;
  text-align: center;
}
.a-nav-badge {
  margin-left: auto;
  background: var(--teal);
  color: #fff;
  font-size: 0.58rem;
  font-weight: 700;
  padding: 2px 7px;
  border-radius: 100px;
}
.a-sidebar-foot {
  padding: 14px 18px;
  border-top: 1px solid var(--a-border);
}
.back-link {
  background: none;
  border: none;
  color: var(--a-muted);
  font-size: 0.78rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 6px;
  transition: color 0.2s;
}
.back-link:hover {
  color: var(--a-text);
}
@media (max-width: 980px) {
  .a-sidebar {
    width: 195px;
  }
}
</style>
