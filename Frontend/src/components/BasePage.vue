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
        <!-- Page Header -->
        <div class="bg-gradient-to-r from-blue-600 to-indigo-700 rounded-2xl p-8 text-white mb-8">
          <div class="flex items-center justify-between">
            <div>
              <h1 class="text-3xl font-bold mb-2">{{ pageTitle }}</h1>
              <p class="text-blue-100 text-lg">{{ pageDescription }}</p>
            </div>
            <div class="w-20 h-20 bg-white/20 rounded-full flex items-center justify-center">
              <font-awesome-icon :icon="pageIcon" class="text-4xl text-yellow-400" />
            </div>
          </div>
        </div>

        <!-- Page Content -->
        <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <slot></slot>
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
import { ref } from 'vue'
import Sidebar from './Sidebar.vue'
import AppHeader from './AppHeader.vue'

defineProps({
  pageTitle: {
    type: String,
    required: true
  },
  pageDescription: {
    type: String,
    required: true
  },
  pageIcon: {
    type: String,
    required: true
  }
})

const sidebarOpen = ref(false)

const toggleSidebar = () => {
  sidebarOpen.value = !sidebarOpen.value
}
</script>
