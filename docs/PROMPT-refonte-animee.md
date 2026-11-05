# Prompt — Refonte « nouvelle génération » animée du site Clinique Saint Viateur

> Copie tout ce qui suit dans Claude Code (ou un autre agent de code), lancé à la racine du projet `clinique-saint/`.

---

## Contexte du projet (à lire avant toute modification)

Tu travailles sur le site de la **Clinique Médicale Saint Viateur** (Riviera Sideci, Cocody, Abidjan). Clinique privée, urgences 24h/24, plus de 79 897 patients, lauréate du 3ᵉ Prix national d'excellence médicale.

**Stack existante (à conserver) :**
- `frontend/` : Vue 3.5 + TypeScript + Vite 5 + Pinia + Vue Router, icônes `@lucide/vue`, éditeur TipTap (admin).
- `backend/` : FastAPI + SQLAlchemy + Alembic + MySQL, uploads statiques, sauvegardes planifiées (APScheduler). Modules : `auth`, `blog`, `specialties`, `promotions`, `jobs`, `site` (messages de contact), `support`, `uploads`, `backups`.
- Pages publiques : `HomeView` (1 280 lignes, toute la page d'accueil), `SpecialtiesListView`, `SpecialtyDetailView`, `BlogListView`, `ArticleDetailView`, `PromotionsListView`, `JoinUsView`, `JobOfferDetailView`, `NotFoundView`. Admin caché (Ctrl+Shift+A) : `LoginView`, `AdminView` + `components/admin/*`.
- Design actuel : palette bordeaux/rouge dans `frontend/src/assets/base.css` (`--navy #7a0f1a`, `--blue #c8102e`, `--sky #e0475a`…), titres en *Cormorant Garamond*, texte en *DM Sans*, mode sombre via `:root[data-theme="dark"]` (`useTheme.ts`).
- Animations actuelles (basiques) : directive `v-reveal` (fondu + translation au scroll via IntersectionObserver), directive `v-count-up`, `HeroCanvas.vue` (particules, croix et tracé ECG en canvas 2D), anneaux CSS dans le hero, `JobsTicker`, `PromotionCarousel`. Les pages `ArticleDetailView`, `JobOfferDetailView`, `NotFoundView` n'ont **aucune** animation, et les pages liste n'ont que 3 `v-reveal`.
- Médias disponibles dans `frontend/src/assets/images/` : `hero/` (façade, ambulance, chantier), `facility/` (14 photos : labo, échographie, dentaire, accueil, salles d'attente…), `team/` (portraits, remise de prix, équipes), `patients/` (nouveau-nés, enfants), `events/`. Toutes en `.webp`.

## Objectif

Transformer le site public en une expérience **vivante, cinématographique et « nouvelle génération »**, au niveau d'un site primé (Awwwards), tout en restant un site médical : **rassurant, lisible, rapide et accessible**. Le mouvement doit servir le message (confiance, disponibilité 24/7, excellence, humanité) et pousser vers l'action principale : **appeler / prendre rendez-vous**.

## 1. Fondations du système d'animation

1. Installer `gsap` (avec `ScrollTrigger`, `SplitText` et `Flip`, gratuits depuis GSAP 3.13), `lenis` (smooth scroll) et `lottie-web` (ou `@lottiefiles/dotlottie-web`).
2. Créer `frontend/src/motion/` avec :
   - `tokens.ts` : durées (`fast 0.25s`, `base 0.6s`, `slow 1.2s`) et courbes (`expo.out`, `power3.inOut`, un `customEase` « médical » doux), réutilisées partout.
   - `useLenis.ts` : smooth scroll global synchronisé avec `ScrollTrigger`, désactivé sous `prefers-reduced-motion` et sur l'admin.
   - `useScrollScene.ts` : composable qui crée et nettoie (`gsap.context().revert()` dans `onBeforeUnmount`) les timelines d'une page.
   - Faire évoluer `v-reveal` en `v-reveal="{ type: 'fade' | 'up' | 'mask' | 'split-words' | 'scale', delay, stagger }"` basé sur GSAP, en gardant la compatibilité avec les classes actuelles `.rv`, `.d1`…`.d4`.
3. **Accessibilité obligatoire** : toutes les animations se coupent sous `prefers-reduced-motion: reduce` (le contenu doit apparaître directement à son état final). Ajouter un bouton « Réduire les animations » dans le footer, mémorisé en `localStorage` (avec try/catch).
4. **Performance** : animer uniquement `transform`, `opacity`, `clip-path` et `filter` ; `will-change` posé seulement pendant l'animation ; mettre en pause le canvas et les vidéos hors écran (IntersectionObserver + `document.visibilitychange`) ; cibles : LCP < 2,5 s, CLS < 0,05, 60 fps sur un Android d'entrée de gamme. Charger GSAP, Lottie et les vidéos en lazy loading par page.

## 2. Vidéos et animations générées (style « After Effects »)

Le site doit contenir des **vidéos d'ambiance stratégiques** et des **animations vectorielles de type motion design**.

### 2a. Vidéos d'ambiance (générées par IA, puis intégrées)
Pour chaque emplacement, fournis-moi **le prompt de génération vidéo** (pour Veo, Runway, Kling ou Sora), la durée, le cadrage et la boucle, puis code l'intégration avec un poster `.webp` existant en repli :

| Emplacement | Intention | Spécifications |
|---|---|---|
| Hero (accueil) | « Une clinique qui ne dort jamais » : façade de jour qui passe à la nuit, ambulance qui arrive, lumières qui s'allument | 8–10 s en boucle parfaite, 16:9 et 9:16 (mobile), sans texte, tons chauds bordeaux et ambre, mouvement lent de caméra (dolly) |
| Section « Notre histoire » | Mains de soignants, nouveau-né, stéthoscope, lumière douce | 6 s, boucle, voile bordeaux à 60 % par-dessus |
| Bannière urgences 24/7 | Couloir, gyrophare flouté, rythme cardiaque | 5 s, très sombre, sert de fond au numéro d'urgence |
| `JoinUsView` (recrutement) | Équipe qui rit, collaboration, laboratoire | 8 s, énergique mais posé |
| Chaque spécialité (optionnel) | Plan court lié au service (échographie, pédiatrie, labo…) | 4 s, utilisé au survol de la carte et en fond du header de la page détail |

Règles d'intégration : composant `AmbientVideo.vue` (`<video autoplay muted loop playsinline preload="none">`, sources `.webm` (AV1/VP9) + `.mp4` (H.264), ≤ 2,5 Mo par vidéo, poster obligatoire, lecture seulement quand la vidéo est visible, image fixe sous `prefers-reduced-motion` ou en mode économie de données via `navigator.connection.saveData`). Permettre à l'admin d'uploader une vidéo de couverture par spécialité, ce qui implique d'étendre `SpecialtyEditor.vue`, le modèle `specialty.py` (champ `cover_video_url`) avec une migration Alembic, et le service d'upload (types `video/mp4` et `video/webm`, taille maximale configurable).

### 2b. Motion design vectoriel (équivalent After Effects → Lottie)
Crée des animations Lottie (JSON) ou SVG animées par GSAP pour :
- **Logo animé** au chargement : la croix médicale se dessine (stroke-dashoffset), puis le nom apparaît lettre par lettre (≤ 1,8 s, une fois par session).
- **Ligne ECG signature** : un tracé qui parcourt le site au scroll (`ScrollTrigger` scrub) en reliant les sections, avec un battement à chaque titre de section.
- **Icônes de spécialités animées** au survol (cœur qui bat, dent qui brille, bébé qui bouge, microscope qui zoome…), en remplacement ou en complément des icônes Lucide actuelles.
- **États de formulaire** : envoi (pouls qui accélère), succès (coche qui se dessine avec un éclat), erreur (léger tremblement).
- **Page 404** : animation illustrée (ECG qui s'aplatit puis « repart » au clic sur « Retour à l'accueil »).
Si un fichier Lottie ne peut pas être produit, code l'équivalent en SVG et GSAP. Ne laisse aucun emplacement vide.

## 3. Refonte page par page

### Accueil (`HomeView.vue`) : découpe d'abord la vue en composants de section (`HeroSection`, `ServicesSection`, `OffersSection`, `AboutSection`, `BlogSection`, `TestimonialsSection`, `ContactSection`, `MapBanner`) dans `components/home/`.
- **Préchargement** : rideau bordeaux et logo animé, puis le rideau s'ouvre sur le hero (≤ 2 s, ignoré au retour sur la page).
- **Hero** : vidéo d'ambiance plus `HeroCanvas` (amélioré : particules qui réagissent à la souris, ECG plus net, profondeur en parallaxe). Titre révélé mot par mot avec un masque (SplitText), le mot *Riviera* en italique avec un dégradé animé. Badge « Ouvert maintenant » avec un point qui pulse, calculé en temps réel selon l'heure d'Abidjan. Boutons magnétiques (ils suivent légèrement le curseur). Le bloc urgences « respire » ; au clic sur le numéro, une onde se propage.
- **Bandeau d'infos (strip)** : défilement continu (marquee) infini, qui ralentit au survol.
- **Services** : grille en entrée échelonnée, cartes en tilt 3D au survol avec un reflet lumineux, vidéo ou Lottie de la spécialité au survol, transition partagée (`Flip` ou View Transitions API) de la carte vers la page détail.
- **Offres** : carrousel avec inertie et glisser au doigt, cartes en profondeur (effet « stack »), réactions avec micro-animation.
- **Notre histoire** : section épinglée (pin) avec scroll horizontal ou narration en 3 temps (Fondation → Équipe → Prix d'excellence) qui utilise les photos `team/` et `facility/` en parallaxe ; compteurs qui s'emballent ; trophée qui brille.
- **Galerie de l'établissement** (nouvelle section) : visite virtuelle au scroll des 14 photos `facility/` (zoom de type Ken Burns, révélation par `clip-path`), légendes animées.
- **Témoignages** : défilement infini sur deux rangées en sens opposés, étoiles qui se remplissent une par une.
- **Contact** : champs à label flottant, validation animée en temps réel, horaires avec la journée courante surlignée et un indicateur « ouvert / fermé » en direct.
- **Bannière carte** : carte stylisée (SVG d'Abidjan) avec un pin qui tombe et des ondes ; bouton itinéraire magnétique.

### Pages internes
- **Transitions entre pages** : `<router-view v-slot>` avec `<Transition>`, sous forme de rideau bordeaux en balayage ou de fondu-zoom, et une transition d'élément partagé pour les images (carte → détail) via `document.startViewTransition` quand c'est disponible.
- `SpecialtiesListView` / `BlogListView` / `PromotionsListView` : en-tête avec un titre géant révélé et un fond animé (dégradé en maillage lent), filtres avec un indicateur actif qui glisse, grille qui se réorganise avec `Flip` au filtrage, squelettes de chargement shimmer à la place des spinners.
- `SpecialtyDetailView` : header en vidéo ou parallaxe, sommaire collant avec une barre de progression, médecins en cartes qui se retournent (flip), FAQ en accordéon fluide (hauteur animée).
- `ArticleDetailView` : barre de progression de lecture, image de couverture en parallaxe, citations et titres révélés, temps de lecture.
- `JoinUsView` / `JobOfferDetailView` : vidéo d'équipe, valeurs en cartes animées, chronologie du processus de recrutement dessinée au scroll, formulaire de candidature par étapes avec progression animée.
- **Global** : curseur personnalisé discret sur desktop (un point qui grossit sur les liens, caché au tactile), navbar qui se masque au scroll vers le bas et réapparaît vers le haut, avec un fond flouté (`backdrop-filter`), bouton flottant « Appeler les urgences » qui pulse sur mobile, bascule de thème clair/sombre avec un fondu circulaire (View Transitions).

## 4. Direction artistique

- Garder l'identité bordeaux et les polices actuelles, mais ajouter : grain photographique léger, dégradés en maillage bordeaux → rose (`--sky-light`), verre dépoli pour les cartes flottantes, grands titres éditoriaux (`clamp(3rem, 8vw, 7rem)`) sur le hero et les en-têtes.
- Le mouvement doit rester **calme et maîtrisé** : pas de rebond excessif, pas de clignotement, aucune animation qui bloque la lecture d'une information médicale ou d'un numéro de téléphone. Le numéro d'urgence reste visible et cliquable à tout moment.
- Mode sombre : chaque nouvel effet (vidéo, voiles, Lottie, dégradés) doit avoir sa variante sombre lisible.

## 5. Nettoyage et qualité (à faire en même temps)

- **Supprimer de `frontend/src/assets/images/`** les fichiers qui n'ont rien à faire dans le bundle public et peuvent contenir des données sensibles : `backup_20260826_094448.sql`, `Receipt-2340-6375-3765.pdf`, `01 - Gestionnaire Comptes.docx/.pdf`, `FICHE D'HABILITATION.doc`, `LISTE DES DOSSIER AOUT 26 CLOTURES.docx`, `715478495_…jpg` (le renommer s'il est utilisé). Vérifier ensuite qu'ils ne sont plus dans `frontend/dist/` ni dans l'historique Git à publier.
- Remplacer les emojis d'interface (📞📍✉️🚨🏆) par des icônes Lucide animées, cohérentes entre Windows, Android et iOS.
- SEO : balises Open Graph avec image et vidéo, données structurées `MedicalClinic` / `Hospital` (JSON-LD : horaires, téléphone, adresse, `geo`), `sitemap.xml` généré depuis le backend (spécialités, articles, offres).
- `npm run build` doit passer sans erreur `vue-tsc`. L'admin (`AdminView`, `components/admin/*`) ne doit **pas** être alourdi par GSAP, Lenis ou les vidéos : vérifier le découpage des chunks Vite.

## 6. Méthode de travail attendue

1. Commence par me présenter un **plan en étapes** (fondations → accueil → transitions → pages internes → médias générés → nettoyage), avec la liste des fichiers créés ou modifiés et les dépendances ajoutées. Attends ma validation.
2. Livre étape par étape, avec un commit par étape sur une branche `feat/refonte-animee`, et vérifie après chaque étape avec `npm run build` et un test visuel (`npm run dev` + backend `uvicorn app.main:app --reload --port 8000`).
3. Pour chaque vidéo à générer, rassemble dans `docs/medias-a-generer.md` : prompt de génération, durée, format, emplacement, nom de fichier attendu (`frontend/public/media/…`), poster de repli. Le site doit fonctionner parfaitement avec les posters tant que les vidéos ne sont pas fournies.
4. À la fin, donne un récapitulatif : ce qui a été fait, les mesures Lighthouse (performance et accessibilité, mobile et desktop) avant/après, et ce qui reste à fournir (vidéos réelles, validation client).
