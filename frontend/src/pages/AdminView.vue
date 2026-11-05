<script setup lang="ts">
import { onMounted } from "vue";

import "@/assets/admin.css";
import AdminSidebar from "@/components/admin/AdminSidebar.vue";
import ApplicationsTable from "@/components/admin/ApplicationsTable.vue";
import ArticleEditor from "@/components/admin/ArticleEditor.vue";
import BackupsManager from "@/components/admin/BackupsManager.vue";
import CategoriesManager from "@/components/admin/CategoriesManager.vue";
import JobOfferEditor from "@/components/admin/JobOfferEditor.vue";
import JobsManager from "@/components/admin/JobsManager.vue";
import MessagesTable from "@/components/admin/MessagesTable.vue";
import PromotionEditor from "@/components/admin/PromotionEditor.vue";
import PromotionsManager from "@/components/admin/PromotionsManager.vue";
import SpecialtiesManager from "@/components/admin/SpecialtiesManager.vue";
import SpecialtyEditor from "@/components/admin/SpecialtyEditor.vue";
import { useAdmin } from "@/composables/useAdmin";
import { useArticlesStore } from "@/stores/articles";
import { useBlogCategoriesStore } from "@/stores/blogCategories";
import { useJobApplicationsStore } from "@/stores/jobApplications";
import { useJobOffersStore } from "@/stores/jobOffers";
import { useMessagesStore } from "@/stores/messages";
import { usePromotionsStore } from "@/stores/promotions";
import { useSpecialtiesStore } from "@/stores/specialties";

const { activeTab, title } = useAdmin();
const messages = useMessagesStore();
const articles = useArticlesStore();
const categories = useBlogCategoriesStore();
const specialties = useSpecialtiesStore();
const jobOffers = useJobOffersStore();
const jobApplications = useJobApplicationsStore();
const promotions = usePromotionsStore();

onMounted(() => {
  messages.fetchAll();
  articles.fetchAll();
  categories.fetchAdminAll();
  specialties.fetchAdminAll();
  jobOffers.fetchAdminAll();
  jobApplications.fetchAll();
  promotions.fetchAdminAll();
});
</script>

<template>
  <div class="admin-shell">
    <AdminSidebar />
    <div class="a-main">
      <div class="a-topbar">
        <h1>{{ title }}</h1>
        <div style="display: flex; align-items: center; gap: 10px">
          <span class="a-badge">Administrateur</span>
        </div>
      </div>

      <div class="a-content">
        <div v-if="activeTab === 'dashboard'">
          <div class="dash-row">
            <div class="dcard">
              <div class="dcard-ico">✉️</div>
              <div class="dcard-n">{{ messages.unreadCount }}</div>
              <div class="dcard-l">Nouveaux messages</div>
            </div>
            <div class="dcard">
              <div class="dcard-ico">📰</div>
              <div class="dcard-n">{{ articles.adminItems.filter((a) => a.status === 'published').length }}</div>
              <div class="dcard-l">Articles publiés</div>
            </div>
            <div class="dcard">
              <div class="dcard-ico">🩺</div>
              <div class="dcard-n">{{ specialties.adminItems.length }}</div>
              <div class="dcard-l">Spécialités</div>
            </div>
            <div class="dcard">
              <div class="dcard-ico">📥</div>
              <div class="dcard-n">{{ messages.items.length }}</div>
              <div class="dcard-l">Messages au total</div>
            </div>
          </div>
          <div class="a-sec-title">Derniers messages reçus</div>
          <table class="a-table">
            <thead>
              <tr>
                <th>Expéditeur</th>
                <th>Sujet</th>
                <th>Date</th>
                <th>Statut</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="m in messages.items.slice(0, 4)" :key="m.id">
                <td style="font-weight: 500; color: var(--a-text)">{{ m.name }}</td>
                <td>{{ m.subject }}</td>
                <td style="white-space: nowrap; font-size: 0.75rem">
                  {{ new Date(m.created_at).toLocaleString("fr-FR") }}
                </td>
                <td>
                  <span class="msg-badge" :class="m.status === 'new' ? 'mb-new' : 'mb-read'">
                    {{ m.status === "new" ? "Nouveau" : "Lu" }}
                  </span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <MessagesTable v-else-if="activeTab === 'messages'" />
        <ArticleEditor v-else-if="activeTab === 'articles' || activeTab === 'rediger'" />
        <CategoriesManager v-else-if="activeTab === 'blog-categories'" />
        <SpecialtiesManager v-else-if="activeTab === 'specialties-list'" />
        <SpecialtyEditor v-else-if="activeTab === 'specialties-editor'" />
        <JobsManager v-else-if="activeTab === 'jobs-list'" />
        <JobOfferEditor v-else-if="activeTab === 'jobs-editor'" />
        <ApplicationsTable v-else-if="activeTab === 'jobs-applications'" />
        <PromotionsManager v-else-if="activeTab === 'promotions-list'" />
        <PromotionEditor v-else-if="activeTab === 'promotions-editor'" />
        <BackupsManager v-else-if="activeTab === 'backups'" />
      </div>
    </div>
  </div>
</template>

<style scoped>
.admin-shell {
  position: fixed;
  inset: 0;
  z-index: 8000;
  background: var(--a-bg);
  display: flex;
  flex-direction: row;
}
</style>
