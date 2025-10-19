<template>
  <div v-if="isOpen" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
    <div class="bg-white rounded-2xl max-w-6xl w-full max-h-[90vh] overflow-hidden">
      <!-- Modal Header -->
      <div class="bg-gradient-to-r from-blue-600 to-indigo-700 p-6 text-white">
        <div class="flex items-center justify-between">
          <div>
            <h2 class="text-2xl font-bold">داده‌های ذخیره شده برنامه 403640724</h2>
            <p class="text-blue-100 mt-1">مشاهده و مدیریت اطلاعات ثبت شده</p>
          </div>
          <button
            @click="$emit('close')"
            class="text-white hover:text-gray-200 transition-colors"
          >
            <font-awesome-icon icon="fas fa-times" class="text-2xl" />
          </button>
        </div>
      </div>

      <!-- Modal Content -->
      <div class="p-6 overflow-y-auto max-h-[calc(90vh-120px)]">
        <!-- Loading State -->
        <div v-if="loading" class="text-center py-8">
          <font-awesome-icon icon="fas fa-spinner" class="animate-spin text-2xl text-blue-600 mb-4" />
          <p class="text-gray-600">در حال بارگذاری داده‌ها...</p>
        </div>

        <!-- Data Table -->
        <div v-else-if="data.length > 0" class="overflow-x-auto">
          <table class="min-w-full bg-white border border-gray-200 rounded-lg">
            <thead class="bg-gray-50">
              <tr>
                <th class="px-4 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider border-b">ردیف</th>
                <th class="px-4 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider border-b">نام رده</th>
                <th class="px-4 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider border-b">تلفن/ایمیل/تحت اقدام</th>
                <th class="px-4 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider border-b">تلگرام</th>
                <th class="px-4 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider border-b">اینستاگرام</th>
                <th class="px-4 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider border-b">روبیکا</th>
                <th class="px-4 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider border-b">سروش</th>
                <th class="px-4 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider border-b">واتس اپ</th>
                <th class="px-4 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider border-b">بله</th>
                <th class="px-4 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider border-b">آی گپ</th>
                <th class="px-4 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider border-b">شاد</th>
                <th class="px-4 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider border-b">ایتا</th>
                <th class="px-4 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider border-b">گپ</th>
                <th class="px-4 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider border-b">سایر شبکه‌ها</th>
                <th class="px-4 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider border-b">Gmail</th>
                <th class="px-4 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider border-b">Yahoo</th>
                <th class="px-4 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider border-b">Microsoft</th>
                <th class="px-4 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider border-b">سایر ایمیل‌ها</th>
                <th class="px-4 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider border-b">شماره خبر‌ها</th>
                <th class="px-4 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider border-b">نتیجه پرونده</th>
                <th class="px-4 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider border-b">تاریخ ایجاد</th>
                <th class="px-4 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider border-b">عملیات</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-200">
              <tr v-for="(item, index) in paginatedData" :key="item.id" class="hover:bg-gray-50">
                <td class="px-4 py-3 text-sm text-gray-900">{{ item.row_number || '-' }}</td>
                <td class="px-4 py-3 text-sm text-gray-900">{{ item.category_name || '-' }}</td>
                <td class="px-4 py-3 text-sm text-gray-900">{{ item.phone_email_action || '-' }}</td>
                <td class="px-4 py-3 text-sm text-gray-900 text-center">{{ toPersianNumbers(item.telegram_count || 0) }}</td>
                <td class="px-4 py-3 text-sm text-gray-900 text-center">{{ toPersianNumbers(item.instagram_count || 0) }}</td>
                <td class="px-4 py-3 text-sm text-gray-900 text-center">{{ toPersianNumbers(item.rubika_count || 0) }}</td>
                <td class="px-4 py-3 text-sm text-gray-900 text-center">{{ toPersianNumbers(item.soroush_count || 0) }}</td>
                <td class="px-4 py-3 text-sm text-gray-900 text-center">{{ toPersianNumbers(item.whatsapp_count || 0) }}</td>
                <td class="px-4 py-3 text-sm text-gray-900 text-center">{{ toPersianNumbers(item.bale_count || 0) }}</td>
                <td class="px-4 py-3 text-sm text-gray-900 text-center">{{ toPersianNumbers(item.igap_count || 0) }}</td>
                <td class="px-4 py-3 text-sm text-gray-900 text-center">{{ toPersianNumbers(item.shad_count || 0) }}</td>
                <td class="px-4 py-3 text-sm text-gray-900 text-center">{{ toPersianNumbers(item.eitaa_count || 0) }}</td>
                <td class="px-4 py-3 text-sm text-gray-900 text-center">{{ toPersianNumbers(item.gap_count || 0) }}</td>
                <td class="px-4 py-3 text-sm text-gray-900 text-center">{{ toPersianNumbers(item.other_virtual_networks_count || 0) }}</td>
                <td class="px-4 py-3 text-sm text-gray-900 text-center">{{ toPersianNumbers(item.gmail_count || 0) }}</td>
                <td class="px-4 py-3 text-sm text-gray-900 text-center">{{ toPersianNumbers(item.yahoo_count || 0) }}</td>
                <td class="px-4 py-3 text-sm text-gray-900 text-center">{{ toPersianNumbers(item.microsoft_count || 0) }}</td>
                <td class="px-4 py-3 text-sm text-gray-900 text-center">{{ toPersianNumbers(item.other_emails_count || 0) }}</td>
                <td class="px-4 py-3 text-sm text-gray-900 max-w-xs truncate">{{ item.registered_news_numbers || '-' }}</td>
                <td class="px-4 py-3 text-sm text-gray-900 max-w-xs truncate">{{ item.final_case_result || '-' }}</td>
                <td class="px-4 py-3 text-sm text-gray-500">{{ formatDate(item.created_at) }}</td>
                <td class="px-4 py-3 text-sm text-gray-900">
                  <div class="flex space-x-2 space-x-reverse">
                    <button
                      @click="editItem(item)"
                      class="text-blue-600 hover:text-blue-800 transition-colors"
                      title="ویرایش"
                    >
                      <font-awesome-icon icon="fas fa-edit" />
                    </button>
                    <button
                      @click="deleteItem(item.id)"
                      class="text-red-600 hover:text-red-800 transition-colors"
                      title="حذف"
                    >
                      <font-awesome-icon icon="fas fa-trash" />
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>

          <!-- Pagination -->
          <div v-if="totalPages > 1" class="mt-6 flex items-center justify-between">
            <div class="text-sm text-gray-700">
              نمایش {{ (currentPage - 1) * itemsPerPage + 1 }} تا {{ Math.min(currentPage * itemsPerPage, data.length) }} از {{ data.length }} رکورد
            </div>
            <div class="flex space-x-2 space-x-reverse">
              <button
                @click="currentPage = Math.max(1, currentPage - 1)"
                :disabled="currentPage === 1"
                class="px-3 py-2 text-sm font-medium text-gray-500 bg-white border border-gray-300 rounded-md hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                قبلی
              </button>
              <span class="px-3 py-2 text-sm font-medium text-gray-700">
                صفحه {{ currentPage }} از {{ totalPages }}
              </span>
              <button
                @click="currentPage = Math.min(totalPages, currentPage + 1)"
                :disabled="currentPage === totalPages"
                class="px-3 py-2 text-sm font-medium text-gray-500 bg-white border border-gray-300 rounded-md hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                بعدی
              </button>
            </div>
          </div>
        </div>

        <!-- Empty State -->
        <div v-else class="text-center py-12">
          <font-awesome-icon icon="fas fa-inbox" class="text-4xl text-gray-400 mb-4" />
          <h3 class="text-lg font-medium text-gray-900 mb-2">هیچ داده‌ای یافت نشد</h3>
          <p class="text-gray-500">هنوز هیچ اطلاعاتی برای این برنامه ثبت نشده است.</p>
        </div>
      </div>

      <!-- Modal Footer -->
      <div class="bg-gray-50 px-6 py-4 border-t border-gray-200">
        <div class="flex justify-end">
          <button
            @click="$emit('close')"
            class="px-6 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700 transition-colors"
          >
            بستن
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useToast } from 'vue-toastification'
import axios from 'axios'

const props = defineProps({
  isOpen: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['close', 'edit'])

const toast = useToast()
const loading = ref(false)
const data = ref([])
const currentPage = ref(1)
const itemsPerPage = 10

const paginatedData = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage
  const end = start + itemsPerPage
  return data.value.slice(start, end)
})

const totalPages = computed(() => {
  return Math.ceil(data.value.length / itemsPerPage)
})

const formatDate = (dateString) => {
  if (!dateString) return '-'
  const date = new Date(dateString)
  return date.toLocaleString('fa-IR', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

// Persian number formatting function
const toPersianNumbers = (str) => {
  if (!str) return '۰'
  return str.toString().replace(/[0-9]/g, (digit) => {
    return String.fromCharCode(digit.charCodeAt(0) + 1728)
  })
}

const loadData = async () => {
  loading.value = true
  try {
    const response = await axios.get('/programs/403640724/all')
    data.value = response.data || []
  } catch (error) {
    console.error('Error loading data:', error)
    toast.error('خطا در بارگذاری داده‌ها')
    data.value = []
  } finally {
    loading.value = false
  }
}

const editItem = (item) => {
  emit('edit', item)
  emit('close')
}

const deleteItem = async (id) => {
  if (!confirm('آیا از حذف این رکورد اطمینان دارید؟')) {
    return
  }

  try {
    // Find the user_id for this record
    const item = data.value.find(d => d.id === id)
    if (!item) {
      toast.error('رکورد مورد نظر یافت نشد')
      return
    }

    await axios.delete(`/programs/403640724/${item.user_id}`)
    toast.success('رکورد با موفقیت حذف شد')
    await loadData() // Reload data
  } catch (error) {
    console.error('Error deleting item:', error)
    toast.error('خطا در حذف رکورد')
  }
}

onMounted(() => {
  if (props.isOpen) {
    loadData()
  }
})

// Watch for modal open/close to load data
import { watch } from 'vue'
watch(() => props.isOpen, (newValue) => {
  if (newValue) {
    loadData()
    currentPage.value = 1 // Reset pagination
  }
})
</script>
