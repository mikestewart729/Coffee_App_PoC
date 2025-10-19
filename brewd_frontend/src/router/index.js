import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/stores/user'
import SignUpView from '../views/SignUpView.vue'
import LoginView from '../views/LoginView.vue'
import NearbyShopsView from '../views/NearbyShopsView.vue'
import RepeatBrewsView from '../views/RepeatBrewsView.vue'
import SearchView from '../views/SearchView.vue'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'nearbyshops',
      component: NearbyShopsView,
      meta: { requiresAuth: true },
    },
    {
      path: '/signup',
      name: 'signup',
      component: SignUpView,
      meta: { guestOnly: true },
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView,
      meta: { guestOnly: true },
    },
    {
      path: '/repeatbrews',
      name: 'repeatbrews',
      component: RepeatBrewsView,
      meta: { requiresAuth: true },
    },
    {
      path: '/search',
      name: 'search',
      component: SearchView,
      meta: { requiresAuth: true },
    },
  ],
})

// Navigation guard to protect routes
router.beforeEach((to, from, next) => {
  const userStore = useUserStore()

  // Redirect to Login page if route requires auth and user not authenticated
  if (to.meta.requiresAuth && !userStore.isAuthenticated) {
    next({ name: 'login' })
  }
  // Redirect to Nearby Shops if route is guest only and user is authenticated
  else if (to.meta.guestOnly && userStore.isAuthenticated) {
    next({ name: 'nearbyshops' })
  }
  // Otherwise, proceed as normal
  else {
    next()
  }
})

export default router
