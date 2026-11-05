<template>
  <footer>
    <div>
      <div class="footer-brand">✚ Clinique Médicale Saint Viateur</div>
      <p style="font-size: 0.74rem; margin-top: 4px">
        Route Akouédo, Riviera Sideci – Cocody, Abidjan · Côte d'Ivoire
      </p>
    </div>
    <div class="footer-links">
      <RouterLink to="/specialites">Spécialités</RouterLink>
      <RouterLink to="/#about">La clinique</RouterLink>
      <RouterLink to="/blog">Actualités</RouterLink>
      <RouterLink to="/#contact">Contact</RouterLink>
      <RouterLink to="/nous-rejoindre">Nous rejoindre</RouterLink>
      <a href="https://www.facebook.com/CliniqueMedicaleSaintViateur/" target="_blank" rel="noopener">Facebook</a>
    </div>
    <p class="footer-copy">© 2026 Clinique Médicale Saint Viateur · Tous droits réservés</p>
  </footer>
</template>

<style scoped>
footer {
  background: #180809;
  color: rgba(255, 255, 255, 0.38);
  padding: 40px 5vw;
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 18px;
}
.footer-brand {
  font-family: "Cormorant Garamond", serif;
  font-size: 0.95rem;
  color: rgba(255, 255, 255, 0.85);
}
.footer-links {
  display: flex;
  gap: 24px;
  flex-wrap: wrap;
}
.footer-links a {
  color: rgba(255, 255, 255, 0.4);
  text-decoration: none;
  font-size: 0.78rem;
  transition: color 0.2s;
}
.footer-links a:hover {
  color: var(--gold-lt);
}
.footer-copy {
  font-size: 0.72rem;
}
</style>
