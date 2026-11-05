# Vidéos d'ambiance à produire — Clinique Médicale Saint Viateur

**Pour qui :** la personne qui tournera, fera générer ou montera les vidéos du site, et la direction de la clinique qui les validera.
**État :** le site est prêt à les recevoir. Tant qu'une vidéo n'est pas fournie, l'emplacement affiche une image ou un fond animé : rien n'est cassé ni vide.

---

## 1. Règles à respecter (non négociables)

1. **Aucune fausse image documentaire.** Une vidéo générée par IA ne doit jamais montrer la façade, les locaux, l'ambulance, les médecins ou les patients « de la clinique ». Le public la prendrait pour une image réelle. Pour montrer la vraie clinique : **tournage réel** (option A).
2. **Pas de patients, pas de visages identifiables sans autorisation écrite.** Pour un tournage réel, faire signer une autorisation de droit à l'image à chaque membre du personnel visible. Aucun patient à l'image.
3. **Aucune information indispensable dans la vidéo.** Elle est décorative : coupée en mode « animations réduites », en mode économie de données, et invisible pour les lecteurs d'écran. Tout le texte important reste dans la page.
4. **Pas de clignotement** (plus de 3 flashs par seconde), pas de gyrophare stroboscopique, pas de sang, pas de scène de soins invasifs.
5. **Sans son, sans texte incrusté, sans logo.** Le site superpose son propre texte.

---

## 2. Où déposer les fichiers

Dossier : `frontend/src/assets/media/`. Les fichiers sont détectés automatiquement au build (voir `LISEZMOI.md` dans ce dossier).

| Emplacement | Fichiers | Image affichée sans vidéo |
|---|---|---|
| Hero de l'accueil | `hero.webm`, `hero.mp4`, `hero-mobile.webm`, `hero-mobile.mp4` | Photo réelle de l'ambulance devant la clinique |
| Section « Notre histoire » | `histoire.webm`, `histoire.mp4` | Aucune (fond bordeaux), la vidéo est un bonus |
| Bandeau « Urgences 24h/24 » | `urgences.webm`, `urgences.mp4` | Fond dégradé + tracé ECG animé |
| Page « Nous rejoindre » | `recrutement.webm`, `recrutement.mp4` | Photo réelle de l'équipe |

Les spécialités pourront recevoir leur propre vidéo depuis l'administration (étape 7 du projet).

---

## 3. Fiches par emplacement

### 3.1 Hero de l'accueil — « Une clinique qui ne dort jamais »

| | |
|---|---|
| **Rôle** | Donner vie au premier écran, derrière le titre, à 28 % d'opacité sous un voile bordeaux |
| **Durée** | 8 à 10 s, boucle parfaite (le début et la fin se raccordent) |
| **Formats** | 16:9 (1920×1080 source → 1280×720 livré) **et** 9:16 (720×1280) pour mobile |
| **Caméra** | Travelling avant très lent (dolly) ou plan fixe avec léger mouvement ; pas de mouvement brusque |
| **Lumière** | Heure bleue / début de nuit ; lumières chaudes qui s'allument |
| **Couleurs** | Tons chauds, ambre et bordeaux ; peu saturés (la vidéo est assombrie et désaturée par le site) |
| **Composition** | Laisser le **tiers gauche calme et sombre** : le titre s'y superpose |

**Option A — Tournage réel (recommandé).** Façade de la clinique, route d'Akouédo, filmée au crépuscule sur trépied. Accélérer (timelapse) le passage du jour à la nuit et l'éclairage des fenêtres. Facultatif : l'ambulance qui se gare, sans plaque lisible ni personne identifiable. Une minute de rushes suffit.

**Option B — Génération IA (abstraite, sans représenter la clinique)**

> *Prompt (Veo / Runway / Kling / Sora — en anglais, ils y répondent mieux) :*
> Slow cinematic dolly through soft out-of-focus warm city lights at dusk, deep burgundy and amber bokeh drifting gently, a faint thin red line of light pulsing like a heartbeat across the frame, calm, premium, hopeful mood, no people, no buildings in focus, no text, no logos, shallow depth of field, 24fps, seamless loop, dark left third of the frame for text overlay.
>
> *À éviter (negative prompt) :* people, faces, hospital building, ambulance, text, logo, watermark, flashing lights, fast motion, blood.

### 3.2 Section « Notre histoire » — gestes et lumière

| | |
|---|---|
| **Rôle** | Fond texturé très discret (16 % d'opacité, rendu en luminance) derrière le récit en 4 chapitres |
| **Durée** | 6 s, boucle |
| **Format** | 16:9, 1280×720 livré |
| **Caméra** | Gros plans, mouvements lents, mise au point douce |
| **Lumière** | Lumière naturelle douce, fenêtre |

**Option A — Tournage réel.** Mains du personnel (sans visage) qui préparent un plateau de soins, un stéthoscope posé sur un bureau, l'automate du laboratoire en fonctionnement, une porte qui s'ouvre sur un couloir lumineux.

**Option B — Génération IA**

> Extreme close-up of anonymous hands in light blue medical gloves gently arranging a stethoscope and a clipboard on a white desk, soft window light, slow motion, warm and reassuring atmosphere, shallow depth of field, no faces, no patients, no text, seamless 6-second loop.
>
> *À éviter :* faces, patients, needles, blood, syringes, text, logo.

### 3.3 Bandeau « Urgences 24h/24 » — vigilance

| | |
|---|---|
| **Rôle** | Fond du bandeau qui met en avant le numéro d'urgence (30 % d'opacité, désaturé) |
| **Durée** | 5 s, boucle |
| **Format** | 16:9, 1280×720 livré |
| **Ambiance** | Très sombre, calme et vigilante, **pas anxiogène** |

**Option A — Tournage réel.** De nuit, reflets flous et lents d'un gyrophare sur un mur ou une vitre de la clinique (pas de flash direct), ou couloir des urgences vide et éclairé, filmé en flou volontaire.

**Option B — Génération IA**

> Very dark abstract scene, slow soft red and white light reflections sweeping across a blurred glossy surface at night, like a distant emergency beacon seen through frosted glass, gentle and calm rhythm, no strobe, no vehicles, no people, no text, cinematic, seamless 5-second loop.
>
> *À éviter :* strobe, flashing faster than once per second, vehicles, people, blood, text.

### 3.4 Page « Nous rejoindre » — une équipe

| | |
|---|---|
| **Rôle** | Remplace la photo d'équipe en tête des offres d'emploi |
| **Durée** | 8 s, boucle |
| **Format** | 16:10 (1280×800 livré) |

**Option A — Tournage réel (fortement recommandé).** C'est la vraie équipe qui donne envie de la rejoindre : échange souriant au comptoir d'accueil, technicien au laboratoire, équipe réunie qui se tourne vers la caméra. **Uniquement des membres du personnel volontaires, avec autorisation écrite.**

**Option B — Génération IA (sans visages)**

> Warm, softly lit medical team workspace seen out of focus, silhouettes of caregivers in white coats walking and collaborating in the background, hands passing a tablet, natural light, hopeful and professional mood, faces not distinguishable, no text, seamless 8-second loop.
>
> *À éviter :* recognizable faces, patients, text, logo.

---

## 4. Encodage (commandes vérifiées avec FFmpeg 9)

Objectif : **2,5 Mo maximum par fichier**, sans piste audio, 24 images/s. Remplacer `source.mp4` par le fichier monté.

```bash
# 1. Version bureau WebM (VP9) — le site la préfère
ffmpeg -i source.mp4 -t 10 -an -vf "scale=1280:-2,fps=24" \
  -c:v libvpx-vp9 -b:v 0 -crf 42 -row-mt 1 -deadline good -cpu-used 2 hero.webm

# 2. Version bureau MP4 (H.264) — repli pour Safari et anciens navigateurs
ffmpeg -i source.mp4 -t 10 -an -vf "scale=1280:-2,fps=24" \
  -c:v libx264 -crf 28 -preset slow -profile:v high -pix_fmt yuv420p -movflags +faststart hero.mp4

# 3. Versions mobiles verticales 9:16 (recadrage au centre)
ffmpeg -i source.mp4 -t 10 -an -vf "crop=ih*9/16:ih,scale=720:-2,fps=24" \
  -c:v libvpx-vp9 -b:v 0 -crf 44 -row-mt 1 -deadline good -cpu-used 2 hero-mobile.webm
ffmpeg -i source.mp4 -t 10 -an -vf "crop=ih*9/16:ih,scale=720:-2,fps=24" \
  -c:v libx264 -crf 30 -preset slow -pix_fmt yuv420p -movflags +faststart hero-mobile.mp4

# 4. Boucle parfaite : fondu enchaîné de la fin sur le début (10 s de rushes,
#    fondu de 1 s → boucle de 9 s dont la dernière image retombe sur la première)
ffmpeg -i source.mp4 -filter_complex \
  "[0:v]trim=0:10,setpts=PTS-STARTPTS[v];[v]split[a][b];[a]trim=1:10,setpts=PTS-STARTPTS[main];[b]trim=0:1,setpts=PTS-STARTPTS[head];[main][head]xfade=transition=fade:duration=1:offset=8[out]" \
  -map "[out]" -an -c:v libx264 -crf 18 boucle.mp4
# puis encoder boucle.mp4 avec les commandes 1 à 3.

# Vérifier la taille
ls -lh hero.*
```

Si un fichier dépasse 2,5 Mo, augmenter `-crf` de 2 en 2 (qualité un peu plus basse, fichier plus léger) ou réduire `-t`.

---

## 5. Validation avant mise en ligne

- [ ] Option A : autorisations de droit à l'image signées et archivées.
- [ ] Option B : aucune ressemblance avec la clinique réelle, ni visage identifiable.
- [ ] Pas de flash rapide (test : regarder la vidéo en plein écran, dans le noir).
- [ ] Chaque fichier ≤ 2,5 Mo, sans son.
- [ ] La boucle ne saute pas visiblement.
- [ ] Vérifié sur le site : ordinateur, mobile, mode sombre, et bouton « Réduire les animations » (la vidéo doit disparaître au profit de l'image).
