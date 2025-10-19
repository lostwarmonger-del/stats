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
              <h1 class="text-3xl font-bold mb-2">برنامه 404640723</h1>
              <p class="text-blue-100 text-lg">فرم ثبت اطلاعات برنامه 404640723</p>
            </div>
            <div class="w-20 h-20 bg-white/20 rounded-full flex items-center justify-center">
              <font-awesome-icon icon="fas fa-file-alt" class="text-4xl text-yellow-400" />
            </div>
          </div>
        </div>

        <!-- Loading State -->
        <div v-if="loading" class="text-center py-8">
          <font-awesome-icon icon="fas fa-spinner" class="animate-spin text-2xl text-blue-600 mb-4" />
          <p class="text-gray-600">در حال بارگذاری...</p>
        </div>

        <!-- Form Content -->
        <div v-else class="space-y-8">
          <!-- Action Buttons -->
          <div class="flex justify-between items-center mb-6">
            <button
              type="button"
              @click="openDataModal"
              class="bg-gradient-to-r from-indigo-600 to-purple-700 hover:from-indigo-700 hover:to-purple-800 text-white py-3 px-8 rounded-xl transition-all duration-300 font-semibold flex items-center space-x-3 space-x-reverse shadow-lg hover:shadow-xl transform hover:scale-105"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path>
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"></path>
              </svg>
              <span>مشاهده داده‌های ذخیره شده</span>
            </button>
            
            <div class="text-sm text-gray-600">
              آخرین بروزرسانی: {{ lastUpdated || 'هنوز ذخیره نشده' }}
            </div>
          </div>

          <form @submit.prevent="saveData" class="space-y-8">
            <!-- Basic Information Section -->
            <div class="bg-white rounded-xl p-6 border border-gray-200 shadow-sm">
              <h3 class="text-lg font-semibold text-gray-900 mb-4 flex items-center">
                <font-awesome-icon icon="fas fa-info-circle" class="text-blue-600 ml-2" />
                اطلاعات پایه
              </h3>
              
              <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">ردیف <span class="text-red-500">*</span></label>
                  <input 
                    v-model="formData.row_number" 
                    type="text" 
                    readonly
                    class="w-full px-4 py-3 border border-gray-300 rounded-xl bg-gray-100 text-gray-600 cursor-not-allowed transition-all"
                    placeholder="شماره ردیف به صورت خودکار تولید می‌شود"
                  />
                  <p class="text-xs text-gray-500 mt-1">شماره ردیف به صورت خودکار تولید می‌شود</p>
                </div>
                
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">آدرس پیج یا کانال <span class="text-red-500">*</span></label>
                  <input 
                    v-model="formData.page_channel_address" 
                    type="text" 
                    :class="['w-full px-4 py-3 border rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all', errors.page_channel_address ? 'border-red-500' : 'border-gray-300']"
                    placeholder="آدرس پیج یا کانال را وارد کنید"
                  />
                  <p v-if="errors.page_channel_address" class="text-red-500 text-sm mt-1">{{ errors.page_channel_address }}</p>
                </div>
                
                <div class="md:col-span-2">
                  <label class="block text-sm font-medium text-gray-700 mb-2">موضوع خبر <span class="text-red-500">*</span></label>
                  <input 
                    v-model="formData.news_subject" 
                    type="text" 
                    :class="['w-full px-4 py-3 border rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all', errors.news_subject ? 'border-red-500' : 'border-gray-300']"
                    placeholder="موضوع خبر را وارد کنید"
                  />
                  <p v-if="errors.news_subject" class="text-red-500 text-sm mt-1">{{ errors.news_subject }}</p>
                </div>
              </div>
            </div>

            <!-- NABA Code Section -->
            <div class="bg-white rounded-xl p-6 border border-gray-200 shadow-sm">
              <h3 class="text-lg font-semibold text-gray-900 mb-4 flex items-center">
                <font-awesome-icon icon="fas fa-code" class="text-green-600 ml-2" />
                اطلاعات کد نباء
              </h3>
              
              <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">کد نبا <span class="text-red-500">*</span></label>
                  <input 
                    v-model="formData.naba_code" 
                    type="number" 
                    :class="['w-full px-4 py-3 border rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all', errors.naba_code ? 'border-red-500' : 'border-gray-300']"
                    placeholder="کد نبا را وارد کنید"
                  />
                  <p v-if="errors.naba_code" class="text-red-500 text-sm mt-1">{{ errors.naba_code }}</p>
                </div>
                
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">بررسی کد نباء <span class="text-red-500">*</span></label>
                  <input 
                    v-model="formData.naba_code_review" 
                    type="text" 
                    :class="['w-full px-4 py-3 border rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all', errors.naba_code_review ? 'border-red-500' : 'border-gray-300']"
                    placeholder="نتیجه بررسی کد نباء"
                  />
                  <p v-if="errors.naba_code_review" class="text-red-500 text-sm mt-1">{{ errors.naba_code_review }}</p>
                </div>
                
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">تاریخ ثبت کد نباء <span class="text-red-500">*</span></label>
                  <ShamsiDatePicker 
                    v-model="formData.naba_code_registration_date"
                    placeholder="تاریخ شمسی (مثال: 1403/01/15)"
                    :class="errors.naba_code_registration_date ? 'border-red-500' : ''"
                  />
                  <p v-if="errors.naba_code_registration_date" class="text-red-500 text-sm mt-1">{{ errors.naba_code_registration_date }}</p>
                </div>
              </div>
            </div>

            <!-- Suspicion Classification Section -->
            <div class="bg-white rounded-xl p-6 border border-gray-200 shadow-sm">
              <h3 class="text-lg font-semibold text-gray-900 mb-4 flex items-center">
                <font-awesome-icon icon="fas fa-shield-alt" class="text-red-600 ml-2" />
                کلاسه مظنونیت
              </h3>
              
              <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">کلاسه مظنونیت <span class="text-red-500">*</span></label>
                  <input 
                    v-model="formData.suspicion_classification" 
                    type="number" 
                    :class="['w-full px-4 py-3 border rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all', errors.suspicion_classification ? 'border-red-500' : 'border-gray-300']"
                    placeholder="کلاسه مظنونیت را وارد کنید"
                  />
                  <p v-if="errors.suspicion_classification" class="text-red-500 text-sm mt-1">{{ errors.suspicion_classification }}</p>
                </div>
                
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">تاریخ ثبت کلاسه مظنونیت <span class="text-red-500">*</span></label>
                  <ShamsiDatePicker 
                    v-model="formData.suspicion_registration_date"
                    placeholder="تاریخ شمسی (مثال: 1403/01/15)"
                    :class="errors.suspicion_registration_date ? 'border-red-500' : ''"
                  />
                  <p v-if="errors.suspicion_registration_date" class="text-red-500 text-sm mt-1">{{ errors.suspicion_registration_date }}</p>
                </div>
              </div>
            </div>

            <!-- Military Personnel Section -->
            <div class="bg-white rounded-xl p-6 border border-gray-200 shadow-sm">
              <h3 class="text-lg font-semibold text-gray-900 mb-4 flex items-center">
                <font-awesome-icon icon="fas fa-users" class="text-purple-600 ml-2" />
                اطلاعات نظامی
              </h3>
              
              <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">تعداد نظامی شناسایی شده <span class="text-red-500">*</span></label>
                  <input 
                    v-model="formData.identified_military_count" 
                    type="number" 
                    :class="['w-full px-4 py-3 border rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all', errors.identified_military_count ? 'border-red-500' : 'border-gray-300']"
                    placeholder="تعداد نظامی شناسایی شده"
                  />
                  <p v-if="errors.identified_military_count" class="text-red-500 text-sm mt-1">{{ errors.identified_military_count }}</p>
                </div>
                
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">تعداد وابستگان نظامی شناسایی شده <span class="text-red-500">*</span></label>
                  <input 
                    v-model="formData.identified_military_dependents_count" 
                    type="number" 
                    :class="['w-full px-4 py-3 border rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all', errors.identified_military_dependents_count ? 'border-red-500' : 'border-gray-300']"
                    placeholder="تعداد وابستگان نظامی"
                  />
                  <p v-if="errors.identified_military_dependents_count" class="text-red-500 text-sm mt-1">{{ errors.identified_military_dependents_count }}</p>
                </div>
                
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">پلیس افتخاری <span class="text-red-500">*</span></label>
                  <input 
                    v-model="formData.honorary_police" 
                    type="number" 
                    :class="['w-full px-4 py-3 border rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all', errors.honorary_police ? 'border-red-500' : 'border-gray-300']"
                    placeholder="اطلاعات پلیس افتخاری"
                  />
                  <p v-if="errors.honorary_police" class="text-red-500 text-sm mt-1">{{ errors.honorary_police }}</p>
                </div>
              </div>
            </div>

            <!-- Action Results Section -->
            <div class="bg-white rounded-xl p-6 border border-gray-200 shadow-sm">
              <h3 class="text-lg font-semibold text-gray-900 mb-4 flex items-center">
                <font-awesome-icon icon="fas fa-clipboard-check" class="text-orange-600 ml-2" />
                نتیجه اقدامات
              </h3>
              
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">نتیجه اقدامات (درصورت اطلاع) <span class="text-red-500">*</span></label>
                <textarea 
                  v-model="formData.action_results" 
                  rows="4"
                  :class="['w-full px-4 py-3 border rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all', errors.action_results ? 'border-red-500' : 'border-gray-300']"
                  placeholder="نتیجه اقدامات انجام شده را شرح دهید"
                ></textarea>
                <p v-if="errors.action_results" class="text-red-500 text-sm mt-1">{{ errors.action_results }}</p>
              </div>
            </div>

            <!-- Save Button -->
            <div class="flex justify-end">
              <button 
                type="submit" 
                :disabled="saving"
                class="bg-gradient-to-r from-blue-600 to-indigo-700 hover:from-blue-700 hover:to-indigo-800 text-white py-3 px-8 rounded-xl transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed font-semibold flex items-center space-x-2 space-x-reverse"
              >
                <font-awesome-icon v-if="saving" icon="fas fa-spinner" class="animate-spin" />
                <font-awesome-icon v-else icon="fas fa-save" />
                <span>{{ saving ? 'در حال ذخیره...' : 'ذخیره اطلاعات' }}</span>
              </button>
      </div>
          </form>
      </div>
      </main>
    </div>
  </div>
  
  <!-- Data Viewing Modal -->
  <ProgramDataModal 
    :is-open="dataModalOpen" 
    @close="closeDataModal"
    @edit="editDataFromModal"
  />
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useAuthStore } from '../stores/auth'
import { useToast } from 'vue-toastification'
import axios from 'axios'
import ProgramDataModal from './ProgramDataModal.vue'
import ShamsiDatePicker from './ShamsiDatePicker.vue'
import Sidebar from './Sidebar.vue'
import AppHeader from './AppHeader.vue'

const authStore = useAuthStore()
const toast = useToast()
const loading = ref(false)
const saving = ref(false)
const sidebarOpen = ref(true)
const lastUpdated = ref('')

const formData = ref({
  row_number: '', // Will be auto-filled
  page_channel_address: '',
  news_subject: '',
  naba_code: '',
  naba_code_review: '',
  naba_code_registration_date: '',
  suspicion_classification: '',
  suspicion_registration_date: '',
  action_results: '',
  identified_military_count: '',
  identified_military_dependents_count: '',
  honorary_police: ''
})

const errors = ref({})
const dataModalOpen = ref(false)
const hasExistingData = ref(false)

const toggleSidebar = () => {
  sidebarOpen.value = !sidebarOpen.value
}

const validateForm = () => {
  errors.value = {}
  let isValid = true

  const requiredFields = [
    'page_channel_address',
    'news_subject', 
    'naba_code',
    'naba_code_review',
    'naba_code_registration_date',
    'suspicion_classification',
    'suspicion_registration_date',
    'action_results',
    'identified_military_count',
    'identified_military_dependents_count',
    'honorary_police'
  ]

  requiredFields.forEach(field => {
    const value = formData.value[field]
    // Handle both string and number fields
    const isEmpty = value === null || value === undefined || 
                   value === '' ||
                   (typeof value === 'string' && value.trim() === '')
    
    if (isEmpty) {
      errors.value[field] = 'این فیلد الزامی است'
      isValid = false
    }
  })

  return isValid
}

const generateRowNumber = () => {
  // Generate a unique row number based on user ID and timestamp
  const timestamp = Date.now().toString().slice(-6)
  const userId = authStore.user.id.toString().padStart(3, '0')
  return `${userId}-${timestamp}`
}

const saveData = async () => {
  // Auto-fill row number
  formData.value.row_number = generateRowNumber()
  
  // Validate form
  if (!validateForm()) {
    toast.error('لطفاً تمام فیلدهای الزامی را پر کنید')
    return
  }

  saving.value = true
  try {
    await axios.post('/programs/404640723', formData.value)
    toast.success('اطلاعات با موفقیت ذخیره شد')
    
    // Reset form after successful save
    resetForm()
    
    // Refresh the "Last Updated" field with the latest data
    await loadData()
  } catch (error) {
    console.error('Error saving data:', error)
    
    // Check if it's a validation error (422)
    if (error.response?.status === 422) {
      toast.error('برو دم در خونه خودتون بازی کن')
    } else {
      toast.error(error.response?.data?.detail || 'خطا در ذخیره اطلاعات')
    }
  } finally {
    saving.value = false
  }
}

const resetForm = () => {
  formData.value = {
    row_number: '',
    page_channel_address: '',
    news_subject: '',
    naba_code: '',
    naba_code_review: '',
    naba_code_registration_date: '',
    suspicion_classification: '',
    suspicion_registration_date: '',
    action_results: '',
    identified_military_count: '',
    identified_military_dependents_count: '',
    honorary_police: ''
  }
  errors.value = {}
  hasExistingData.value = false
}

const loadData = async () => {
  loading.value = true
  try {
    // Get the latest saved data to show in "Last Updated"
    const response = await axios.get('/programs/404640723/all')
    const userData = response.data || []
    
    if (userData.length > 0) {
      // Find the most recent record
      const latestRecord = userData.reduce((latest, current) => {
        const latestDate = new Date(latest.created_at || latest.updated_at)
        const currentDate = new Date(current.created_at || current.updated_at)
        return currentDate > latestDate ? current : latest
      })
      
      // Format the date for display
      const date = new Date(latestRecord.created_at || latestRecord.updated_at)
      lastUpdated.value = date.toLocaleString('fa-IR', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })
    } else {
      lastUpdated.value = ''
    }
    
    // Form should always start empty for new submissions
    hasExistingData.value = false
  } catch (error) {
    console.error('Error in loadData:', error)
    hasExistingData.value = false
    lastUpdated.value = ''
  } finally {
    loading.value = false
  }
}

const openDataModal = () => {
  dataModalOpen.value = true
}

const closeDataModal = () => {
  dataModalOpen.value = false
}

const editDataFromModal = (data) => {
  // Load the selected data into the form for editing
  Object.keys(formData.value).forEach(key => {
    if (data[key] !== undefined) {
      formData.value[key] = data[key]
    }
  })
  toast.success('داده‌ها برای ویرایش بارگذاری شد')
}

onMounted(() => {
  loadData()
})
</script>