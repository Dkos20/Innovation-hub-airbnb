import { createRouter, createWebHistory } from 'vue-router'
import Home from '../components/Home.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'Home',
      component: Home
    },
    {
      path: '/Login',
      name: 'Login',
      component: () => import('../components/Login.vue')
    },
    {
      path: '/Register',
      name: 'Register',
      component: () => import('../components/Register.vue')
    },
    {
      path: '/About',
      name: 'About',
      component: () => import('../components/About.vue')
    }
  ]
})

export default router
