<template>
  <div v-if="isOpen" class="fixed inset-0 z-50 overflow-y-auto" @click="closeModal">
    <div class="flex items-center justify-center min-h-screen px-4 pt-4 pb-20 text-center sm:block sm:p-0">
      <!-- Background overlay -->
      <div class="fixed inset-0 transition-opacity bg-gray-500 bg-opacity-75" @click="closeModal"></div>

      <!-- Modal panel -->
      <div class="inline-block w-full max-w-md p-6 my-8 overflow-hidden text-right align-middle transition-all transform bg-white shadow-xl rounded-2xl" @click.stop>
        <!-- Header -->
        <div class="flex items-center justify-between mb-6">
          <h3 class="text-xl font-bold text-gray-900">اعلانات سیستم</h3>
          <button @click="closeModal" class="p-2 text-gray-400 hover:text-gray-600 transition-colors">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
            </svg>
          </button>
        </div>

        <!-- Send Notification Form (Only for Admin ID 1) -->
        <div v-if="canSendNotifications" class="mb-6 p-4 bg-blue-50 rounded-xl border border-blue-200">
          <h4 class="text-lg font-semibold text-blue-900 mb-4">ارسال اعلان جدید</h4>
          
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">عنوان اعلان</label>
              <input 
                v-model="newNotification.title"
                type="text" 
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                placeholder="عنوان اعلان را وارد کنید"
              />
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">متن اعلان</label>
              <textarea 
                v-model="newNotification.message"
                rows="3"
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                placeholder="متن اعلان را وارد کنید"
              ></textarea>
            </div>
            
            <button 
              @click="sendNotification"
              :disabled="!newNotification.title || !newNotification.message || sending"
              class="w-full px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              <span v-if="sending">در حال ارسال...</span>
              <span v-else>ارسال اعلان</span>
            </button>
          </div>
        </div>

        <!-- Notifications List -->
        <div class="space-y-3">
          <h4 class="text-lg font-semibold text-gray-900 mb-4">اعلانات اخیر</h4>
          
          <div v-if="notifications.length === 0" class="text-center py-8 text-gray-500">
            <svg class="w-12 h-12 mx-auto mb-4 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-5 5v-5zM4.5 19.5a1.5 1.5 0 01-1.5-1.5V6a1.5 1.5 0 011.5-1.5h15A1.5 1.5 0 0121 6v12a1.5 1.5 0 01-1.5 1.5h-15z"></path>
            </svg>
            <p>هیچ اعلانی وجود ندارد</p>
          </div>
          
          <div v-else class="max-h-64 overflow-y-auto scrollbar-hide space-y-3">
            <div 
              v-for="notification in notifications" 
              :key="notification.id"
              class="p-4 bg-gray-50 rounded-lg border border-gray-200 hover:bg-gray-100 transition-colors"
            >
              <div class="flex items-start justify-between">
                <div class="flex-1">
                  <h5 class="font-semibold text-gray-900 mb-1">{{ notification.title }}</h5>
                  <p class="text-sm text-gray-600 mb-2">{{ notification.message }}</p>
                  <div class="flex items-center justify-between text-xs text-gray-500">
                    <span>ارسال شده توسط: {{ notification.created_by_name }}</span>
                    <span>{{ formatDate(notification.created_at) }}</span>
                  </div>
                </div>
                
                <!-- Delete button (Only for Admin ID 1) -->
                <button 
                  v-if="canSendNotifications"
                  @click="deleteNotification(notification.id)"
                  class="ml-3 p-1 text-red-500 hover:text-red-700 hover:bg-red-50 rounded transition-colors"
                  title="حذف اعلان"
                >
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
                  </svg>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useAuthStore } from '../stores/auth'
import { useToast } from 'vue-toastification'
import axios from 'axios'

const props = defineProps({
  isOpen: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['close'])

const authStore = useAuthStore()
const toast = useToast()

const notifications = ref([])
const loading = ref(false)
const sending = ref(false)

const newNotification = ref({
  title: '',
  message: ''
})

// Check if current user can send notifications (only admin ID 1)
const canSendNotifications = computed(() => {
  return authStore.user?.id === 1
})

const closeModal = () => {
  emit('close')
}

const fetchNotifications = async () => {
  loading.value = true
  try {
    const response = await axios.get('/notifications')
    notifications.value = response.data.notifications
  } catch (error) {
    console.error('Error fetching notifications:', error)
    toast.error('خطا در دریافت اعلانات')
  } finally {
    loading.value = false
  }
}

const sendNotification = async () => {
  if (!newNotification.value.title || !newNotification.value.message) {
    toast.error('لطفاً عنوان و متن اعلان را وارد کنید')
    return
  }

  sending.value = true
  try {
    await axios.post('/notifications', {
      title: newNotification.value.title,
      message: newNotification.value.message
    })
    
    toast.success('اعلان با موفقیت ارسال شد')
    
    // Reset form
    newNotification.value = {
      title: '',
      message: ''
    }
    
    // Refresh notifications
    await fetchNotifications()
  } catch (error) {
    console.error('Error sending notification:', error)
    toast.error(error.response?.data?.detail || 'خطا در ارسال اعلان')
  } finally {
    sending.value = false
  }
}

const deleteNotification = async (notificationId) => {
  if (!confirm('آیا مطمئن هستید که می‌خواهید این اعلان را حذف کنید؟')) {
    return
  }

  try {
    await axios.delete(`/notifications/${notificationId}`)
    toast.success('اعلان با موفقیت حذف شد')
    
    // Refresh notifications
    await fetchNotifications()
  } catch (error) {
    console.error('Error deleting notification:', error)
    toast.error(error.response?.data?.detail || 'خطا در حذف اعلان')
  }
}

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('fa-IR', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

onMounted(() => {
  if (props.isOpen) {
    fetchNotifications()
  }
})

// Watch for modal open/close to fetch notifications
watch(() => props.isOpen, (newValue) => {
  if (newValue) {
    fetchNotifications()
  }
})
</script>

<style scoped>
.scrollbar-hide {
  -ms-overflow-style: none;
  scrollbar-width: none;
}

.scrollbar-hide::-webkit-scrollbar {
  display: none;
}
</style>