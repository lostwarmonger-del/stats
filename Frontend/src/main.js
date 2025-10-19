import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { createRouter, createWebHistory } from 'vue-router'
import Toast from 'vue-toastification'
import 'vue-toastification/dist/index.css'
import { library } from '@fortawesome/fontawesome-svg-core'
import { fas } from '@fortawesome/free-solid-svg-icons'
import { far } from '@fortawesome/free-regular-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import axios from 'axios'
import './style.css'
import App from './App.vue'

// Configure axios base URL
axios.defaults.baseURL = 'http://localhost:8001'

// Import components
import LoginForm from './components/LoginForm.vue'
import Dashboard from './components/Dashboard.vue'
import Program404640723 from './components/Program404640723.vue'
import Program404640725 from './components/Program404640725.vue'
import Program404640758 from './components/Program404640758.vue'
import Program403640724 from './components/Program403640724.vue'
import Program403640722 from './components/Program403640722.vue'
import ProgramAbulFazl from './components/ProgramAbulFazl.vue'
import ProgramTharAllah from './components/ProgramTharAllah.vue'
import ProgramQamarBaniHashim from './components/ProgramQamarBaniHashim.vue'
import ProgramBaqiyatAllah from './components/ProgramBaqiyatAllah.vue'
import CommissionPrevention from './components/CommissionPrevention.vue'
import MonitoringDashboard from './components/MonitoringDashboard.vue'
import UserManagement from './components/UserManagement.vue'

// Add icons to library
library.add(fas, far)

// Router configuration
const routes = [
  { path: '/', redirect: '/login' },
  { path: '/login', component: LoginForm },
  { path: '/dashboard', component: Dashboard, meta: { requiresAuth: true } },
  { path: '/program-404640723', component: Program404640723, meta: { requiresAuth: true } },
  { path: '/program-404640725', component: Program404640725, meta: { requiresAuth: true } },
  { path: '/program-404640758', component: Program404640758, meta: { requiresAuth: true } },
  { path: '/program-403640724', component: Program403640724, meta: { requiresAuth: true } },
  { path: '/program-403640722', component: Program403640722, meta: { requiresAuth: true } },
  { path: '/program-abul-fazl', component: ProgramAbulFazl, meta: { requiresAuth: true } },
  { path: '/program-thar-allah', component: ProgramTharAllah, meta: { requiresAuth: true } },
  { path: '/program-qamar-bani-hashim', component: ProgramQamarBaniHashim, meta: { requiresAuth: true } },
  { path: '/program-baqiyat-allah', component: ProgramBaqiyatAllah, meta: { requiresAuth: true } },
  { path: '/commission-prevention', component: CommissionPrevention, meta: { requiresAuth: true } },
  { 
    path: '/monitoring-dashboard', 
    component: MonitoringDashboard,
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  { 
    path: '/user-management', 
    component: UserManagement,
    meta: { requiresAuth: true, requiresAdmin: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Route guards
router.beforeEach(async (to, from, next) => {
  // Import auth store
  const { useAuthStore } = await import('./stores/auth')
  const authStore = useAuthStore()
  
  // If we have a token but haven't checked auth yet, check it first
  if (authStore.token && !authStore.isAuthenticated) {
    await authStore.checkAuth()
  }
  
  // Check if route requires authentication
  if (to.meta.requiresAuth) {
    if (!authStore.isAuthenticated) {
      // If not authenticated and trying to access protected route, redirect to login
      next('/login')
      return
    }
    
    // Check if route requires admin access
    if (to.meta.requiresAdmin) {
      if (authStore.user?.role !== 'admin') {
        // Redirect to dashboard if not admin
        next('/dashboard')
        return
      }
    }
  } else {
    // If authenticated and trying to access login page, redirect to dashboard
    if (to.path === '/login' && authStore.isAuthenticated) {
      next('/dashboard')
      return
    }
  }
  
  next()
})

// Toast options
const toastOptions = {
  position: 'top-right',
  timeout: 3000,
  closeOnClick: true,
  pauseOnFocusLoss: true,
  pauseOnHover: true,
  draggable: true,
  draggablePercent: 0.6,
  showCloseButtonOnHover: false,
  hideProgressBar: false,
  closeButton: 'button',
  icon: true,
  rtl: true
}

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)
app.use(router)
app.use(Toast, toastOptions)
app.component('font-awesome-icon', FontAwesomeIcon)

app.mount('#app')