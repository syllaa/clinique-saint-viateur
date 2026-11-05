# Mesures Lighthouse — référence avant refonte

**Date :** 5 novembre 2026 · **Lighthouse :** 12.6.1 (Chrome headless) · **Build :** production (`vite build`, après les correctifs de l'étape 1, sans changement de performance) servi par `vite preview` avec l'API locale.

| Page | Format | Performance | Accessibilité | Bonnes pratiques | SEO | FCP | LCP | TBT | CLS |
|---|---|---|---|---|---|---|---|---|---|
| Accueil `/` | Mobile | 68 | 90 | 96 | 92 | 3,3 s | 4,3 s | 340 ms | 0 |
| Accueil `/` | Desktop | 89 | 94 | 96 | 92 | 0,7 s | 1,5 s | 190 ms | 0,008 |
| Spécialités | Mobile | 85 | 88 | 96 | 92 | 3,0 s | 3,6 s | 0 ms | 0 |
| Spécialités | Desktop | 78 | 93 | 96 | 92 | 1,1 s | 1,1 s | 0 ms | **0,342** |
| Blog | Mobile | 81 | 90 | 96 | 92 | 3,0 s | 4,0 s | 0 ms | 0 |
| Blog | Desktop | 77 | 96 | 96 | 92 | 1,1 s | 1,1 s | 0 ms | **0,374** |

Objectifs de la refonte : LCP < 2,5 s, CLS < 0,05 et INP < 200 ms sur mobile.

## Problèmes relevés (sur les 6 mesures)
- Contraste insuffisant : textes et liens du pied de page.
- Polices Google bloquantes au rendu.
- JavaScript inutilisé et images non dimensionnées (pas de `srcset`).
- `robots.txt` absent (le serveur renvoie la page HTML), favicon absent (erreur 404 en console).
- Ordre des titres non séquentiel (`h4` dans les cartes de contact).
- Gros décalages de mise en page (CLS) sur desktop quand les cartes arrivent après le chargement de l'API.
- Bouton « Urgences » de la navbar sans nom accessible sur mobile (régression de l'étape 1, corrigée à l'étape 2).

## Limites de la mesure
- « Cache des fichiers statiques » et « compression du texte » sont des artefacts de `vite preview` : en production, ils dépendent du serveur web (nginx ou autre), à configurer à l'étape 9.
- Le site est mesuré en local : les temps réels dépendront de l'hébergement et du réseau mobile en Côte d'Ivoire.

---

## Après l'étape 5 (pages internes) — 5 novembre 2026

Même protocole (build de production, `vite preview`, API locale).

| Page | Format | Perf. | Access. | Bonnes prat. | SEO | FCP | LCP | TBT | CLS |
|---|---|---|---|---|---|---|---|---|---|
| Accueil | Mobile | 59 *(68)* | 100 *(90)* | 100 *(96)* | 100 *(92)* | 4,5 s | 5,8 s | 290 ms | 0 |
| Accueil | Desktop | 87 *(89)* | 100 *(94)* | 100 | 100 | 0,7 s | 1,5 s | 160 ms | 0,003 |
| Spécialités | Mobile | 80 *(85)* | 100 *(88)* | 100 | 100 | 3,0 s | 4,1 s | 30 ms | 0 |
| Spécialités | Desktop | 96 *(78)* | 100 *(93)* | 100 | 100 | 0,8 s | 1,2 s | 0 ms | **0** *(0,342)* |
| Blog | Mobile | 80 *(81)* | 100 *(90)* | 100 | 100 | 3,1 s | 4,0 s | 0 ms | 0 |
| Blog | Desktop | 97 *(77)* | 100 *(96)* | 100 | 100 | 0,7 s | 1,1 s | 0 ms | **0** *(0,374)* |

*Entre parenthèses : valeur de référence avant refonte.*

**Reste à traiter (étape 9)** : la performance de l'accueil sur mobile a baissé avec la refonte animée (LCP 5,8 s, contre 4,3 s avant). Pistes : chargement différé des sections situées sous la ligne de flottaison, préchargement de l'image du hero, polices hébergées localement, allègement du CSS de l'accueil.
