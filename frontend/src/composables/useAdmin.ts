import { computed, ref } from "vue";

export type AdminTab =
  | "dashboard"
  | "messages"
  | "articles"
  | "rediger"
  | "blog-categories"
  | "specialties-list"
  | "specialties-editor"
  | "jobs-list"
  | "jobs-editor"
  | "jobs-applications"
  | "promotions-list"
  | "promotions-editor"
  | "backups";

const TAB_TITLES: Record<AdminTab, string> = {
  dashboard: "Vue d'ensemble",
  messages: "Messages reçus",
  articles: "Articles publiés",
  rediger: "Rédiger un article",
  "blog-categories": "Catégories du blog",
  "specialties-list": "Spécialités médicales",
  "specialties-editor": "Éditeur de spécialité",
  "jobs-list": "Offres d'emploi",
  "jobs-editor": "Éditeur d'offre",
  "jobs-applications": "Candidatures reçues",
  "promotions-list": "Offres promotionnelles",
  "promotions-editor": "Éditeur d'offre promotionnelle",
  backups: "Sauvegardes",
};

const activeTab = ref<AdminTab>("dashboard");
const editingSpecialtyId = ref<number | null>(null);
const editingJobOfferId = ref<number | null>(null);
const editingPromotionId = ref<number | null>(null);

export function useAdmin() {
  const title = computed(() => TAB_TITLES[activeTab.value]);

  function setTab(tab: AdminTab) {
    activeTab.value = tab;
  }

  function editSpecialty(id: number | null) {
    editingSpecialtyId.value = id;
    activeTab.value = "specialties-editor";
  }

  function editJobOffer(id: number | null) {
    editingJobOfferId.value = id;
    activeTab.value = "jobs-editor";
  }

  function editPromotion(id: number | null) {
    editingPromotionId.value = id;
    activeTab.value = "promotions-editor";
  }

  return {
    activeTab,
    title,
    setTab,
    editingSpecialtyId,
    editSpecialty,
    editingJobOfferId,
    editJobOffer,
    editingPromotionId,
    editPromotion,
  };
}
