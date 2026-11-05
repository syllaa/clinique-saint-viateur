# Vidéos d'ambiance

Déposez ici les vidéos finales. Elles sont détectées automatiquement au prochain build (`npm run build`) ou au redémarrage de `npm run dev`.

| Emplacement | Fichiers attendus |
|---|---|
| Hero de l'accueil | `hero.webm`, `hero.mp4`, `hero-mobile.webm`, `hero-mobile.mp4` |
| Section « Notre histoire » | `histoire.webm`, `histoire.mp4` (+ `-mobile` facultatif) |
| Bandeau urgences 24h/24 | `urgences.webm`, `urgences.mp4` (+ `-mobile` facultatif) |
| Page « Nous rejoindre » | `recrutement.webm`, `recrutement.mp4` (+ `-mobile` facultatif) |

- Il suffit d'au moins un fichier (idéalement `.webm` + `.mp4`) pour activer un emplacement.
- Tant qu'aucun fichier n'est présent, le site affiche l'image de remplacement prévue : rien n'est cassé.
- Taille cible : 2,5 Mo maximum par fichier. Les commandes d'encodage sont dans `docs/medias-a-generer.md`.
