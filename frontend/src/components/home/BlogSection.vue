<script setup lang="ts">
import BlogGrid from "@/components/blog/BlogGrid.vue";
</script>

<template>
  <section id="blog" class="section blog-section" aria-labelledby="blog-title">
    <div class="section-inner">
      <p v-reveal class="section-kicker">Notre blog médical</p>
      <h2 id="blog-title" v-reveal="'words'" class="section-title d1">Actualités & Conseils santé</h2>
      <p v-reveal class="section-lead d2">
        Restez informé des actualités de la clinique, des conseils de prévention et des nouvelles médicales utiles
        pour votre santé et celle de votre famille.
      </p>
      <BlogGrid />
      <div class="section-more">
        <RouterLink to="/blog" class="btn-outline">Voir tous les articles →</RouterLink>
      </div>
    </div>
  </section>
</template>

<style scoped>
.blog-section {
  background: var(--bg-alt);
}
</style>
