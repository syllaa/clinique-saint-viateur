import {
  Ambulance,
  Baby,
  Bone,
  BrainCircuit,
  Brain,
  Droplets,
  Ear,
  Eye,
  FlaskConical,
  HeartPulse,
  Hospital,
  Microscope,
  Pill,
  Ribbon,
  Scan,
  Scissors,
  Smile,
  Stethoscope,
  Venus,
  Wind,
} from "@lucide/vue";
import type { Component } from "vue";

export interface SpecialtyIconOption {
  name: string; // stored value, e.g. "heart-pulse"
  label: string;
  category: string;
  component: Component;
}

export const ICON_CATEGORIES = [
  "Cardiologie",
  "Médecine",
  "Pédiatrie",
  "Chirurgie",
  "Laboratoire",
  "Imagerie",
  "Santé de la femme",
  "Santé de l'enfant",
  "Dentaire",
  "Urgences",
  "Autres",
] as const;

export const SPECIALTY_ICONS: SpecialtyIconOption[] = [
  { name: "heart-pulse", label: "Cardiologie", category: "Cardiologie", component: HeartPulse },
  { name: "stethoscope", label: "Médecine générale", category: "Médecine", component: Stethoscope },
  { name: "baby", label: "Pédiatrie", category: "Pédiatrie", component: Baby },
  { name: "venus", label: "Gynécologie", category: "Santé de la femme", component: Venus },
  { name: "brain", label: "Neurologie", category: "Médecine", component: Brain },
  { name: "smile", label: "Dentisterie", category: "Dentaire", component: Smile },
  { name: "eye", label: "Ophtalmologie", category: "Médecine", component: Eye },
  { name: "ear", label: "ORL", category: "Médecine", component: Ear },
  { name: "droplets", label: "Dermatologie", category: "Médecine", component: Droplets },
  { name: "bone", label: "Orthopédie", category: "Chirurgie", component: Bone },
  { name: "wind", label: "Pneumologie", category: "Médecine", component: Wind },
  { name: "flask-conical", label: "Laboratoire", category: "Laboratoire", component: FlaskConical },
  { name: "microscope", label: "Biologie médicale", category: "Laboratoire", component: Microscope },
  { name: "scan", label: "Radiologie", category: "Imagerie", component: Scan },
  { name: "ambulance", label: "Urgences", category: "Urgences", component: Ambulance },
  { name: "pill", label: "Pharmacie", category: "Médecine", component: Pill },
  { name: "ribbon", label: "Oncologie", category: "Médecine", component: Ribbon },
  { name: "brain-circuit", label: "Psychiatrie", category: "Médecine", component: BrainCircuit },
  { name: "scissors", label: "Chirurgie", category: "Chirurgie", component: Scissors },
  { name: "hospital", label: "Autre", category: "Autres", component: Hospital },
];

export const DEFAULT_ICON_NAME = "hospital";

const ICON_MAP: Record<string, SpecialtyIconOption> = Object.fromEntries(
  SPECIALTY_ICONS.map((i) => [i.name, i]),
);

/** Resolve a stored icon_name to its component, falling back to the generic
 * "hospital" icon for unknown/legacy values so rendering never breaks. */
export function resolveSpecialtyIcon(iconName: string | null | undefined): SpecialtyIconOption {
  if (iconName && ICON_MAP[iconName]) return ICON_MAP[iconName];
  return ICON_MAP[DEFAULT_ICON_NAME];
}
