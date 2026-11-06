# Website image: build the Vue app, then serve it with nginx, which also
# proxies /api, /auth, /uploads, /sitemap.xml and /robots.txt to the API.

# ── 1. Build ──────────────────────────────────────────────
FROM node:22-slim AS build
WORKDIR /app

# Public address of the site, baked into social previews / canonical links.
ARG VITE_SITE_URL
# Empty = the API is reached through this same nginx (same origin, no CORS).
ARG VITE_API_URL=""
ARG VITE_GOOGLE_MAPS_API_KEY=""
ENV VITE_SITE_URL=$VITE_SITE_URL \
    VITE_API_URL=$VITE_API_URL \
    VITE_GOOGLE_MAPS_API_KEY=$VITE_GOOGLE_MAPS_API_KEY

COPY package.json package-lock.json ./
RUN npm ci

COPY . .
RUN test -n "$VITE_SITE_URL" || (echo "VITE_SITE_URL est requis (adresse publique du site)" && exit 1)
RUN npm run build

# ── 2. Serve ──────────────────────────────────────────────
FROM nginx:1.27-alpine
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
