<template>
  <div class="min-h-screen bg-gray-50 rtl">
    <!-- Sidebar Component -->
    <Sidebar 
      :sidebar-open="sidebarOpen" 
      @toggle-sidebar="toggleSidebar" 
    />

    <!-- Main Content -->
    <div class="flex-1 transition-all duration-300" :class="{ 'mr-64': sidebarOpen }">
      <!-- App Header -->
      <AppHeader :sidebar-open="sidebarOpen" @toggle-sidebar="toggleSidebar" />

      <!-- Page Content -->
      <main class="p-6">
        <!-- Welcome Section -->
        <div class="bg-gradient-to-r from-blue-600 to-indigo-700 rounded-2xl p-8 text-white mb-8">
          <div class="flex items-center justify-between">
            <div>
              <h1 class="text-3xl font-bold mb-2">خوش آمدید!</h1>
              <p class="text-blue-100 text-lg">{{ userName }} عزیز، به پنل مدیریت خوش آمدید</p>
            </div>
            <div class="w-20 h-20 bg-white/20 rounded-full flex items-center justify-center">
              <font-awesome-icon icon="fas fa-crown" class="text-4xl text-yellow-400" />
            </div>
          </div>
        </div>

        <!-- Stats Cards -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <div class="bg-white rounded-xl p-6 shadow-sm border border-gray-200 hover:shadow-md transition-shadow">
            <div class="flex items-center justify-between">
              <div>
                <p class="text-gray-600 text-sm font-medium">کل برنامه‌ها</p>
                <p class="text-2xl font-bold text-gray-900">11</p>
              </div>
              <div class="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
                <font-awesome-icon icon="fas fa-file-alt" class="text-blue-600 text-xl" />
              </div>
            </div>
          </div>

          <div class="bg-white rounded-xl p-6 shadow-sm border border-gray-200 hover:shadow-md transition-shadow">
            <div class="flex items-center justify-between">
              <div>
                <p class="text-gray-600 text-sm font-medium">طرح‌های ویژه</p>
                <p class="text-2xl font-bold text-gray-900">4</p>
              </div>
              <div class="w-12 h-12 bg-yellow-100 rounded-lg flex items-center justify-center">
                <font-awesome-icon icon="fas fa-star" class="text-yellow-600 text-xl" />
              </div>
            </div>
          </div>

          <div class="bg-white rounded-xl p-6 shadow-sm border border-gray-200 hover:shadow-md transition-shadow">
            <div class="flex items-center justify-between">
              <div>
                <p class="text-gray-600 text-sm font-medium">کمیسیون‌ها</p>
                <p class="text-2xl font-bold text-gray-900">1</p>
              </div>
              <div class="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center">
                <font-awesome-icon icon="fas fa-shield-alt" class="text-green-600 text-xl" />
              </div>
            </div>
          </div>

          <div class="bg-white rounded-xl p-6 shadow-sm border border-gray-200 hover:shadow-md transition-shadow">
            <div class="flex items-center justify-between">
              <div>
                <p class="text-gray-600 text-sm font-medium">داشبوردها</p>
                <p class="text-2xl font-bold text-gray-900">1</p>
              </div>
              <div class="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center">
                <font-awesome-icon icon="fas fa-chart-line" class="text-purple-600 text-xl" />
              </div>
            </div>
          </div>
        </div>

        <!-- Quick Access -->
        <div class="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
          <h2 class="text-xl font-bold text-gray-900 mb-4">دسترسی سریع</h2>
          <div class="grid grid-cols-1 gap-4">
            <router-link 
              to="/monitoring-dashboard"
              class="flex items-center p-4 bg-purple-50 rounded-lg hover:bg-purple-100 transition-colors group"
            >
              <div class="w-10 h-10 bg-purple-500 rounded-lg flex items-center justify-center ml-3">
                <font-awesome-icon icon="fas fa-chart-line" class="text-white" />
              </div>
              <div>
                <p class="font-medium text-gray-900">داشبورد مانیتورینگ</p>
                <p class="text-sm text-gray-600">آمار و گزارش</p>
              </div>
            </router-link>
          </div>
        </div>
      </main>
    </div>

    <!-- Overlay for mobile -->
    <div 
      v-if="sidebarOpen"
      @click="toggleSidebar"
      class="fixed inset-0 bg-black/50 z-40 lg:hidden"
    ></div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useAuthStore } from '../stores/auth'
import Sidebar from './Sidebar.vue'
import AppHeader from './AppHeader.vue'

const authStore = useAuthStore()
const sidebarOpen = ref(false)

const userName = computed(() => {
  return authStore.user?.name || 'کاربر'
})

const toggleSidebar = () => {
  sidebarOpen.value = !sidebarOpen.value
}
</script>

