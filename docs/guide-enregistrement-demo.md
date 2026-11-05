# Guide d'enregistrement — démo du site (rendu final)

Ce guide sert à enregistrer une vidéo de démonstration du site pour la présenter au client.
Une fois la vidéo enregistrée, dépose le fichier dans ce dossier `docs/` (ou donne le chemin
du fichier et il y sera placé).

## Avant de commencer

1. Les deux serveurs doivent tourner en local :
   - Backend : `http://127.0.0.1:8000` (déjà lancé — `uvicorn app.main:app --reload --port 8000`)
   - Frontend : `http://localhost:5173` (déjà lancé — `npm run dev`)
2. Ouvre le site dans le navigateur : **http://localhost:5173**
3. Agrandis la fenêtre du navigateur (idéalement plein écran, ou une résolution 1440×900 minimum)
   pour un rendu propre à l'enregistrement.
4. Ferme les autres onglets/notifications qui pourraient apparaître à l'écran.

## Comment enregistrer (Windows)

**Option rapide — Xbox Game Bar (déjà intégrée à Windows) :**
1. `Win + G` pour ouvrir la barre de jeu
2. Clique sur le bouton d'enregistrement (cercle rouge), ou `Win + Alt + R` pour démarrer/arrêter directement
3. La vidéo est enregistrée automatiquement dans `Vidéos\Captures` (fichier `.mp4`)

**Option alternative — OBS Studio** (si installé) : source "Capture d'écran" ou "Capture de fenêtre"
sur le navigateur, puis Démarrer/Arrêter l'enregistrement.

## Script minuté (~3 min 30)

Parle normalement en naviguant, ou laisse la vidéo muette si tu préfères ajouter une voix off
après coup avec le texte suggéré ci-dessous.

### 1. Accueil — 0:00 à 0:25
- Ouvrir `http://localhost:5173/`
- Laisser le Hero s'afficher (stats animées qui montent : 79K+, 10+)
- Montrer le bandeau "Nous recrutons" qui défile sous la barre de navigation
- *Texte suggéré : "Voici la nouvelle page d'accueil de la Clinique Médicale Saint Viateur."*

### 2. Défiler la page d'accueil — 0:25 à 1:00
- Scroller lentement jusqu'à "Nos spécialités" (grille de cartes)
- Continuer jusqu'au carousel "Nos offres et promotions" — montrer les flèches de défilement
- Continuer jusqu'à "Notre histoire" (photo + statistiques)
- *Texte suggéré : "Toutes les spécialités, les offres du moment et l'histoire de la clinique sont mises en avant dès l'accueil."*

### 3. Détail d'une spécialité — 1:00 à 1:30
- Cliquer sur la carte **Chirurgie**
- Montrer le hero avec photo, le badge "Disponible 24h/24", les sections (interventions, bloc opératoire, parcours patient)
- Descendre jusqu'à la carte "Prendre rendez-vous" (sidebar)
- *Texte suggéré : "Chaque spécialité a sa propre page complète, avec toutes les informations pratiques."*

### 4. Page « Toutes nos offres » — 1:30 à 2:00
- Revenir en haut, cliquer sur **Offres** dans le menu (ou aller sur `/promotions`)
- Montrer la recherche, les filtres par catégorie, le tri
- Cliquer sur une réaction (👍 ❤️ 🔥) sur une carte pour montrer l'interaction en direct
- *Texte suggéré : "Les visiteurs peuvent filtrer les offres et réagir directement, sans créer de compte."*

### 5. Article de blog détaillé — 2:00 à 2:25
- Aller sur **Blog**, ouvrir l'article "Campagne de dépistage cardiovasculaire gratuit"
- Montrer la photo, les informations pratiques, la FAQ dépliable
- *Texte suggéré : "Les articles peuvent inclure des informations pratiques, des listes et une FAQ, pas seulement du texte."*

### 6. Page « Nous rejoindre » — 2:25 à 3:00
- Aller sur **Nous rejoindre**
- Montrer la carte Google Maps et les offres d'emploi
- Cliquer sur une offre (ex : Infirmier(ère) diplômé(e) d'État) pour ouvrir le détail
- *Texte suggéré : "La clinique peut aussi publier ses offres d'emploi et recevoir des candidatures directement en ligne."*

### 7. (Optionnel) Aperçu de l'administration — 3:00 à 3:30
- Aller sur `/login`, se connecter avec le compte admin
- Montrer rapidement le tableau de bord, puis une section (ex : Offres promotionnelles)
- *Texte suggéré : "Toute cette page est gérée par l'équipe de la clinique elle-même, sans avoir besoin de toucher au code."*

## Une fois la vidéo enregistrée

Dépose le fichier `.mp4` dans `docs/` (par exemple `docs/demo-rendu-final.mp4`), ou indique-moi
son emplacement et je le déplacerai ici.
