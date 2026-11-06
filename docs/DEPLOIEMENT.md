# Déploiement — Clinique Médicale Saint Viateur

**Pour qui :** la personne qui met le site en ligne et l'administre ensuite. Connaissances supposées : un serveur Linux avec Docker, un nom de domaine, un accès SSH.

---

## 1. Ce qui est déployé

| Service | Image | Rôle | Exposé |
|---|---|---|---|
| `web` | `frontend/Dockerfile` (nginx) | Sert le site, relaie `/api`, `/auth`, `/uploads`, `/sitemap.xml`, `/robots.txt` vers l'API, ajoute les en-têtes de sécurité | Oui, sur `WEB_PORT` (8080 par défaut) |
| `api` | `backend/Dockerfile` (FastAPI) | API, administration, sauvegardes automatiques ; applique les migrations au démarrage | Non (réseau interne) |
| `db` | `mariadb:11.4` | Base de données | Non (réseau interne) |

Volumes persistants : `db-data` (base), `uploads` (images, vidéos, CV), `backups` (sauvegardes SQL).

---

## 2. Première mise en ligne

```bash
git clone <dépôt> clinique-saint && cd clinique-saint
cp .env.example .env
nano .env          # remplir TOUTES les valeurs (voir commentaires dans le fichier)
docker compose up -d --build
docker compose logs -f api   # attendre « Application startup complete »
```

Puis :
1. **HTTPS (obligatoire).** Placer un reverse proxy avec certificat devant `WEB_PORT` (Caddy, nginx + Certbot, Traefik…). Exemple Caddy :
   ```
   www.exemple-clinique.ci {
       reverse_proxy 127.0.0.1:8080
   }
   ```
   Une fois le site uniquement en HTTPS, décommenter la ligne `Strict-Transport-Security` dans `frontend/nginx.conf` puis `docker compose up -d --build web`.
2. **Compte administrateur.** Ouvrir le site, appuyer sur `Ctrl+Maj+A`, se connecter avec `ADMIN_USERNAME` / `ADMIN_PASSWORD`, puis **Administration → Sécurité** pour choisir un mot de passe personnel.
3. **Référencement.** Déclarer `https://<domaine>/sitemap.xml` dans Google Search Console.

---

## 3. Reprendre les données existantes (base locale WAMP)

Sur le poste actuel :
```bash
cd backend
./clisvenv/Scripts/python.exe -c "from app.backups.service import create_backup; print(create_backup())"
# le fichier est dans backend/backups/backup_AAAAMMJJ_HHMMSS.sql
```
Copier aussi le dossier `backend/uploads/` (images, vidéos, CV).

Sur le serveur, **avant** le premier `docker compose up` de l'API (base vide) :
```bash
docker compose up -d db
docker compose exec -T db sh -c 'mariadb -u"$MARIADB_USER" -p"$MARIADB_PASSWORD" "$MARIADB_DATABASE"' < backup_AAAAMMJJ_HHMMSS.sql
docker compose up -d --build
# fichiers envoyés : copier dans le volume uploads
docker compose cp ./uploads/. api:/app/uploads/
```
La sauvegarde contient la table `alembic_version` : les migrations repartent de la bonne version.

---

## 4. Mettre à jour le site

```bash
git pull
docker compose up -d --build     # les migrations s'appliquent seules au démarrage de l'API
```
Avant une mise à jour importante : **Administration → Sauvegardes → Sauvegarder maintenant**, puis télécharger le fichier.

---

## 5. Sauvegardes

- Automatiques toutes les 24 h, conservées `BACKUP_RETENTION_DAYS` jours (volume `backups`).
- Elles restent **sur le même serveur que la base** : copier régulièrement les fichiers ailleurs (téléchargement depuis l'administration, ou `docker compose cp api:/app/backups ./copie-backups`).
- Restaurer : même commande que la reprise de données (section 3).

---

## 6. Sécurité en place

| Mesure | Où |
|---|---|
| En-têtes CSP, `X-Content-Type-Options`, `Referrer-Policy`, `X-Frame-Options`, `Permissions-Policy` (+ HSTS à activer) | `frontend/nginx.conf` |
| Limitation des tentatives (connexion, contact, candidatures, réactions) | `backend/app/rate_limit.py` |
| Adresse réelle des visiteurs transmise par nginx (`--proxy-headers`) | `backend/docker-entrypoint.sh` |
| Image API sans `.env`, venv, CV ni sauvegardes (`.dockerignore`), utilisateur non privilégié | `backend/Dockerfile` |
| Base et API non exposées sur Internet | `docker-compose.yml` |

**Limite connue :** les compteurs de tentatives sont en mémoire du processus API. Avec un seul conteneur `api` (configuration fournie) c'est exact ; si l'API est un jour dupliquée, prévoir un stockage partagé (Redis).

---

## 7. Variables d'environnement

Voir les commentaires de `.env.example` (racine). Points d'attention :
- `SITE_URL` sert aux aperçus de partage, aux liens canoniques et au sitemap : **mettre le vrai domaine** avant le build.
- `ADMIN_PASSWORD` n'est utilisé qu'à la création du premier compte, sur une base vide. Le modifier ensuite dans `.env` **ne change pas** le mot de passe existant : passer par Administration → Sécurité.

---

## 8. Développement local (sans Docker)

```bash
# API
cd backend
./clisvenv/Scripts/Activate.ps1          # ou source clisvenv/bin/activate
pip install -r requirements-dev.txt
alembic upgrade head
uvicorn app.main:app --reload --port 8000

# Site
cd frontend
npm install
npm run dev                               # http://localhost:5173
```
Prérequis : MySQL/MariaDB démarré (WAMP) avec les accès de `backend/.env`.
