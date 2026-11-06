<script setup lang="ts">
import { defineAsyncComponent, onMounted } from "vue";

import HeroSection from "@/components/home/HeroSection.vue";
import InfoStrip from "@/components/home/InfoStrip.vue";
import { applySeo, clinicJsonLd } from "@/composables/useHead";

// Each section owns its data, markup, styles and animations
// (see components/home/). This page only sets the order.
//
// Only what is visible on arrival (hero + info strip) is in the page's
// initial bundle; every section below the fold is a separate chunk loaded
// right after, so a phone parses and styles far less before first paint.
// No layout shift: those sections sit below the first screen, and <main>
// keeps a full-screen minimum height (ui.css).
const ServicesSection = defineAsyncComponent(() => import("@/components/home/ServicesSection.vue"));
const OffersSection = defineAsyncComponent(() => import("@/components/home/OffersSection.vue"));
const AboutSection = defineAsyncComponent(() => import("@/components/home/AboutSection.vue"));
const GallerySection = defineAsyncComponent(() => import("@/components/home/GallerySection.vue"));
const EmergencyBanner = defineAsyncComponent(() => import("@/components/home/EmergencyBanner.vue"));
const BlogSection = defineAsyncComponent(() => import("@/components/home/BlogSection.vue"));
const TestimonialsSection = defineAsyncComponent(() => import("@/components/home/TestimonialsSection.vue"));
const ContactSection = defineAsyncComponent(() => import("@/components/home/ContactSection.vue"));
const MapBanner = defineAsyncComponent(() => import("@/components/home/MapBanner.vue"));

onMounted(() =>
  applySeo({
    title: "Clinique Médicale Saint Viateur – Riviera Sideci, Cocody, Abidjan",
    description:
      "Établissement médical privé à Cocody, Abidjan : urgences et réanimation 24h/24, 7j/7, consultations, laboratoire, imagerie, maternité. Appelez le 27 22 59 04 17.",
    jsonLd: clinicJsonLd(),
  }),
);
</script>

<template>
  <HeroSection />
  <InfoStrip />
  <ServicesSection />
  <OffersSection />
  <AboutSection />
  <GallerySection />
  <EmergencyBanner />
  <BlogSection />
  <TestimonialsSection />
  <ContactSection />
  <MapBanner />
</template>
