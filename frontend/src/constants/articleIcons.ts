export interface ArticleIconOption {
  emoji: string;
  label: string;
}

export const ARTICLE_ICONS: ArticleIconOption[] = [
  { emoji: "📋", label: "Actualité" },
  { emoji: "📰", label: "Article" },
  { emoji: "📢", label: "Annonce" },
  { emoji: "🔔", label: "Information" },
  { emoji: "📅", label: "Événement" },
  { emoji: "🩺", label: "Médecine générale" },
  { emoji: "🫀", label: "Cardiologie" },
  { emoji: "🧠", label: "Neurologie" },
  { emoji: "👶", label: "Pédiatrie" },
  { emoji: "🤰", label: "Maternité" },
  { emoji: "🦷", label: "Dentaire" },
  { emoji: "👁️", label: "Ophtalmologie" },
  { emoji: "🦴", label: "Orthopédie" },
  { emoji: "💉", label: "Vaccination" },
  { emoji: "💊", label: "Pharmacie" },
  { emoji: "🔬", label: "Laboratoire" },
  { emoji: "🦟", label: "Prévention" },
  { emoji: "🥗", label: "Nutrition" },
  { emoji: "🏃", label: "Bien-être" },
  { emoji: "😷", label: "Maladie" },
  { emoji: "🚑", label: "Urgences" },
  { emoji: "🏥", label: "Clinique" },
];

export const DEFAULT_ARTICLE_ICON = "📋";
