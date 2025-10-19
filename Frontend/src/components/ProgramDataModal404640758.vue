<template>
  <div v-if="isOpen" class="fixed inset-0 z-50 overflow-y-auto" @click="closeModal">
    <div class="flex items-center justify-center min-h-screen px-4 pt-4 pb-20 text-center sm:block sm:p-0">
      <!-- Background overlay -->
      <div class="fixed inset-0 transition-opacity bg-gray-500 bg-opacity-75" @click="closeModal"></div>

      <!-- Modal panel -->
      <div class="inline-block w-full max-w-7xl p-6 my-8 overflow-hidden text-right align-middle transition-all transform bg-white shadow-xl rounded-2xl" @click.stop>
        <!-- Header -->
        <div class="flex items-center justify-between mb-6">
          <h3 class="text-2xl font-bold text-gray-900">داده‌های ذخیره شده - برنامه 404640758</h3>
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
                placeholder="تاریخ شمسی (مثال: 1403/01/15)"
                @change="applyFilters"
              />
            </div>
            
            <!-- Date To Filter -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">تا تاریخ</label>
              <ShamsiDatePicker 
                v-model="filters.dateTo"
                placeholder="تاریخ شمسی (مثال: 1403/01/15)"
                @change="applyFilters"
              />
            </div>
            
            <!-- Search Filter -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">جستجو</label>
              <input 
                v-model="filters.search" 
                @input="applyFilters"
                type="text" 
                placeholder="جستجو در نام، نام خانوادگی، کد ملی..."
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
          </div>
          
          <!-- Clear Filters Button -->
          <div class="mt-4 flex justify-end">
            <button 
              @click="clearFilters"
              class="px-4 py-2 text-sm text-gray-600 hover:text-gray-800 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
            >
              پاک کردن فیلترها
            </button>
          </div>
        </div>

        <!-- Loading State -->
        <div v-if="loading" class="flex items-center justify-center py-12">
          <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
          <span class="mr-3 text-gray-600">در حال بارگذاری...</span>
        </div>

        <!-- Data Display -->
        <div v-else-if="filteredData.length > 0" class="space-y-4">
          <!-- Data Cards -->
          <div v-for="(item, index) in paginatedData" :key="item.id" class="bg-gradient-to-r from-blue-50 to-indigo-50 rounded-xl p-6 border border-blue-200 hover:shadow-lg transition-all duration-200">
            <div class="flex items-center justify-between mb-4">
              <h4 class="text-lg font-semibold text-gray-900">رکورد {{ (currentPage - 1) * itemsPerPage + index + 1 }}</h4>
              <div class="flex items-center space-x-3 space-x-reverse">
                <span class="text-sm text-gray-500">{{ item.user_name }} (ID: {{ item.user_id }})</span>
                <div class="flex items-center space-x-2 space-x-reverse">
                  <button 
                    @click="editItem(item)"
                    class="p-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
                    title="ویرایش این رکورد"
                  >
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"></path>
                    </svg>
                  </button>
                  <button 
                    v-if="authStore.user?.role === 'admin'"
                    @click="deleteItem(item)"
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
              <div v-if="item.first_name" class="bg-white p-3 rounded-lg border border-gray-200">
                <label class="block text-sm font-medium text-gray-700 mb-1">نام</label>
                <p class="text-gray-900">{{ item.first_name }}</p>
              </div>

              <div v-if="item.last_name" class="bg-white p-3 rounded-lg border border-gray-200">
                <label class="block text-sm font-medium text-gray-700 mb-1">نام خانوادگی</label>
                <p class="text-gray-900">{{ item.last_name }}</p>
              </div>

              <div v-if="item.father_name" class="bg-white p-3 rounded-lg border border-gray-200">
                <label class="block text-sm font-medium text-gray-700 mb-1">نام پدر</label>
                <p class="text-gray-900">{{ item.father_name }}</p>
              </div>

              <div v-if="item.id_number" class="bg-white p-3 rounded-lg border border-gray-200">
                <label class="block text-sm font-medium text-gray-700 mb-1">شماره شناسنامه</label>
                <p class="text-gray-900">{{ item.id_number }}</p>
              </div>

              <div v-if="item.birth_date" class="bg-white p-3 rounded-lg border border-gray-200">
                <label class="block text-sm font-medium text-gray-700 mb-1">تاریخ تولد</label>
                <p class="text-gray-900">{{ item.birth_date }}</p>
              </div>

              <div v-if="item.national_id" class="bg-white p-3 rounded-lg border border-gray-200">
                <label class="block text-sm font-medium text-gray-700 mb-1">کد ملی</label>
                <p class="text-gray-900">{{ item.national_id }}</p>
              </div>

              <div v-if="item.id_issue_date" class="bg-white p-3 rounded-lg border border-gray-200">
                <label class="block text-sm font-medium text-gray-700 mb-1">تاریخ صدور شناسنامه</label>
                <p class="text-gray-900">{{ item.id_issue_date }}</p>
              </div>

              <div v-if="item.id_issue_place" class="bg-white p-3 rounded-lg border border-gray-200">
                <label class="block text-sm font-medium text-gray-700 mb-1">محل صدور شناسنامه</label>
                <p class="text-gray-900">{{ item.id_issue_place }}</p>
              </div>

              <div v-if="item.religion" class="bg-white p-3 rounded-lg border border-gray-200">
                <label class="block text-sm font-medium text-gray-700 mb-1">دین (مذهب)</label>
                <p class="text-gray-900">{{ item.religion }}</p>
              </div>

              <div v-if="item.province" class="bg-white p-3 rounded-lg border border-gray-200">
                <label class="block text-sm font-medium text-gray-700 mb-1">استان</label>
                <p class="text-gray-900">{{ item.province }}</p>
              </div>

              <div v-if="item.city" class="bg-white p-3 rounded-lg border border-gray-200">
                <label class="block text-sm font-medium text-gray-700 mb-1">شهر</label>
                <p class="text-gray-900">{{ item.city }}</p>
              </div>

              <div v-if="item.address" class="bg-white p-3 rounded-lg border border-gray-200">
                <label class="block text-sm font-medium text-gray-700 mb-1">آدرس محل سکونت</label>
                <p class="text-gray-900">{{ item.address }}</p>
              </div>

              <div v-if="item.phone_number" class="bg-white p-3 rounded-lg border border-gray-200">
                <label class="block text-sm font-medium text-gray-700 mb-1">شماره تماس</label>
                <p class="text-gray-900">{{ item.phone_number }}</p>
              </div>

              <div v-if="item.marital_status" class="bg-white p-3 rounded-lg border border-gray-200">
                <label class="block text-sm font-medium text-gray-700 mb-1">وضعیت تأهل</label>
                <p class="text-gray-900">{{ item.marital_status }}</p>
              </div>

              <div v-if="item.military_service_status" class="bg-white p-3 rounded-lg border border-gray-200">
                <label class="block text-sm font-medium text-gray-700 mb-1">وضعیت خدمت وظیفه</label>
                <p class="text-gray-900">{{ item.military_service_status }}</p>
              </div>

              <div v-if="item.physical_status" class="bg-white p-3 rounded-lg border border-gray-200">
                <label class="block text-sm font-medium text-gray-700 mb-1">وضعیت جسمانی</label>
                <p class="text-gray-900">{{ item.physical_status }}</p>
              </div>

              <div v-if="item.health_description" class="bg-white p-3 rounded-lg border border-gray-200">
                <label class="block text-sm font-medium text-gray-700 mb-1">توضیح سطح سلامت</label>
                <p class="text-gray-900">{{ item.health_description }}</p>
              </div>

              <div v-if="item.nationality" class="bg-white p-3 rounded-lg border border-gray-200">
                <label class="block text-sm font-medium text-gray-700 mb-1">ملیت</label>
                <p class="text-gray-900">{{ item.nationality }}</p>
              </div>

              <div v-if="item.activity_field" class="bg-white p-3 rounded-lg border border-gray-200">
                <label class="block text-sm font-medium text-gray-700 mb-1">حوزه فعالیت</label>
                <p class="text-gray-900">{{ item.activity_field }}</p>
              </div>

              <div v-if="item.educational_background" class="bg-white p-3 rounded-lg border border-gray-200">
                <label class="block text-sm font-medium text-gray-700 mb-1">سوابق تحصیلی</label>
                <p class="text-gray-900">{{ item.educational_background }}</p>
              </div>

              <div v-if="item.work_experience" class="bg-white p-3 rounded-lg border border-gray-200">
                <label class="block text-sm font-medium text-gray-700 mb-1">تجربیات شغلی</label>
                <p class="text-gray-900">{{ item.work_experience }}</p>
              </div>

              <div v-if="item.foreign_languages" class="bg-white p-3 rounded-lg border border-gray-200">
                <label class="block text-sm font-medium text-gray-700 mb-1">زبان های خارجی</label>
                <p class="text-gray-900">{{ item.foreign_languages }}</p>
              </div>

              <div v-if="item.certificates" class="bg-white p-3 rounded-lg border border-gray-200">
                <label class="block text-sm font-medium text-gray-700 mb-1">گواهینامه دوره های گذرانده شده</label>
                <p class="text-gray-900">{{ item.certificates }}</p>
              </div>

              <div v-if="item.requested_cooperation" class="bg-white p-3 rounded-lg border border-gray-200">
                <label class="block text-sm font-medium text-gray-700 mb-1">همکاری پیشنهادی مورد درخواست</label>
                <p class="text-gray-900">{{ item.requested_cooperation }}</p>
              </div>

              <div v-if="item.proposed_salary" class="bg-white p-3 rounded-lg border border-gray-200">
                <label class="block text-sm font-medium text-gray-700 mb-1">حقوق پیشنهادی</label>
                <p class="text-gray-900">{{ item.proposed_salary }}</p>
              </div>

              <div v-if="item.scientific_activities" class="bg-white p-3 rounded-lg border border-gray-200">
                <label class="block text-sm font-medium text-gray-700 mb-1">فعالیت های علمی</label>
                <p class="text-gray-900">{{ item.scientific_activities }}</p>
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
        </div>

        <!-- No Data State -->
        <div v-else class="text-center py-12">
          <svg class="w-16 h-16 mx-auto mb-4 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
          </svg>
          <h3 class="text-lg font-medium text-gray-900 mb-2">هیچ داده‌ای یافت نشد</h3>
          <p class="text-gray-500">هنوز هیچ داده‌ای برای این برنامه ذخیره نشده است.</p>
        </div>

        <!-- Pagination -->
        <div v-if="filteredData.length > itemsPerPage" class="mt-6 flex items-center justify-between">
          <div class="text-sm text-gray-700">
            نمایش {{ (currentPage - 1) * itemsPerPage + 1 }} تا {{ Math.min(currentPage * itemsPerPage, filteredData.length) }} از {{ filteredData.length }} مورد
          </div>
          <div class="flex items-center space-x-2 space-x-reverse">
            <button 
              @click="currentPage = Math.max(1, currentPage - 1)"
              :disabled="currentPage === 1"
              class="px-3 py-1 text-sm border border-gray-300 rounded-lg hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              قبلی
            </button>
            <span class="px-3 py-1 text-sm bg-blue-100 text-blue-800 rounded-lg">
              {{ currentPage }} از {{ totalPages }}
            </span>
            <button 
              @click="currentPage = Math.min(totalPages, currentPage + 1)"
              :disabled="currentPage === totalPages"
              class="px-3 py-1 text-sm border border-gray-300 rounded-lg hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              بعدی
            </button>
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

// Data
const data = ref([])
const users = ref([])
const loading = ref(false)

// Filters
const filters = ref({
  userId: null,
  dateFrom: '',
  dateTo: '',
  search: ''
})

// Pagination
const currentPage = ref(1)
const itemsPerPage = 10

// Computed
const filteredData = computed(() => {
  let filtered = data.value

  // User filter
  if (filters.value.userId) {
    filtered = filtered.filter(item => item.user_id === filters.value.userId)
  }

  // Date filters
  if (filters.value.dateFrom) {
    filtered = filtered.filter(item => {
      // Convert Persian date to Gregorian for comparison
      const persianDate = filters.value.dateFrom
      if (persianDate && persianDate.includes('/')) {
        const [year, month, day] = persianDate.split('/').map(Number)
        // Convert Persian date to Gregorian (simplified conversion)
        const gregorianDate = new Date(year + 621, month - 1, day)
        const itemDate = new Date(item.created_at)
        return itemDate >= gregorianDate
      }
      return true
    })
  }

  if (filters.value.dateTo) {
    filtered = filtered.filter(item => {
      // Convert Persian date to Gregorian for comparison
      const persianDate = filters.value.dateTo
      if (persianDate && persianDate.includes('/')) {
        const [year, month, day] = persianDate.split('/').map(Number)
        // Convert Persian date to Gregorian (simplified conversion)
        const gregorianDate = new Date(year + 621, month - 1, day)
        gregorianDate.setHours(23, 59, 59, 999) // End of day
        const itemDate = new Date(item.created_at)
        return itemDate <= gregorianDate
      }
      return true
    })
  }

  // Search filter
  if (filters.value.search) {
    const searchTerm = filters.value.search.toLowerCase()
    filtered = filtered.filter(item => 
      (item.first_name && item.first_name.toLowerCase().includes(searchTerm)) ||
      (item.last_name && item.last_name.toLowerCase().includes(searchTerm)) ||
      (item.national_id && item.national_id.includes(searchTerm)) ||
      (item.province && item.province.toLowerCase().includes(searchTerm)) ||
      (item.city && item.city.toLowerCase().includes(searchTerm)) ||
      (item.activity_field && item.activity_field.toLowerCase().includes(searchTerm))
    )
  }

  return filtered
})

const totalPages = computed(() => Math.ceil(filteredData.value.length / itemsPerPage))

const paginatedData = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage
  const end = start + itemsPerPage
  return filteredData.value.slice(start, end)
})

// Methods
const loadData = async () => {
  loading.value = true
  try {
    const response = await axios.get('/programs/404640758/all')
    data.value = response.data || []
  } catch (error) {
    console.error('Error loading data:', error)
    toast.error('خطا در بارگذاری داده‌ها')
  } finally {
    loading.value = false
  }
}

const loadUsers = async () => {
  if (authStore.user?.role === 'admin') {
    try {
      // Get users who have data in program 404640758
      const response = await axios.get('/programs/404640758/all')
      const programData = response.data || []
      
      // Extract unique users from the program data
      const userIds = [...new Set(programData.map(item => item.user_id))]
      
      // Get user details for these IDs
      const usersResponse = await axios.get('/users')
      const allUsers = usersResponse.data || []
      
      // Filter to only include users who have data in this program
      users.value = allUsers.filter(user => userIds.includes(user.id))
    } catch (error) {
      console.error('Error loading users:', error)
    }
  }
}

const applyFilters = () => {
  currentPage.value = 1 // Reset to first page when filtering
}

const clearFilters = () => {
  filters.value = {
    userId: null,
    dateFrom: '',
    dateTo: '',
    search: ''
  }
  currentPage.value = 1
}

const formatDate = (dateString) => {
  if (!dateString) return '-'
  const date = new Date(dateString)
  return date.toLocaleDateString('fa-IR', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const editItem = (item) => {
  emit('edit', item)
  closeModal()
}

const deleteItem = async (item) => {
  if (confirm('آیا از حذف این رکورد اطمینان دارید؟')) {
    try {
      await axios.delete(`/programs/404640758/${item.id}`)
      toast.success('رکورد با موفقیت حذف شد')
      await loadData()
    } catch (error) {
      console.error('Error deleting item:', error)
      toast.error('خطا در حذف رکورد')
    }
  }
}

const exportData = async () => {
  try {
    const response = await axios.get('/programs/404640758/export', {
      responseType: 'blob'
    })
    
    const url = window.URL.createObjectURL(new Blob([response.data]))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', 'program_404640758_data.xlsx')
    document.body.appendChild(link)
    link.click()
    link.remove()
    window.URL.revokeObjectURL(url)
    
    toast.success('فایل اکسل با موفقیت دانلود شد')
  } catch (error) {
    console.error('Error exporting data:', error)
    toast.error('خطا در دانلود فایل اکسل')
  }
}

const closeModal = () => {
  emit('close')
}

// Watch for modal open/close
watch(() => props.isOpen, (newValue) => {
  if (newValue) {
    loadData()
    loadUsers()
    currentPage.value = 1
  }
})

// Reset filters when modal closes
watch(() => props.isOpen, (newValue) => {
  if (!newValue) {
    clearFilters()
  }
})
</script>
