import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

// Routes
import authRoutes from './modules/auth'
import postRoutes from './modules/posts'
import categoryRoutes from './modules/categories'
import commentRoutes from './modules/comments'
import subscriptionRoutes from './modules/subscription'

// Views
const Home = () => import('@/views/HomeView.vue')
const NotFound = () => import('@/views/NotFoundView.vue')

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
    meta: { title: 'Главная' }
  },

  ...authRoutes,
  ...postRoutes,
  ...categoryRoutes,
  ...commentRoutes,
  ...subscriptionRoutes,

  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: NotFound,
    meta: { title: 'Страница не найдена' }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) return savedPosition
    if (to.hash) {
      return { el: to.hash, behavior: 'smooth' }
    }
    return { top: 0 }
  }
})

/* ---------------------------
   SAFE INIT FLAG (ВАЖНО)
----------------------------*/
let authInitialized = false

/* ---------------------------
   BEFORE EACH
----------------------------*/
router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore()

  // Инициализация auth ТОЛЬКО 1 РАЗ
  if (!authInitialized) {
    authInitialized = true
    try {
      await authStore.initializeAuth()
    } catch (e) {
      console.error('Auth init error:', e)
    }
  }

  // title
  document.title = to.meta.title
    ? `${to.meta.title} | News Site`
    : 'News Site'

  // защита auth routes
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    return next({
      name: 'Login',
      query: { redirect: to.fullPath }
    })
  }

  // защита guest routes
  if (to.meta.requiresGuest && authStore.isAuthenticated) {
    return next({ name: 'Home' })
  }

  next()
})

/* ---------------------------
   AFTER EACH
----------------------------*/
router.afterEach((to, from) => {
  if (import.meta.env.DEV) {
    console.log(`→ ${from.path} -> ${to.path}`)
  }
})

/* ---------------------------
   ERROR HANDLER (SAFE)
----------------------------*/
router.onError((error) => {
  console.error('Router error:', error)
})

export default router