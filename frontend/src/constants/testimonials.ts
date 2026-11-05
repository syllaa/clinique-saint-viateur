export interface Testimonial {
  text: string;
  author: string;
  meta: string;
  stars: string;
}

export const TESTIMONIALS: Testimonial[] = [
  {
    text: "Service pédiatrique excellent et le laboratoire d'analyses est très bien. Accueil professionnel et sympathique. Je recommande vivement cette clinique à toute ma famille.",
    author: "Konan Amenan",
    meta: "Patient – Cocody, Abidjan",
    stars: "★★★★★",
  },
  {
    text: "J'ai accouché à la clinique Saint Viateur. Le personnel soignant est attentionné et très professionnel. L'environnement est propre et rassurant. Merci à toute l'équipe !",
    author: "Adjoua Brou",
    meta: "Patiente maternité",
    stars: "★★★★★",
  },
  {
    text: "Les urgences sont vraiment disponibles à toute heure. Mon fils a été pris en charge rapidement et efficacement un dimanche soir. Très bonne clinique, je recommande sans hésiter.",
    author: "Diomandé Seydou",
    meta: "Patient urgences",
    stars: "★★★★★",
  },
  {
    text: "Médecins très compétents, diagnostic précis et traitement efficace. Le laboratoire rend les résultats rapidement. Une clinique qui fait honneur à Cocody.",
    author: "Bamba Mariam",
    meta: "Patiente – Riviera",
    stars: "★★★★☆",
  },
];
