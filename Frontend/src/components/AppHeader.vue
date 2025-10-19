<template>
  <!-- Top Bar -->
  <header class="bg-white shadow-sm border-b border-gray-200">
    <div class="flex items-center justify-between px-6 py-4">
      <button 
        @click="$emit('toggle-sidebar')"
        class="relative group p-3 rounded-xl bg-gradient-to-r from-blue-50 to-indigo-50 hover:from-blue-100 hover:to-indigo-100 transition-all duration-300 hover:shadow-lg border border-blue-200/50 hover:border-blue-300/70"
        :title="sidebarOpen ? 'بستن منو' : 'باز کردن منو'"
      >
        <div class="relative w-6 h-6">
          <!-- Arrow that rotates based on sidebar state -->
          <div class="absolute inset-0 flex items-center justify-center">
            <svg 
              :class="[
                'w-5 h-5 text-blue-600 transition-all duration-500 ease-in-out group-hover:text-blue-700 group-hover:scale-110',
                sidebarOpen ? 'rotate-180' : 'rotate-0'
              ]" 
              fill="none" 
              stroke="currentColor" 
              viewBox="0 0 24 24"
            >
              <path 
                stroke-linecap="round" 
                stroke-linejoin="round" 
                stroke-width="2.5" 
                d="M15 19l-7-7 7-7"
              />
            </svg>
          </div>
          
          <!-- Subtle glow effect -->
          <div class="absolute inset-0 rounded-full bg-blue-400/20 scale-0 group-hover:scale-150 transition-all duration-500 ease-out"></div>
        </div>
        
        <!-- Ripple effect on click -->
        <div class="absolute inset-0 rounded-xl bg-blue-500/20 scale-0 group-active:scale-100 transition-transform duration-200 ease-out"></div>
      </button>
      
      <div class="flex items-center justify-between w-full mr-6">
        <div class="flex items-center space-x-6 space-x-reverse">
          <div class="w-8 h-8 bg-blue-800 rounded-full flex items-center justify-center">
            <font-awesome-icon icon="fas fa-user" class="text-white text-sm" />
          </div>
          <div>
            <span class="text-gray-700 font-medium">{{ userName }}</span>
            <p class="text-xs text-gray-500">{{ userRole }}</p>
          </div>
        </div>
        
        <div class="flex items-center space-x-4 space-x-reverse">
          <div class="relative">
            <button 
              @click="openNotificationModal"
              class="text-gray-600 hover:text-gray-900 transition-colors"
              title="اعلانات"
            >
              <font-awesome-icon icon="fas fa-bell" class="text-xl" />
              <span 
                :class="[
                  'absolute -top-1 -left-1 w-3 h-3 bg-red-500 rounded-full',
                  hasRecentNotifications ? 'notification-blink' : ''
                ]"
              ></span>
            </button>
          </div>
          
          <button 
            @click="handleLogout"
            class="text-gray-600 hover:text-red-600 transition-colors"
            title="خروج از سیستم"
          >
            <font-awesome-icon icon="fas fa-sign-out-alt" class="text-xl" />
          </button>
        </div>
      </div>
    </div>
  </header>
  
  <!-- Notification Modal -->
  <NotificationModal 
    :is-open="notificationModalOpen" 
    @close="closeNotificationModal" 
  />
</template>

<script setup>
import { computed, ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { useToast } from 'vue-toastification'
import axios from 'axios'
import NotificationModal from './NotificationModal.vue'

defineProps({
  sidebarOpen: {
    type: Boolean,
    default: false
  }
})

defineEmits(['toggle-sidebar'])

const router = useRouter()
const authStore = useAuthStore()
const toast = useToast()

const notificationModalOpen = ref(false)
const hasRecentNotifications = ref(false)

const userName = computed(() => authStore.userName || 'کاربر')
const userRole = computed(() => {
  const roles = {
    'admin': 'مدیر سیستم',
    'manager': 'مدیر',
    'user': 'کاربر'
  }
  return roles[authStore.userRole] || 'کاربر'
})

const checkRecentNotifications = async () => {
  try {
    const response = await axios.get('/notifications')
    hasRecentNotifications.value = response.data.has_recent_notifications
    console.log('Recent notifications check:', response.data.has_recent_notifications)
  } catch (error) {
    console.error('Error checking recent notifications:', error)
    hasRecentNotifications.value = false
  }
}

const openNotificationModal = async () => {
  notificationModalOpen.value = true
  await checkRecentNotifications()
}

const closeNotificationModal = () => {
  notificationModalOpen.value = false
}

const handleLogout = () => {
  authStore.logout()
  toast.success('با موفقیت از سیستم خارج شدید')
  router.push('/login')
}

// Check for recent notifications when component mounts
onMounted(() => {
  checkRecentNotifications()
})
</script>

<style scoped>
.notification-blink {
  animation: blink 1s infinite;
}

@keyframes blink {
  0%, 50% { opacity: 1; }
  51%, 100% { opacity: 0.3; }
}
</style>
