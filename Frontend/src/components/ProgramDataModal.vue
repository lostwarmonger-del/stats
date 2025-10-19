<template>
  <div v-if="isOpen" class="fixed inset-0 z-50 overflow-y-auto" @click="closeModal">
    <div class="flex items-center justify-center min-h-screen px-4 pt-4 pb-20 text-center sm:block sm:p-0">
      <!-- Background overlay -->
      <div class="fixed inset-0 transition-opacity bg-gray-500 bg-opacity-75" @click="closeModal"></div>

      <!-- Modal panel -->
      <div class="inline-block w-full max-w-7xl p-6 my-8 overflow-hidden text-right align-middle transition-all transform bg-white shadow-xl rounded-2xl" @click.stop>
        <!-- Header -->
        <div class="flex items-center justify-between mb-6">
          <h3 class="text-2xl font-bold text-gray-900">داده‌های ذخیره شده - برنامه 404640723</h3>
          <div class="flex items-center space-x-3 space-x-reverse">
            <button 
              @click="exportData"
              class="bg-gradient-to-r from-green-600 to-emerald-700 hover:from-green-700 hover:to-emerald-800 text-white py-2 px-4 rounded-lg transition-all duration-200 font-semibold flex items-center space-x-2 space-x-reverse"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
              </svg>
              <span>خروجی به اکسل</span>
            </button>
            <button @click="closeModal" class="p-2 text-gray-400 hover:text-gray-600 transition-colors">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
              </svg>
            </button>
          </div>
        </div>

        <!-- Filters and Controls -->
        <div class="mb-6 p-4 bg-gray-50 rounded-xl border border-gray-200">
          <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
            <!-- User Filter (Admin Only) -->
            <div v-if="authStore.user?.role === 'admin'">
              <label class="block text-sm font-medium text-gray-700 mb-2">فیلتر بر اساس کاربر</label>
              <select 
                v-model="filters.userId" 
                @change="applyFilters"
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option :value="null">همه کاربران</option>
                <option v-for="user in users" :key="user.id" :value="user.id">
                  {{ user.name }} ({{ user.username }})
                </option>
              </select>
            </div>
            
            <!-- Date From Filter -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">از تاریخ</label>
              <ShamsiDatePicker 
                v-model="filters.dateFrom"
                placeholder="تاریخ شروع (شمسی)"
                @update:modelValue="applyFilters"
              />
            </div>
            
            <!-- Date To Filter -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">تا تاریخ</label>
              <ShamsiDatePicker 
                v-model="filters.dateTo"
                placeholder="تاریخ پایان (شمسی)"
                @update:modelValue="applyFilters"
              />
            </div>
            
            <!-- Clear Filters -->
            <div class="flex items-end">
              <button 
                @click="clearFilters"
                class="w-full px-4 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700 transition-colors"
              >
                پاک کردن فیلترها
              </button>
            </div>
          </div>
        </div>

        <!-- Loading State -->
        <div v-if="loading" class="flex items-center justify-center py-12">
          <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
          <span class="mr-3 text-gray-600">در حال بارگذاری...</span>
        </div>

        <!-- Data Display -->
        <div v-else-if="paginatedData.length > 0" class="space-y-4">
          <!-- Data Cards -->
          <div v-for="(item, index) in paginatedData" :key="item.id" class="bg-gradient-to-r from-blue-50 to-indigo-50 rounded-xl p-6 border border-blue-200 hover:shadow-lg transition-all duration-200">
            <div class="flex items-center justify-between mb-4">
              <h4 class="text-lg font-semibold text-gray-900">رکورد {{ (currentPage - 1) * itemsPerPage + index + 1 }}</h4>
              <div class="flex items-center space-x-3 space-x-reverse">
                <span class="text-sm text-gray-500">{{ item.user_name }} (ID: {{ item.user_id }})</span>
                <div class="flex items-center space-x-2 space-x-reverse">
                  <button 
                    @click="editData(item)"
                    class="p-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
                    title="ویرایش این رکورد"
                  >
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"></path>
                    </svg>
                  </button>
                  <button 
                    v-if="authStore.user?.role === 'admin'"
                    @click="deleteData(item)"
                    class="p-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors"
                    title="حذف این رکورد"
                  >
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
                    </svg>
                  </button>
                </div>
              </div>
            </div>

            <!-- Data Grid -->
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              <div v-if="item.row_number" class="bg-white p-3 rounded-lg border border-gray-200">
                <label class="block text-sm font-medium text-gray-700 mb-1">شماره ردیف</label>
                <p class="text-gray-900">{{ item.row_number }}</p>
              </div>

              <div v-if="item.page_channel_address" class="bg-white p-3 rounded-lg border border-gray-200">
                <label class="block text-sm font-medium text-gray-700 mb-1">آدرس صفحه/کانال</label>
                <p class="text-gray-900">{{ item.page_channel_address }}</p>
              </div>

              <div v-if="item.news_subject" class="bg-white p-3 rounded-lg border border-gray-200">
                <label class="block text-sm font-medium text-gray-700 mb-1">موضوع خبر</label>
                <p class="text-gray-900">{{ item.news_subject }}</p>
              </div>

              <div v-if="item.naba_code" class="bg-white p-3 rounded-lg border border-gray-200">
                <label class="block text-sm font-medium text-gray-700 mb-1">کد نبا</label>
                <p class="text-gray-900">{{ item.naba_code }}</p>
              </div>

              <div v-if="item.naba_code_review" class="bg-white p-3 rounded-lg border border-gray-200">
                <label class="block text-sm font-medium text-gray-700 mb-1">بررسی کد نبا</label>
                <p class="text-gray-900">{{ item.naba_code_review }}</p>
              </div>

              <div v-if="item.naba_code_registration_date" class="bg-white p-3 rounded-lg border border-gray-200">
                <label class="block text-sm font-medium text-gray-700 mb-1">تاریخ ثبت کد نبا</label>
                <p class="text-gray-900">{{ item.naba_code_registration_date }}</p>
              </div>

              <div v-if="item.suspicion_classification" class="bg-white p-3 rounded-lg border border-gray-200">
                <label class="block text-sm font-medium text-gray-700 mb-1">کلاسه مظنونیت</label>
                <p class="text-gray-900">{{ item.suspicion_classification }}</p>
              </div>

              <div v-if="item.suspicion_registration_date" class="bg-white p-3 rounded-lg border border-gray-200">
                <label class="block text-sm font-medium text-gray-700 mb-1">تاریخ ثبت کلاسه مظنونیت</label>
                <p class="text-gray-900">{{ item.suspicion_registration_date }}</p>
              </div>

              <div v-if="item.action_results" class="bg-white p-3 rounded-lg border border-gray-200 md:col-span-2 lg:col-span-3">
                <label class="block text-sm font-medium text-gray-700 mb-1">نتایج اقدامات</label>
                <p class="text-gray-900 whitespace-pre-wrap">{{ item.action_results }}</p>
              </div>

              <div v-if="item.identified_military_count" class="bg-white p-3 rounded-lg border border-gray-200">
                <label class="block text-sm font-medium text-gray-700 mb-1">تعداد نظامی شناسایی شده</label>
                <p class="text-gray-900">{{ item.identified_military_count }}</p>
              </div>

              <div v-if="item.identified_military_dependents_count" class="bg-white p-3 rounded-lg border border-gray-200">
                <label class="block text-sm font-medium text-gray-700 mb-1">تعداد وابستگان نظامی</label>
                <p class="text-gray-900">{{ item.identified_military_dependents_count }}</p>
              </div>

              <div v-if="item.honorary_police" class="bg-white p-3 rounded-lg border border-gray-200">
                <label class="block text-sm font-medium text-gray-700 mb-1">پلیس افتخاری</label>
                <p class="text-gray-900">{{ item.honorary_police }}</p>
              </div>
            </div>

            <!-- Timestamps -->
            <div class="mt-4 pt-4 border-t border-gray-200">
              <div class="flex items-center justify-between text-sm text-gray-500">
                <span v-if="item.created_at">ایجاد شده: {{ formatDate(item.created_at) }}</span>
                <span v-if="item.updated_at">آخرین بروزرسانی: {{ formatDate(item.updated_at) }}</span>
              </div>
            </div>
          </div>

          <!-- Pagination -->
          <div v-if="totalPages > 1" class="flex items-center justify-center space-x-2 space-x-reverse mt-6">
            <button 
              @click="goToPage(currentPage - 1)"
              :disabled="currentPage === 1"
              class="px-3 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              قبلی
            </button>
            
            <span 
              v-for="page in visiblePages" 
              :key="page"
              @click="goToPage(page)"
              :class="[
                'px-3 py-2 rounded-lg cursor-pointer transition-colors',
                page === currentPage 
                  ? 'bg-blue-600 text-white' 
                  : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
              ]"
            >
              {{ page }}
            </span>
            
            <button 
              @click="goToPage(currentPage + 1)"
              :disabled="currentPage === totalPages"
              class="px-3 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              بعدی
            </button>
          </div>
        </div>

        <!-- Empty State -->
        <div v-else class="text-center py-12">
          <svg class="w-16 h-16 mx-auto mb-4 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
          </svg>
          <h3 class="text-lg font-medium text-gray-900 mb-2">هیچ داده‌ای یافت نشد</h3>
          <p class="text-gray-500">هنوز هیچ داده‌ای برای این برنامه ذخیره نشده است.</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useAuthStore } from '../stores/auth'
import { useToast } from 'vue-toastification'
import axios from 'axios'
import ShamsiDatePicker from './ShamsiDatePicker.vue'

const props = defineProps({
  isOpen: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['close', 'edit'])

const authStore = useAuthStore()
const toast = useToast()

const data = ref([])
const filteredData = ref([])
const loading = ref(false)
const currentPage = ref(1)
const itemsPerPage = ref(10)
const users = ref([])

const filters = ref({
  dateFrom: '',
  dateTo: '',
  userId: null
})

// Computed properties for pagination
const totalPages = computed(() => Math.ceil(filteredData.value.length / itemsPerPage.value))

const paginatedData = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage.value
  const end = start + itemsPerPage.value
  return filteredData.value.slice(start, end)
})

const visiblePages = computed(() => {
  const pages = []
  const start = Math.max(1, currentPage.value - 2)
  const end = Math.min(totalPages.value, currentPage.value + 2)
  
  for (let i = start; i <= end; i++) {
    pages.push(i)
  }
  return pages
})

const closeModal = () => {
  emit('close')
}

const editData = (item) => {
  emit('edit', item)
  closeModal()
}

const deleteData = async (item) => {
  if (!confirm('آیا مطمئن هستید که می‌خواهید این رکورد را حذف کنید؟')) {
    return
  }
  
  try {
    // Ensure authorization header is set
    if (authStore.token) {
      axios.defaults.headers.common['Authorization'] = `Bearer ${authStore.token}`
    }
    
    await axios.delete(`/programs/404640723/${item.id}`)
    toast.success('رکورد با موفقیت حذف شد')
    
    // Refresh the data
    await fetchData()
  } catch (error) {
    console.error('Error deleting data:', error)
    toast.error('خطا در حذف رکورد')
  }
}

const applyFilters = () => {
  // If user filter is applied, fetch data from backend
  if (filters.value.userId !== null) {
    fetchData()
    return
  }
  
  // When "All Users" is selected, fetch all data and apply date filtering
  fetchData()
}

// Simple Jalali to Gregorian conversion (approximate)
const jalaliToGregorian = (jalaliDate) => {
  if (!jalaliDate) return null
  
  const [year, month, day] = jalaliDate.split('/').map(Number)
  
  // Approximate conversion (for filtering purposes)
  // This is a simplified conversion - for production use a proper library
  const gregorianYear = year + 621
  const gregorianMonth = month + 2 // Approximate offset
  const gregorianDay = day
  
  return new Date(gregorianYear, gregorianMonth - 1, gregorianDay)
}

const clearFilters = () => {
  filters.value.dateFrom = ''
  filters.value.dateTo = ''
  filters.value.userId = null
  fetchData() // Refetch data to clear user filter
  currentPage.value = 1
}

const goToPage = (page) => {
  if (page >= 1 && page <= totalPages.value) {
    currentPage.value = page
  }
}

const exportData = async () => {
  try {
    // Ensure authorization header is set
    if (authStore.token) {
      axios.defaults.headers.common['Authorization'] = `Bearer ${authStore.token}`
    }
    
    const response = await axios.get('/programs/404640723/export', {
      responseType: 'blob'
    })
    
    // Create download link
    const url = window.URL.createObjectURL(new Blob([response.data]))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', 'program_404640723_data.xlsx')
    document.body.appendChild(link)
    link.click()
    link.remove()
    window.URL.revokeObjectURL(url)
    
    toast.success('فایل اکسل با موفقیت دانلود شد')
  } catch (error) {
    console.error('Error exporting data:', error)
    toast.error('خطا در صادرات داده‌ها')
  }
}

const fetchUsers = async () => {
  try {
    if (authStore.token) {
      axios.defaults.headers.common['Authorization'] = `Bearer ${authStore.token}`
    }
    
    // Get all data first to extract unique user IDs who have saved data for this program
    const response = await axios.get('/programs/404640723/all')
    const programData = response.data || []
    
    // Extract unique user IDs from the program data
    const userIds = [...new Set(programData.map(item => item.user_id))]
    
    if (userIds.length === 0) {
      // No data saved yet, so no users to show
      users.value = []
      return
    }
    
    // Get user details for only those who have saved data
    const userResponse = await axios.get('/users')
    const allUsers = userResponse.data || []
    
    // Filter to only show users who have saved data for this program
    users.value = allUsers.filter(user => userIds.includes(user.id))
  } catch (error) {
    console.error('Error loading users:', error)
    users.value = []
  }
}

const fetchData = async () => {
  loading.value = true
  try {
    // Ensure authorization header is set
    if (authStore.token) {
      axios.defaults.headers.common['Authorization'] = `Bearer ${authStore.token}`
    }
    
    // Build query parameters
    const params = new URLSearchParams()
    if (filters.value.userId !== null) {
      params.append('user_id', filters.value.userId)
    }
    
    // Backend now handles the filtering based on user role
    const response = await axios.get(`/programs/404640723/all?${params.toString()}`)
    data.value = response.data || []
    console.log('Data loaded:', data.value)
    
    // Apply date filtering if no user filter is applied
    if (filters.value.userId === null) {
      filteredData.value = data.value.filter(item => {
        if (!filters.value.dateFrom && !filters.value.dateTo) {
          return true
        }
        
        // Convert Jalali dates to Gregorian for comparison
        const itemDate = new Date(item.created_at)
        
        if (filters.value.dateFrom) {
          const fromDate = jalaliToGregorian(filters.value.dateFrom)
          if (itemDate < fromDate) return false
        }
        
        if (filters.value.dateTo) {
          const toDate = jalaliToGregorian(filters.value.dateTo)
          if (itemDate > toDate) return false
        }
        
        return true
      })
    } else {
      filteredData.value = [...data.value]
    }
  } catch (error) {
    console.error('Error loading data:', error)
    console.error('Error details:', error.response?.data)
    toast.error('خطا در بارگذاری داده‌ها')
    data.value = []
    filteredData.value = []
  } finally {
    loading.value = false
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

// Watch for modal open/close to fetch data
watch(() => props.isOpen, async (newValue) => {
  if (newValue) {
    await fetchData()
    // Fetch users if admin - this will now only show users who have saved data for this program
    if (authStore.user?.role === 'admin') {
      await fetchUsers()
    }
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
