# Audit technique complet — Clinique Médicale Saint Viateur

**Date :** 5 novembre 2026 · **Phase :** 1 (audit), sans aucune modification du code · **Périmètre :** `frontend/`, `backend/`, `docs/`

---

## 0. Synthèse

Le projet est **sain et bien construit** : architecture claire, routes d'administration réellement protégées côté serveur, uploads validés et ré-encodés, HTML d'articles nettoyé (nh3), sauvegardes automatiques avec rétention, et **62 tests backend qui passent**. La refonte peut donc se faire **par évolution**, sans reconstruction.

Les vrais problèmes sont ailleurs :

| Priorité | Problème | Impact |
|---|---|---|
| 🔴 Bloquant | Le dépôt Git est **tout le dossier utilisateur** `C:/Users/LENOVO`, sans aucun commit | Pas d'historique, pas de retour arrière possible, branche `feat/refonte-animee` impossible à exploiter proprement |
| 🔴 Critique | Mot de passe admin initial = `admin123` dans `backend/.env` | Si la base a été créée avec cette valeur et jamais changée, l'administration est ouverte à quiconque |
| 🔴 Critique | **Aucun menu sur mobile** : les liens de navigation sont masqués sous 980 px sans menu burger | Sur smartphone (la majorité du trafic en Côte d'Ivoire), on ne peut accéder ni aux spécialités, ni au blog, ni au recrutement depuis la barre de navigation |
| 🟠 Élevé | Aucune limitation de débit sur `/auth/login`, le formulaire de contact, les candidatures et les réactions | Attaque par force brute sur l'admin, spam de messages et de CV |
| 🟠 Élevé | Documents sensibles dans `frontend/src/assets/images/` (sauvegarde SQL, reçu, comptes, habilitation, dossiers clôturés) | **Pas** présents dans le site publié (vérifié dans `dist/`), mais exposés à quiconque reçoit le code source |
| 🟠 Élevé | Le jeton de rafraîchissement n'est jamais utilisé : la session admin expire au bout de 30 min | Perte possible d'un article en cours de rédaction dans l'éditeur |
| 🟡 Moyen | Seules **2 photos sur environ 60** sont utilisées sur le site | Gros potentiel visuel inexploité, en lien direct avec l'objectif de la refonte |
| 🟡 Moyen | `HomeView.vue` fait 1 280 lignes et `SpecialtyDetailView.vue` 825 | Maintenance difficile, refonte risquée sans découpage préalable |
| 🟡 Moyen | Témoignages patients écrits en dur dans le code, sans source vérifiable | Risque juridique et de crédibilité s'ils ne sont pas authentiques et autorisés |

---

## 1. Architecture actuelle

```
clinique-saint/
├── backend/                 FastAPI · SQLAlchemy 2 · Alembic · MySQL (PyMySQL)
│   ├── app/
│   │   ├── main.py          lifespan : create_all + seed admin/contenu + sauvegarde planifiée (APScheduler)
│   │   ├── config.py        pydantic-settings, lit backend/.env
│   │   ├── auth/            JWT (python-jose) + bcrypt (passlib), rôles via User.role
│   │   ├── blog/ jobs/ promotions/ site/ specialties/ support/ uploads/ backups/
│   │   │                    chaque module : router · service · crud · schemas
│   │   ├── models/          13 modèles SQLAlchemy
│   │   ├── seed.py          contenu initial (spécialités…)
│   │   └── utils.py         nettoyage HTML (nh3)
│   ├── alembic/versions/    8 migrations (0001 → 0008)
│   ├── mcp/admin_ticket.py  serveur MCP local pour gérer les tickets de support
│   ├── tests/               10 fichiers, 62 tests (SQLite en mémoire)
│   ├── uploads/             images publiques + CV privés (ignorés par .gitignore)
│   ├── backups/             fichiers mysqldump (ignorés par .gitignore)
│   └── clisvenv/            environnement virtuel Python
├── frontend/                Vue 3.5 · TypeScript · Vite 5 · Pinia · Vue Router · Lucide · TipTap · Axios
│   └── src/
│       ├── pages/           11 vues (9 publiques, 2 admin)
│       ├── components/      admin (15) · blog (2) · common (7) · hero (1) · jobs (1) · layout (3) · promotions (2) · specialties (2)
│       ├── stores/          9 stores Pinia
│       ├── services/        10 services API (Axios)
│       ├── composables/     auth, admin, thème, dialogues, SEO (useHead), identifiant d'appareil
│       ├── directives/      v-reveal, v-count-up
│       ├── constants/       icônes, témoignages
│       └── assets/          base.css, admin.css, images/
└── docs/                    documentation PDF, vidéo de démo, guide d'enregistrement, prompts
```

**Flux :** le frontend (port 5173) appelle l'API (port 8000) via Axios (`VITE_API_URL`, par défaut `http://localhost:8000`). Les images uploadées sont servies en statique sur `/uploads/images`. Les CV ne sont **jamais** servis en statique : ils passent par une route authentifiée.

**Déploiement :** un `Dockerfile` par application (backend : `uvicorn` ; frontend : build puis `serve -s dist`). Pas de `docker-compose`, pas de proxy inverse, pas de configuration de production documentée.

---

## 2. Cartographie des pages

| Route | Vue | Rôle | Données | Animations actuelles |
|---|---|---|---|---|
| `/` | `HomeView` (1 280 l.) | Accueil : hero, bandeau d'infos, services, offres, histoire, blog, témoignages, contact, carte | spécialités, promotions, articles, envoi de message | 45 `v-reveal`, compteurs, `HeroCanvas`, anneaux CSS |
| `/specialites` | `SpecialtiesListView` | Liste des spécialités | spécialités | 3 `v-reveal` |
| `/specialites/:slug` | `SpecialtyDetailView` (825 l.) | Détail, médecins, FAQ | spécialité par slug | 16 `v-reveal` |
| `/blog` | `BlogListView` | Articles et catégories, pagination | articles, catégories | 3 `v-reveal` |
| `/blog/:slug` | `ArticleDetailView` | Article, FAQ, articles liés | article, articles liés | **aucune** |
| `/promotions` | `PromotionsListView` | Offres et réactions | promotions, catégories | 3 `v-reveal` |
| `/nous-rejoindre` | `JoinUsView` | Recrutement | offres d'emploi | 13 `v-reveal` |
| `/nous-rejoindre/offres/:slug` | `JobOfferDetailView` | Offre et candidature (CV en PDF) | offre, candidature | **aucune** |
| `/login` | `LoginView` | Connexion admin | auth | — |
| `/admin` | `AdminView` | Back-office | tous les modules | — |
| `/*` | `NotFoundView` | Page 404 | — | **aucune** |

**Composants globaux :** `JobsTicker` (bandeau des offres sous la navbar, sur toutes les pages publiques), `DialogModal` (alertes et confirmations), `NavBar` et `FooterBar` (inclus page par page, pas dans `App.vue`).

**Garde de navigation :** `/login` et `/admin` renvoient une 404 tant que l'accès n'est pas déverrouillé (Ctrl+Shift+A, état gardé en `localStorage`), puis `/admin` exige un utilisateur authentifié avec le rôle admin. Le raccourci n'est qu'un **masquage visuel** : la vraie protection est bien côté backend (voir §5).

---

## 3. Cartographie des API

Légende : 🔓 public · 🔒 admin (`require_admin`).

| Module | Préfixe | Routes publiques | Routes admin |
|---|---|---|---|
| auth | `/auth` | 🔓 `POST /login`, `POST /refresh` · utilisateur connecté : `GET /me` | — |
| site | `/api/site` | 🔓 `POST /messages` (formulaire de contact) | 🔒 liste, marquer lu, tout marquer lu, supprimer |
| specialties | `/api/specialties` | 🔓 `GET /`, `GET /{slug}` | 🔒 CRUD, réordonnancement, médecins, FAQ |
| blog | `/api/blog` | 🔓 catégories, articles (paginés), article par slug, articles liés | 🔒 CRUD articles et catégories, FAQ |
| promotions | `/api/promotions` | 🔓 catégories, actives, toutes (paginées), `POST /{id}/reactions` | 🔒 CRUD, activer/désactiver |
| jobs | `/api/jobs` | 🔓 offres, offre par slug, `POST /offers/{slug}/applications` (upload de CV) | 🔒 CRUD offres, candidatures, statut, téléchargement de CV |
| support | `/api/support` | — | 🔒 tout le routeur (tickets) |
| uploads | `/api/uploads` | — | 🔒 `POST /images` |
| backups | `/api/backups` | — | 🔒 lister, créer, télécharger, supprimer |
| santé | `/` | 🔓 `GET /` | — |
| statique | `/uploads/images` | 🔓 images uploadées | — |

**Constat :** toutes les routes d'écriture sensibles sont protégées. Les quatre routes publiques en écriture (`/auth/login`, `/api/site/messages`, candidatures, réactions) n'ont **aucune limitation de débit ni anti-spam**.

**Modèles (13) :** `User`, `Specialty`, `SpecialtyDoctor`, `SpecialtyFaq`, `Article`, `ArticleFaq`, `BlogCategory`, `Promotion`, `PromotionReaction` (identifiée par un identifiant d'appareil généré côté client), `JobOffer`, `JobApplication`, `Message`, `Ticket`.

---

## 4. Modules d'administration

`AdminView` + `AdminSidebar` orchestrent les gestionnaires suivants :

| Gestionnaire | Composants | Fonctions |
|---|---|---|
| Spécialités | `SpecialtiesManager`, `SpecialtyEditor`, `IconPicker`, `EmojiPicker` | CRUD, ordre, média (icône, emoji ou image), médecins, FAQ |
| Articles | `ArticleEditor`, `RichTextEditor` (TipTap), `CategoriesManager` | CRUD, catégories, FAQ, image de couverture |
| Promotions | `PromotionsManager`, `PromotionEditor` | CRUD, activation |
| Recrutement | `JobsManager`, `JobOfferEditor`, `ApplicationsTable` | offres, candidatures, CV |
| Messages | `MessagesTable` | lecture, suppression |
| Sauvegardes | `BackupsManager` | création manuelle, téléchargement, suppression |

L'admin a son propre thème (sombre par défaut, `admin.css`). **À préserver intégralement** lors de la refonte : aucune bibliothèque d'animation ne doit y être chargée.

---

## 5. Sécurité

### Points solides (à conserver)
- `require_admin` appliqué au niveau des routeurs `support`, `uploads` et `backups`, et route par route ailleurs, avec un contrôle réel du rôle.
- Images : liste blanche d'extensions, taille maximale, **décodage Pillow puis ré-encodage en WebP** (un faux fichier image est rejeté), redimensionnement à 1 600 px, nom de fichier en UUID.
- CV : PDF uniquement, signature `%PDF-` vérifiée, stockage hors du dossier statique, téléchargement réservé à l'admin.
- Sauvegardes : nom de fichier validé par une expression régulière (pas de traversée de répertoire), mot de passe MySQL passé par variable d'environnement et non en ligne de commande.
- HTML des articles nettoyé avec nh3.
- `SECRET_KEY` personnalisée (86 caractères, pas la valeur par défaut).
- `.env`, `uploads/` et `backups/` exclus par `.gitignore`.

### Problèmes
| # | Gravité | Constat | Recommandation |
|---|---|---|---|
| S1 | 🔴 | `ADMIN_PASSWORD=admin123` dans `.env`. Le compte est créé avec ce mot de passe si la table des utilisateurs est vide au démarrage. | Changer immédiatement le mot de passe du compte en base ; ajouter une fonction de changement de mot de passe dans l'admin ; refuser de démarrer en production avec `admin123`. |
| S2 | 🟠 | Pas de limitation de débit sur la connexion, le contact, les candidatures et les réactions. | Ajouter `slowapi` (ou équivalent) : par exemple 5 tentatives de connexion par minute et par IP, et un champ piège (honeypot) sur les formulaires publics. |
| S3 | 🟠 | Jetons JWT stockés en `localStorage`, donc lisibles en cas de faille XSS. | Risque réduit par nh3. À terme, envisager un cookie `HttpOnly` pour le jeton de rafraîchissement. Hors périmètre de la refonte, sauf validation. |
| S4 | 🟠 | Fichiers sensibles dans `frontend/src/assets/images/` : `backup_20260826_094448.sql`, `Receipt-2340-6375-3765.pdf`, `01 - Gestionnaire Comptes.docx/.pdf`, `FICHE D'HABILITATION.doc`, `LISTE DES DOSSIER AOUT 26 CLOTURES.docx`. Aucun n'est référencé dans le code et aucun n'est dans `dist/`. | Les **déplacer** hors du projet (et non les supprimer) : la sauvegarde SQL existe déjà dans `backend/backups/`, mais je ne supprime rien sans ton accord. |
| S5 | 🟡 | `DEBUG=true` dans `.env`. | `false` en production (créer un `.env.production.example`). |
| S6 | 🟡 | Le jeton de rafraîchissement est émis mais jamais utilisé : à la première erreur 401, le frontend déconnecte sans tenter de renouveler la session. | Ajouter un renouvellement automatique dans l'intercepteur Axios. Corrige aussi le problème de perte de travail dans l'éditeur. |
| S7 | 🟡 | Aucune en-tête de sécurité HTTP (CSP, `X-Content-Type-Options`, `Referrer-Policy`, HSTS). | À ajouter au proxy inverse lors du déploiement, ou via un middleware. |
| S8 | 🟡 | Pas de changement de mot de passe ni de gestion multi-utilisateurs dans l'admin. | À prévoir avec S1. |
| S9 | ℹ️ | `Base.metadata.create_all()` au démarrage **en plus** d'Alembic. | Risque de schéma qui diverge des migrations. À terme, n'utiliser que `alembic upgrade head`. |

---

## 6. Frontend : qualité, design, accessibilité

### Design
- La palette est centralisée dans `base.css`, mais les **noms des variables trompent** : `--navy` est un bordeaux, `--gold` et `--green` sont des rouges. C'est l'héritage d'un ancien thème bleu et or.
- **Le préchargeur de `index.html` utilise encore l'ancien thème** (fond bleu marine `#0a1f3c`, emblème doré) : à chaque chargement, une couleur hors charte s'affiche brièvement.
- Les icônes d'interface sont des emojis (📞📍✉️🚨🏆☀️🌙), dont le rendu varie selon Windows, Android et iOS.
- Le logo est le caractère `✚` dans un cercle : il n'existe ni logo vectoriel ni favicon.
- `NavBar` et `FooterBar` sont importés page par page au lieu d'être dans le layout : à centraliser pour permettre des transitions entre pages.

### Accessibilité
| Constat | Gravité |
|---|---|
| Aucun menu sur mobile sous 980 px (voir la synthèse) | 🔴 |
| Libellés de formulaire de l'accueil non reliés à leurs champs (`<label>` sans `for` ni imbrication) : un lecteur d'écran ne les annonce pas | 🟠 |
| Seulement 12 attributs `aria-*` et 13 styles `:focus` sur tout le frontend : le focus clavier est peu visible | 🟠 |
| Bouton de thème sans `aria-label` (il n'a qu'un `title` et un emoji) | 🟡 |
| `v-reveal` et `v-count-up` respectent déjà `prefers-reduced-motion` ✅ | — |
| Logo de la navbar avec `href="#"` au lieu de `/` | 🟡 |

### Robustesse
- Les stores n'interceptent pas les erreurs (`fetchAll()` est appelé sans `try/catch` dans `onMounted`). Si l'API tombe, les sections restent vides sans message d'erreur, avec une promesse rejetée non gérée en console.
- `localStorage` est lu sans `try/catch` dans `useAdminAccess`, `useTheme`, `useDeviceId` et `auth`, ce qui peut planter l'application en navigation privée stricte (Safari).
- Témoignages : `constants/testimonials.ts` contient 4 avis écrits en dur, présentés comme « partagés sur Facebook ». **Leur authenticité et l'autorisation de publication doivent être confirmées par la clinique.** Sinon, il faut les retirer ou les remplacer par de vrais avis gérés depuis l'admin.

### SEO
- `useHead.ts` gère titre, description, Open Graph, URL canonique et JSON-LD par page ✅. Une limite est documentée dans le code : sans rendu côté serveur, Facebook et WhatsApp ne voient que les balises de `index.html`.
- Il n'y a **pas de dossier `public/`** : pas de `robots.txt`, de `sitemap.xml`, de favicon ni d'image de partage.
- Recommandation : pré-rendre les pages publiques au build (`vite-ssg` ou un plugin de prérendu). Cela règle les aperçus de partage sans changer d'architecture.

### Médias
| Dossier | Poids | Utilisé dans le code |
|---|---|---|
| `team/` | 2,5 Mo (25 photos) | 0 |
| `hero/` | 820 Ko (3) | 1 (`hero-clinic-facade-street`) |
| `facility/` | 792 Ko (14) | 0 |
| `patients/` | 416 Ko (7) | 0 |
| `events/` | 192 Ko (2) | 0 |
| `715478495_…jpg` | — | 0 (nom non descriptif) |

Une deuxième image (`team-staff-group-large`) apparaît dans `dist/`, sans doute via un CSS. Les photos sont déjà en WebP et légères. Il faut en produire des **variantes responsives** (`srcset`) pour la refonte.

**Point de vigilance :** les photos de `patients/` montrent des nouveau-nés et des enfants. Leur publication suppose une **autorisation écrite des parents**, à confirmer par la clinique avant tout usage.

---

## 7. Performance (état initial)

- Build : chargement différé des routes ✅, aucune bibliothèque lourde côté public (TipTap est importé uniquement par les composants admin, à vérifier dans le découpage des chunks).
- `HeroCanvas` : 65 particules plus un tracé ECG en `requestAnimationFrame`, **sans pause hors écran ni quand l'onglet est caché** : consommation de batterie inutile sur mobile.
- Polices Google chargées de façon bloquante (pas de `preconnect`).
- Mesures Lighthouse : **non réalisées à ce stade**. Elles nécessitent un build de production servi localement ; je les ferai au début de l'étape 3 pour disposer d'une base avant/après.

---

## 8. DevOps et dépendances

| Élément | Constat |
|---|---|
| **Git** | 🔴 La racine du dépôt est `C:/Users/LENOVO`, sans aucun commit. Le projet n'est pas versionné en tant que tel. |
| Backend `requirements.txt` | Versions minimales (`>=`) sans verrouillage : les builds ne sont pas reproductibles. `passlib` n'est plus maintenu (contourné par `bcrypt<4.1`). `pytest` et `httpx` sont mélangés aux dépendances de production. |
| Backend `Dockerfile` | Installe `default-libmysqlclient-dev` et `build-essential` alors que le projet utilise PyMySQL (pur Python) : l'image est alourdie inutilement. |
| Frontend `Dockerfile` | `npm install` sans copier `package-lock.json` (au lieu de `npm ci`), `VITE_API_URL` non fourni au build : l'image appellerait `localhost:8000`. |
| Orchestration | Pas de `docker-compose` (MySQL, API, front, proxy). |
| Sauvegardes | Automatiques toutes les 24 h, rétention 14 jours, et 2 sauvegardes présentes. **Elles restent sur la même machine que la base** : il faut prévoir une copie externe. |
| Tests | Backend : 62/62 ✅ (SQLite en mémoire, sans risque pour les données). Frontend : `vue-tsc` sans erreur ✅, **aucun test automatisé**. |

---

## 9. Fonctionnalités à préserver impérativement

1. Connexion admin, rôles, accès masqué par raccourci clavier (comportement actuel).
2. Toutes les opérations CRUD de l'admin : spécialités (avec médecins, FAQ, ordre, médias), articles (TipTap, catégories, FAQ), promotions, offres d'emploi, candidatures, messages.
3. Upload d'images (ré-encodage WebP) et de CV (PDF privé).
4. Sauvegardes automatiques et manuelles.
5. Formulaire de contact (avec urgence et demande d'hospitalisation) et formulaire de candidature.
6. Réactions aux promotions par identifiant d'appareil.
7. Mode sombre public et thème de l'admin.
8. SEO par page (`useHead`) et URL existantes (`/specialites/:slug`, `/blog/:slug`, `/nous-rejoindre/offres/:slug`).
9. `JobsTicker` et serveur MCP des tickets.
10. Contrats d'API : aucun champ supprimé ni renommé. Les ajouts se font uniquement par migration réversible.

---

## 10. Plan d'exécution proposé

Chaque étape se termine par : tests backend, `vue-tsc`, build, vérification visuelle, puis un commit. Les étapes marquées ⏸ attendent ta validation.

| # | Étape | Contenu | Risque |
|---|---|---|---|
| **0** | **Mise en sécurité** ⏸ | `git init` dans `clinique-saint/` (dépôt propre, `.gitignore` complet), premier commit de l'état actuel, branche `feat/refonte-animee`. Déplacement des documents sensibles hors du projet. Rappel du changement du mot de passe admin. | Faible |
| 1 | Correctifs bloquants | Menu mobile (burger accessible), libellés de formulaires, focus visible, préchargeur aux couleurs de la charte, `try/catch` sur `localStorage`, gestion des erreurs des stores, renouvellement du jeton. | Faible |
| 2 | Fondations du design | Renommer les variables CSS (avec alias de compatibilité), système de design (boutons, cartes, badges, champs, états), icônes Lucide à la place des emojis, logo SVG et favicon. `NavBar`/`FooterBar` déplacés dans un layout public. Mesure Lighthouse de référence. | Moyen (visuel global) |
| 3 | Système d'animation | `frontend/src/motion/` (tokens, Lenis, scènes, préférences), GSAP/ScrollTrigger/Flip chargés **uniquement côté public**, `v-reveal` v2 rétrocompatible, réglage « Réduire les animations ». Vérification que le chunk admin n'est pas alourdi. | Moyen |
| 4 | Page d'accueil | Découpage de `HomeView` en 9 sections, hero immersif, galerie de l'établissement, histoire narrative, ligne ECG, logo animé. Photos réelles exploitées. | Moyen |
| 5 | Pages internes | Transitions entre pages, en-têtes, grilles animées, squelettes de chargement, états vides et d'erreur, barre de lecture des articles, 404 animée, découpage de `SpecialtyDetailView`. | Moyen |
| 6 | Vidéos et motion design | `AmbientVideo.vue` (poster, chargement différé, mode économie de données, pause hors écran), `docs/medias-a-generer.md` avec les prompts de génération, animations SVG/Lottie. **Aucune vidéo affichée tant qu'elle n'est pas fournie.** | Faible |
| 7 | Admin et backend ⏸ | Champ `cover_video_url` (migration Alembic réversible 0009), upload vidéo (MP4/WebM, type et taille vérifiés), aperçu, remplacement et suppression dans `SpecialtyEditor`. Limitation de débit et champ piège. Changement de mot de passe admin. Nouveaux tests. | Moyen |
| 8 | Accessibilité, responsive, SEO | Revue WCAG 2.2 AA, tests sur 5 formats d'écran, `robots.txt`, `sitemap.xml` (généré par le backend), JSON-LD `MedicalClinic` avec les seules données vérifiées, prérendu pour les aperçus de partage. | Moyen |
| 9 | Performance et DevOps | Variantes responsives des images, `preconnect` des polices, pause de `HeroCanvas`, découpage des chunks, Dockerfiles corrigés, `docker-compose`, `.env.production.example`, en-têtes de sécurité. Mesure Lighthouse finale. | Faible |
| 10 | Livraison | Rapport des modifications, comparaison avant/après, fichiers créés et modifiés, dépendances, migrations, résultats des tests, instructions de déploiement. | — |

### Dépendances envisagées (à confirmer à l'étape 3)
- Frontend : `gsap` (ScrollTrigger, Flip, SplitText, gratuits y compris en usage commercial depuis la 3.13), `lenis`. `lottie-web` seulement si un fichier Lottie est réellement fourni, sinon SVG + GSAP (plus léger). Éventuellement `vite-ssg` ou un plugin de prérendu à l'étape 8.
- Backend : `slowapi` (limitation de débit).

---

## 11. Décisions à prendre avant de commencer

1. **Git** : d'accord pour créer un dépôt propre dans `clinique-saint/` (le dépôt actuel englobe tout ton dossier utilisateur) ?
2. **Documents sensibles** : où les déplacer (par exemple `C:\Users\LENOVO\Documents\clinique-archives\`) ?
3. **Mot de passe admin** : est-il encore `admin123` dans la base ? Le site est-il déjà en ligne ?
4. **Témoignages** : sont-ils authentiques et autorisés ? Sinon, faut-il les retirer ou créer un module « Avis » géré depuis l'admin ?
5. **Photos de patients** (nouveau-nés, enfants) : l'autorisation parentale existe-t-elle ? Sinon, je ne les utiliserai pas.
6. **Chiffres officiels** (79 897 patients, 3ᵉ Prix national, horaires, numéros) : sont-ils à jour ?
