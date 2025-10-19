<template>
  <!-- Sidebar -->
  <aside 
    :class="[
      'fixed right-0 top-0 h-full w-64 bg-gradient-to-b from-blue-600 to-blue-800 transform transition-transform duration-300 ease-in-out z-50 flex flex-col',
      sidebarOpen ? 'translate-x-0' : 'translate-x-full'
    ]"
  >
    <!-- Sidebar Header -->
    <div class="flex items-center p-6 border-b border-white/20">
      <div class="flex items-center space-x-3 space-x-reverse">
        <div class="w-10 h-10 bg-yellow-500 rounded-full flex items-center justify-center">
          <font-awesome-icon icon="fas fa-crown" class="text-white text-lg" />
        </div>
        <div>
          <h2 class="text-white font-bold text-lg">سیستم مدیریت</h2>
          <p class="text-white/60 text-xs">پنل مدیریت پیشرفته</p>
        </div>
      </div>
    </div>

    <!-- Scrollable Navigation Content -->
    <div class="flex-1 overflow-y-auto overflow-x-hidden scrollbar-hide">
      <!-- Main Navigation -->
      <nav class="mt-6 px-4">
        <ul class="space-y-2">
          <!-- Primary Navigation -->
          <li>
            <router-link 
              to="/dashboard" 
              class="flex items-center space-x-3 space-x-reverse px-4 py-3 text-white/80 hover:text-white hover:bg-white/10 rounded-lg transition-all duration-200 group"
              active-class="bg-white/20 text-white"
            >
              <font-awesome-icon icon="fas fa-home" class="text-lg transition-transform" />
              <span>داشبورد</span>
            </router-link>
          </li>
          
          <li v-if="canAccessMonitoring">
            <router-link 
              to="/monitoring-dashboard" 
              class="flex items-center space-x-3 space-x-reverse px-4 py-3 text-white/80 hover:text-white hover:bg-white/10 rounded-lg transition-all duration-200 group"
              active-class="bg-white/20 text-white"
            >
              <font-awesome-icon icon="fas fa-chart-line" class="text-lg transition-transform" />
              <span>داشبورد مانیتورینگ و استخراج داده</span>
            </router-link>
          </li>
          
          <li v-if="canAccessUserManagement">
            <router-link 
              to="/user-management" 
              class="flex items-center space-x-3 space-x-reverse px-4 py-3 text-white/80 hover:text-white hover:bg-white/10 rounded-lg transition-all duration-200 group"
              active-class="bg-white/20 text-white"
            >
              <font-awesome-icon icon="fas fa-users" class="text-lg transition-transform" />
              <span>مدیریت کاربران</span>
            </router-link>
          </li>
        </ul>
      </nav>

      <!-- Program Pages Section -->
      <div class="px-4 py-2">
        <div class="border-t border-white/20 pt-4">
          <h3 class="text-xs font-semibold text-white/60 uppercase tracking-wider mb-3 px-4">برنامه‌ها</h3>
          <ul class="space-y-2">
            <li>
              <router-link 
                to="/program-404640723" 
                class="flex items-center space-x-3 space-x-reverse px-4 py-3 text-white/80 hover:text-white hover:bg-white/10 rounded-lg transition-all duration-200 group"
                active-class="bg-white/20 text-white"
              >
                <font-awesome-icon icon="fas fa-file-alt" class="text-lg transition-transform" />
                <span>برنامه 404640723</span>
              </router-link>
            </li>
            
            <li>
              <router-link 
                to="/program-404640725" 
                class="flex items-center space-x-3 space-x-reverse px-4 py-3 text-white/80 hover:text-white hover:bg-white/10 rounded-lg transition-all duration-200 group"
                active-class="bg-white/20 text-white"
              >
                <font-awesome-icon icon="fas fa-file-alt" class="text-lg transition-transform" />
                <span>برنامه 404640725</span>
              </router-link>
            </li>
            
            <li>
              <router-link 
                to="/program-404640758" 
                class="flex items-center space-x-3 space-x-reverse px-4 py-3 text-white/80 hover:text-white hover:bg-white/10 rounded-lg transition-all duration-200 group"
                active-class="bg-white/20 text-white"
              >
                <font-awesome-icon icon="fas fa-file-alt" class="text-lg transition-transform" />
                <span>برنامه 404640758</span>
              </router-link>
            </li>
            
            <li>
              <router-link 
                to="/program-403640724" 
                class="flex items-center space-x-3 space-x-reverse px-4 py-3 text-white/80 hover:text-white hover:bg-white/10 rounded-lg transition-all duration-200 group"
                active-class="bg-white/20 text-white"
              >
                <font-awesome-icon icon="fas fa-file-alt" class="text-lg transition-transform" />
                <span>برنامه 403640724</span>
              </router-link>
            </li>
            
            <li>
              <router-link 
                to="/program-403640722" 
                class="flex items-center space-x-3 space-x-reverse px-4 py-3 text-white/80 hover:text-white hover:bg-white/10 rounded-lg transition-all duration-200 group"
                active-class="bg-white/20 text-white"
              >
                <font-awesome-icon icon="fas fa-file-alt" class="text-lg transition-transform" />
                <span>برنامه 403640722</span>
              </router-link>
            </li>
          </ul>
        </div>
      </div>

      <!-- Special Programs Section -->
      <div class="px-4 py-2">
        <div class="border-t border-white/20 pt-4">
          <h3 class="text-xs font-semibold text-white/60 uppercase tracking-wider mb-3 px-4">طرح‌های ویژه</h3>
          <ul class="space-y-2">
            <li>
              <router-link 
                to="/program-abul-fazl" 
                class="flex items-center space-x-3 space-x-reverse px-4 py-3 text-white/80 hover:text-white hover:bg-white/10 rounded-lg transition-all duration-200 group"
                active-class="bg-white/20 text-white"
              >
                <font-awesome-icon icon="fas fa-star" class="text-lg transition-transform" />
                <span>طرح حضرت ابوالفضل - علیه السلام</span>
              </router-link>
            </li>
            
            <li>
              <router-link 
                to="/program-thar-allah" 
                class="flex items-center space-x-3 space-x-reverse px-4 py-3 text-white/80 hover:text-white hover:bg-white/10 rounded-lg transition-all duration-200 group"
                active-class="bg-white/20 text-white"
              >
                <font-awesome-icon icon="fas fa-star" class="text-lg transition-transform" />
                <span>طرح حضرت ثارالله - علیه السلام</span>
              </router-link>
            </li>
            
            <li>
              <router-link 
                to="/program-qamar-bani-hashim" 
                class="flex items-center space-x-3 space-x-reverse px-4 py-3 text-white/80 hover:text-white hover:bg-white/10 rounded-lg transition-all duration-200 group"
                active-class="bg-white/20 text-white"
              >
                <font-awesome-icon icon="fas fa-star" class="text-lg transition-transform" />
                <span>طرح حضرت قمر بنی هاشم - علیه السلام</span>
              </router-link>
            </li>
            
            <li>
              <router-link 
                to="/program-baqiyat-allah" 
                class="flex items-center space-x-3 space-x-reverse px-4 py-3 text-white/80 hover:text-white hover:bg-white/10 rounded-lg transition-all duration-200 group"
                active-class="bg-white/20 text-white"
              >
                <font-awesome-icon icon="fas fa-star" class="text-lg transition-transform" />
                <span>طرح حضرت بقیه الله - عجل الله</span>
              </router-link>
            </li>
            
            <li>
              <router-link 
                to="/commission-prevention" 
                class="flex items-center space-x-3 space-x-reverse px-4 py-3 text-white/80 hover:text-white hover:bg-white/10 rounded-lg transition-all duration-200 group"
                active-class="bg-white/20 text-white"
              >
                <font-awesome-icon icon="fas fa-shield-alt" class="text-lg transition-transform" />
                <span>کمیسیون پیشگیری مقابله با نفوذ</span>
              </router-link>
            </li>
          </ul>
        </div>
      </div>
    </div>

  </aside>
</template>

<script setup>
import { computed } from 'vue'
import { useAuthStore } from '../stores/auth'

const authStore = useAuthStore()

defineProps({
  sidebarOpen: {
    type: Boolean,
    default: false
  }
})

defineEmits(['toggle-sidebar'])

// Role-based navigation
const canAccessMonitoring = computed(() => {
  return authStore.user?.role === 'admin'
})

const canAccessUserManagement = computed(() => {
  return authStore.user?.role === 'admin'
})
</script>

