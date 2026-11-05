import { createRouter, createWebHistory } from "vue-router";

import { useAdminAccess } from "@/composables/useAdminAccess";
import { scrollToHash, scrollToTop } from "@/motion/useLenis";
import { useAuthStore } from "@/stores/auth";

const router = createRouter({
  history: createWebHistory(),
  scrollBehavior(to, _from, savedPosition) {
    if (to.hash) {
      // Waits for the target (sections often render after an API call) and
      // goes through Lenis when smooth scrolling is active.
      scrollToHash(to.hash);
      return false;
    }
    // Back/forward restores where the visitor was.
    if (savedPosition) return savedPosition;
    scrollToTop();
    return { top: 0 };
  },
  routes: [
    {
      path: "/",
      name: "home",
      component: () => import("@/pages/HomeView.vue"),
    },
    {
      path: "/login",
      name: "login",
      component: () => import("@/pages/LoginView.vue"),
      meta: { requiresAdminUnlock: true },
    },
    {
      path: "/specialites",
      name: "specialties",
      component: () => import("@/pages/SpecialtiesListView.vue"),
    },
    {
      path: "/specialites/:slug",
      name: "specialty-detail",
      component: () => import("@/pages/SpecialtyDetailView.vue"),
    },
    {
      path: "/blog",
      name: "blog",
      component: () => import("@/pages/BlogListView.vue"),
    },
    {
      path: "/blog/:slug",
      name: "blog-detail",
      component: () => import("@/pages/ArticleDetailView.vue"),
    },
    {
      path: "/promotions",
      name: "promotions",
      component: () => import("@/pages/PromotionsListView.vue"),
    },
    {
      path: "/nous-rejoindre",
      name: "join-us",
      component: () => import("@/pages/JoinUsView.vue"),
    },
    {
      path: "/nous-rejoindre/offres/:slug",
      name: "job-offer-detail",
      component: () => import("@/pages/JobOfferDetailView.vue"),
    },
    {
      path: "/admin",
      name: "admin",
      component: () => import("@/pages/AdminView.vue"),
      meta: { requiresAdmin: true, requiresAdminUnlock: true },
    },
    {
      path: "/:pathMatch(.*)*",
      name: "not-found",
      component: () => import("@/pages/NotFoundView.vue"),
    },
  ],
});

router.beforeEach((to) => {
  if (to.meta.requiresAdminUnlock) {
    const { unlocked } = useAdminAccess();
    if (!unlocked.value) {
      // Redirect to the 404 route while keeping the attempted URL intact, so
      // it reads as "this page doesn't exist" rather than a suspicious jump
      // to the homepage.
      return { name: "not-found", params: { pathMatch: to.path.substring(1).split("/") }, query: to.query, hash: to.hash };
    }
  }
  if (to.meta.requiresAdmin) {
    const auth = useAuthStore();
    if (!auth.isAuthenticated || !auth.isAdmin) {
      return { name: "login", query: { redirect: to.fullPath } };
    }
  }
  return true;
});

export default router;
