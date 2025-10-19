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
              <h1 class="text-3xl font-bold mb-2">برنامه 403640724</h1>
              <p class="text-blue-100 text-lg">جدول پیش برد برنامه "هدفمند نمودن و بهینه سازی اقدامات واپایش پنهان سایبری"</p>
            </div>
            <div class="w-20 h-20 bg-white/20 rounded-full flex items-center justify-center">
              <font-awesome-icon icon="fas fa-shield-alt" class="text-4xl text-yellow-400" />
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
                  <label class="block text-sm font-medium text-gray-700 mb-2">نام رده <span class="text-red-500">*</span></label>
                  <input 
                    v-model="formData.category_name" 
                    type="text" 
                    :class="['w-full px-4 py-3 border rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all', errors.category_name ? 'border-red-500' : 'border-gray-300']"
                    placeholder="نام رده را وارد کنید"
                  />
                  <p v-if="errors.category_name" class="text-red-500 text-sm mt-1">{{ errors.category_name }}</p>
                </div>
                
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">شماره تلفن / ایمیل / تحت اقدام <span class="text-red-500">*</span></label>
                  <input 
                    v-model="formData.phone_email_action" 
                    type="text" 
                    :class="['w-full px-4 py-3 border rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all', errors.phone_email_action ? 'border-red-500' : 'border-gray-300']"
                    placeholder="شماره تلفن، ایمیل یا وضعیت تحت اقدام را وارد کنید"
                  />
                  <p v-if="errors.phone_email_action" class="text-red-500 text-sm mt-1">{{ errors.phone_email_action }}</p>
                </div>
              </div>
            </div>

            <!-- Virtual Networks Monitoring Section -->
            <div class="bg-white rounded-xl p-6 border border-gray-200 shadow-sm">
              <h3 class="text-lg font-semibold text-gray-900 mb-4 flex items-center">
                <font-awesome-icon icon="fas fa-network-wired" class="text-green-600 ml-2" />
                تعداد مجموع واپایش پنهان موفق شبکه های مجازی انجام شده
              </h3>
              
              <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">تلگرام</label>
                  <input 
                    :value="toPersianNumbers(formData.telegram_count)"
                    @input="formatNumberInput($event.target.value, 'telegram_count')"
                    type="text" 
                    class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all text-right"
                    placeholder="۰"
                  />
                </div>
                
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">اینستاگرام</label>
                  <input 
                    :value="toPersianNumbers(formData.instagram_count)"
                    @input="formatNumberInput($event.target.value, 'instagram_count')"
                    type="text" 
                    class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all text-right"
                    placeholder="۰"
                  />
                </div>
                
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">روبیکا</label>
                  <input 
                    :value="toPersianNumbers(formData.rubika_count)"
                    @input="formatNumberInput($event.target.value, 'rubika_count')"
                    type="text" 
                    class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all text-right"
                    placeholder="۰"
                  />
                </div>
                
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">سروش</label>
                  <input 
                    :value="toPersianNumbers(formData.soroush_count)"
                    @input="formatNumberInput($event.target.value, 'soroush_count')"
                    type="text" 
                    class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all text-right"
                    placeholder="۰"
                  />
                </div>
                
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">واتس اپ</label>
                  <input 
                    :value="toPersianNumbers(formData.whatsapp_count)"
                    @input="formatNumberInput($event.target.value, 'whatsapp_count')"
                    type="text" 
                    class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all text-right"
                    placeholder="۰"
                  />
                </div>
                
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">بله</label>
                  <input 
                    :value="toPersianNumbers(formData.bale_count)"
                    @input="formatNumberInput($event.target.value, 'bale_count')"
                    type="text" 
                    class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all text-right"
                    placeholder="۰"
                  />
                </div>
                
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">آی گپ</label>
                  <input 
                    :value="toPersianNumbers(formData.igap_count)"
                    @input="formatNumberInput($event.target.value, 'igap_count')"
                    type="text" 
                    class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all text-right"
                    placeholder="۰"
                  />
                </div>
                
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">شاد</label>
                  <input 
                    :value="toPersianNumbers(formData.shad_count)"
                    @input="formatNumberInput($event.target.value, 'shad_count')"
                    type="text" 
                    class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all text-right"
                    placeholder="۰"
                  />
                </div>
                
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">ایتا</label>
                  <input 
                    :value="toPersianNumbers(formData.eitaa_count)"
                    @input="formatNumberInput($event.target.value, 'eitaa_count')"
                    type="text" 
                    class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all text-right"
                    placeholder="۰"
                  />
                </div>
                
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">گپ</label>
                  <input 
                    :value="toPersianNumbers(formData.gap_count)"
                    @input="formatNumberInput($event.target.value, 'gap_count')"
                    type="text" 
                    class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all text-right"
                    placeholder="۰"
                  />
                </div>
                
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">سایر شبکه های مجازی</label>
                  <input 
                    :value="toPersianNumbers(formData.other_virtual_networks_count)"
                    @input="formatNumberInput($event.target.value, 'other_virtual_networks_count')"
                    type="text" 
                    class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all text-right"
                    placeholder="۰"
                  />
                </div>
              </div>
            </div>

            <!-- Email Monitoring Section -->
            <div class="bg-white rounded-xl p-6 border border-gray-200 shadow-sm">
              <h3 class="text-lg font-semibold text-gray-900 mb-4 flex items-center">
                <font-awesome-icon icon="fas fa-envelope" class="text-purple-600 ml-2" />
                تعداد مجموع واپایش پنهان موفق پست های الکترونیکی انجام شده
              </h3>
              
              <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">Gmail</label>
                  <input 
                    :value="toPersianNumbers(formData.gmail_count)"
                    @input="formatNumberInput($event.target.value, 'gmail_count')"
                    type="text" 
                    class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all text-right"
                    placeholder="۰"
                  />
                </div>
                
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">Yahoo</label>
                  <input 
                    :value="toPersianNumbers(formData.yahoo_count)"
                    @input="formatNumberInput($event.target.value, 'yahoo_count')"
                    type="text" 
                    class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all text-right"
                    placeholder="۰"
                  />
                </div>
                
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">Microsoft</label>
                  <input 
                    :value="toPersianNumbers(formData.microsoft_count)"
                    @input="formatNumberInput($event.target.value, 'microsoft_count')"
                    type="text" 
                    class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all text-right"
                    placeholder="۰"
                  />
                </div>
                
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">سایر پست های الکترونیکی</label>
                  <input 
                    :value="toPersianNumbers(formData.other_emails_count)"
                    @input="formatNumberInput($event.target.value, 'other_emails_count')"
                    type="text" 
                    class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all text-right"
                    placeholder="۰"
                  />
                </div>
              </div>
            </div>

            <!-- News Registration Section -->
            <div class="bg-white rounded-xl p-6 border border-gray-200 shadow-sm">
              <h3 class="text-lg font-semibold text-gray-900 mb-4 flex items-center">
                <font-awesome-icon icon="fas fa-newspaper" class="text-orange-600 ml-2" />
                تعداد اخبار ثبت شده در سامانه نباء
              </h3>
              
              <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">شماره خبر های ثبت شده <span class="text-red-500">*</span></label>
                  <input 
                    v-model="formData.registered_news_numbers" 
                    type="text" 
                    :class="['w-full px-4 py-3 border rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all', errors.registered_news_numbers ? 'border-red-500' : 'border-gray-300']"
                    placeholder="شماره خبر های ثبت شده را وارد کنید"
                  />
                  <p v-if="errors.registered_news_numbers" class="text-red-500 text-sm mt-1">{{ errors.registered_news_numbers }}</p>
                </div>
                
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">نتیجه نهایی پرونده <span class="text-red-500">*</span></label>
                  <input 
                    v-model="formData.final_case_result" 
                    type="text" 
                    :class="['w-full px-4 py-3 border rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all', errors.final_case_result ? 'border-red-500' : 'border-gray-300']"
                    placeholder="نتیجه نهایی پرونده را وارد کنید"
                  />
                  <p v-if="errors.final_case_result" class="text-red-500 text-sm mt-1">{{ errors.final_case_result }}</p>
                </div>
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
  <ProgramDataModal403640724 
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
import ProgramDataModal403640724 from './ProgramDataModal403640724.vue'
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
  category_name: '',
  phone_email_action: '',
  telegram_count: 0,
  instagram_count: 0,
  rubika_count: 0,
  soroush_count: 0,
  whatsapp_count: 0,
  bale_count: 0,
  igap_count: 0,
  shad_count: 0,
  eitaa_count: 0,
  gap_count: 0,
  other_virtual_networks_count: 0,
  gmail_count: 0,
  yahoo_count: 0,
  microsoft_count: 0,
  other_emails_count: 0,
  registered_news_numbers: '',
  final_case_result: ''
})

const errors = ref({})
const dataModalOpen = ref(false)
const hasExistingData = ref(false)

const toggleSidebar = () => {
  sidebarOpen.value = !sidebarOpen.value
}

// Persian number formatting functions
const toPersianNumbers = (str) => {
  if (!str) return ''
  return str.toString().replace(/[0-9]/g, (digit) => {
    return String.fromCharCode(digit.charCodeAt(0) + 1728)
  })
}

const toEnglishNumbers = (str) => {
  if (!str) return ''
  return str.toString().replace(/[۰-۹]/g, (digit) => {
    return String.fromCharCode(digit.charCodeAt(0) - 1728)
  })
}

const formatNumberInput = (value, fieldName) => {
  const englishValue = toEnglishNumbers(value)
  const numericValue = parseInt(englishValue) || 0
  formData.value[fieldName] = numericValue
}

const validateForm = () => {
  errors.value = {}
  let isValid = true

  const requiredFields = [
    'category_name',
    'phone_email_action',
    'registered_news_numbers',
    'final_case_result'
  ]

  requiredFields.forEach(field => {
    const value = formData.value[field]
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
    await axios.post('/programs/403640724', formData.value)
    toast.success('اطلاعات با موفقیت ذخیره شد')
    
    // Reset form after successful save
    resetForm()
    
    // Refresh the "Last Updated" field with the latest data
    await loadData()
  } catch (error) {
    console.error('Error saving data:', error)
    
    // Check if it's a validation error (422)
    if (error.response?.status === 422) {
      toast.error('خطا در اعتبارسنجی داده‌ها. لطفاً تمام فیلدها را به درستی پر کنید.')
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
    category_name: '',
    phone_email_action: '',
    telegram_count: 0,
    instagram_count: 0,
    rubika_count: 0,
    soroush_count: 0,
    whatsapp_count: 0,
    bale_count: 0,
    igap_count: 0,
    shad_count: 0,
    eitaa_count: 0,
    gap_count: 0,
    other_virtual_networks_count: 0,
    gmail_count: 0,
    yahoo_count: 0,
    microsoft_count: 0,
    other_emails_count: 0,
    registered_news_numbers: '',
    final_case_result: ''
  }
  errors.value = {}
  hasExistingData.value = false
}

const loadData = async () => {
  loading.value = true
  try {
    // Get the latest saved data to show in "Last Updated"
    const response = await axios.get('/programs/403640724/all')
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