# Rapport final — Refonte du site de la Clinique Médicale Saint Viateur

**Période :** 5 et 6 novembre 2026 · **Branche :** `feat/refonte-animee` (11 commits, un par étape) · **Point de départ :** commit `e4193a3`

**Pour qui :** la direction de la clinique (sections 1, 2 et 7) et l'équipe technique qui reprend le projet (toutes les sections).

---

## 1. En bref

Le site est passé d'une vitrine statique à une expérience animée, plus sûre et plus rapide sur ordinateur, **sans rien reconstruire** : mêmes technologies (Vue 3, FastAPI, MySQL), mêmes adresses de pages, mêmes données, administration préservée.

| | Avant | Après |
|---|---|---|
| Navigation sur téléphone | Aucun menu sous 980 px | Menu complet, accessible au clavier |
| Accessibilité (Lighthouse) | 88 – 96 | **100** sur toutes les pages mesurées¹ |
| SEO (Lighthouse) | 91 – 92 | **100** + sitemap, données structurées, aperçus de partage |
| Stabilité de la mise en page (CLS) | jusqu'à 0,37 | **0** partout |
| Performance desktop | 77 – 89 | **91 – 99** |
| Performance accueil mobile | 68 | **74 – 84** |
| Premier affichage sur mobile | 3,3 s | **1,4 s** |
| Tests automatisés (backend) | 62 | **83**, tous au vert |
| Mot de passe admin | `admin123`, non modifiable | Modifiable depuis l'admin, mots de passe faibles refusés |

¹ Faux positif connu sur la page Offres (contraste mesuré pendant le fondu d'apparition des cartes).

---

## 2. Ce qui a changé pour les visiteurs

- **Accueil** : courte intro de marque (ordinateur, une fois par visite), hero avec photo réelle, titre qui apparaît mot par mot, badge « ouvert / fermé » à l'heure d'Abidjan, numéro d'urgence cliquable qui « respire ». Récit « Notre histoire » en 4 chapitres avec ligne ECG dessinée au défilement, **galerie de l'établissement** (9 vraies photos), **bandeau Urgences 24h/24**, horaires avec le jour courant surligné.
- **Pages internes** : en-tête commun animé, transitions entre pages, filtres à pastille glissante, chargements sans saut, barre de lecture des articles, page 404 « moniteur cardiaque ».
- **Accessibilité** : bouton « Réduire les animations » (pied de page) et respect du réglage système ; navigation clavier complète ; mode sombre lisible.
- **Formulaires** : messages d'erreur clairs (avant : aucun retour en cas d'échec), protection anti-spam invisible.

## 3. Ce qui a changé pour l'administration

- **Sécurité → Changer mon mot de passe** (avec alerte tant que le mot de passe par défaut est utilisé).
- **Vidéo de couverture par spécialité** : envoi, aperçu, remplacement, retrait.
- Session qui se renouvelle seule (plus de déconnexion au bout de 30 min).
- Éditeur d'articles mis à jour (TipTap 3.32) et vérifié.

---

## 4. Sécurité

| Problème trouvé | Correction |
|---|---|
| Mot de passe admin `admin123`, aucun moyen de le changer | Écran de changement, règles de robustesse, avertissement au démarrage de l'API |
| Aucune limite de tentatives (connexion, formulaires) | Limitation par adresse IP (`backend/app/rate_limit.py`) |
| Spam possible sur contact et candidatures | Champ piège invisible |
| Documents sensibles dans le code (sauvegarde SQL, comptes, habilitations…) | Déplacés hors du projet (`Documents\clinique-archives`), jamais entrés dans l'historique Git |
| Pas de versionnement exploitable (dépôt = dossier utilisateur entier) | Dépôt dédié au projet, historique complet |
| Une image Docker aurait embarqué `.env`, venv et CV | `.dockerignore`, utilisateur non privilégié |
| Failles connues dans Vue, Axios, TipTap, ProseMirror | Mises à jour (correctifs compatibles) |
| Aucun en-tête de sécurité HTTP | CSP, nosniff, Referrer-Policy, X-Frame-Options, Permissions-Policy (+ HSTS prêt) dans `frontend/nginx.conf` |

## 5. Détail technique

**Nouveaux modules** : `frontend/src/motion/` (système d'animation), `components/home/` (10 sections), `components/common/` (PageHeader, FilterPills, SkeletonGrid, AmbientVideo, ReadingProgress, LoadError, HoneypotField), `backend/app/rate_limit.py`, `backend/app/seo/`.

**Bilan des fichiers** : 58 créés, 72 modifiés (8 480 lignes ajoutées, 2 282 retirées). `HomeView.vue` est passé de 1 303 à 48 lignes.

**Dépendances ajoutées** (versions exactes) : `gsap 3.15.0`, `lenis 1.3.27`, `@fontsource/cormorant-garamond 5.3.0`, `@fontsource-variable/dm-sans 5.3.0`. Mises à jour : `vue 3.5.45`, `axios 1.21.0`, `@tiptap/* 3.32.0`. Backend : versions figées dans `requirements.txt`, outils de test dans `requirements-dev.txt`.

**Base de données** : migration `0009` (colonne facultative `specialties.cover_video_url`), réversible, appliquée et testée en aller-retour sur la base locale (aucune donnée perdue).

**Tests** : 83 tests backend (19 sécurité/vidéo, 2 SEO ajoutés). Le frontend n'a pas de tests automatisés : chaque étape a été vérifiée par build TypeScript, Lighthouse et parcours scriptés dans Chrome (captures d'écran à l'appui).

**Mesures détaillées** : [docs/mesures/lighthouse-reference.md](mesures/lighthouse-reference.md).

---

## 6. Incidents survenus pendant le projet

| Incident | Impact | Suite |
|---|---|---|
| La sauvegarde faite avant la migration a déclenché la rétention de 14 jours, qui a supprimé les 2 sauvegardes d'août | Aucun : contenu identique à la sauvegarde du jour (vérifié) | Copie d'août conservée dans `Documents\clinique-archives` |
| L'API locale est restée indisponible quelques minutes (rechargée avant la migration) | Poste de développement uniquement | Relancée, plus d'impact |
| MySQL et Docker Desktop arrêtés après un redémarrage du poste | Mesures faussées temporairement | Mesures refaites base démarrée |

---

## 7. Ce qui reste à faire

### Décisions de la clinique
1. **Changer le mot de passe admin** (toujours `admin123` en base) : Administration → Sécurité.
2. **Témoignages** : confirmer que les 4 avis affichés sont authentiques et autorisés, sinon les retirer.
3. **Photos d'enfants et de nouveau-nés** : non utilisées par la refonte faute d'autorisation parentale confirmée. Attention : certaines **spécialités en base** (Pédiatrie, Gynécologie) en affichent déjà, envoyées depuis l'admin.
4. **Chiffres officiels** à revalider (79 897 patients, 3ᵉ Prix national, horaires, numéros).
5. **Vidéos d'ambiance** à produire : brief, prompts et commandes d'encodage dans [docs/medias-a-generer.md](medias-a-generer.md). Le site fonctionne parfaitement sans.

### Avant la mise en ligne
6. Renseigner le vrai domaine dans `.env` (`SITE_URL`) puis suivre [docs/DEPLOIEMENT.md](DEPLOIEMENT.md) (HTTPS obligatoire).
7. Prévoir une **copie externe des sauvegardes** (elles restent sur le même serveur que la base).

### Limites techniques connues
8. **Aperçu de partage par page** : sans rendu serveur, un lien partagé sur WhatsApp/Facebook affiche l'aperçu général de la clinique (Google, lui, voit chaque page). Un pré-rendu au build réglerait ce point.
9. **Vite 5** : 5 alertes de sécurité restantes, limitées aux outils de développement (jamais livrées aux visiteurs) ; corriger demande une migration majeure vers Vite 8.
10. **Images Docker non construites** sur ce poste (Docker Desktop arrêté) : la configuration est validée syntaxiquement, à construire une première fois sur le serveur.
11. Fichiers envoyés mais jamais enregistrés (images, vidéos) : restent sur le disque, comme avant la refonte.
12. Sur ce poste, le port 8000 a refusé ponctuellement l'API locale le 6 novembre (conflit avec un autre service Windows) ; sans effet en production.
