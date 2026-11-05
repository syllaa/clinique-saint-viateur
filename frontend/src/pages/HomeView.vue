<script setup lang="ts">
import { onMounted } from "vue";

import AboutSection from "@/components/home/AboutSection.vue";
import BlogSection from "@/components/home/BlogSection.vue";
import ContactSection from "@/components/home/ContactSection.vue";
import EmergencyBanner from "@/components/home/EmergencyBanner.vue";
import GallerySection from "@/components/home/GallerySection.vue";
import HeroSection from "@/components/home/HeroSection.vue";
import InfoStrip from "@/components/home/InfoStrip.vue";
import MapBanner from "@/components/home/MapBanner.vue";
import OffersSection from "@/components/home/OffersSection.vue";
import ServicesSection from "@/components/home/ServicesSection.vue";
import TestimonialsSection from "@/components/home/TestimonialsSection.vue";
import { applySeo, clinicJsonLd } from "@/composables/useHead";

// Each section owns its data, markup, styles and animations
// (see components/home/). This page only sets the order.
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
