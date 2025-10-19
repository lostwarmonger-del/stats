<!-- ShamsiDatePicker.vue - Persian date picker component -->
<template>
  <div class="relative">
    <input
      :value="formattedDate"
      @input="handleInput"
      @focus="showCalendar = true"
      @blur="handleBlur"
      :placeholder="placeholder"
      :class="inputClass"
      readonly
    />
    
    <!-- Calendar Icon -->
    <div class="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400">
      <font-awesome-icon icon="fas fa-calendar-alt" />
    </div>
    
    <!-- Calendar Dropdown -->
    <div 
      v-if="showCalendar" 
      @mousedown.prevent
      class="calendar-dropdown absolute top-full left-0 mt-1 bg-white border border-gray-300 rounded-lg shadow-lg z-50 p-4 min-w-80"
    >
      <!-- Calendar Header -->
      <div class="flex items-center justify-between mb-4">
        <button 
          @click="previousMonth($event)" 
          type="button"
          class="p-2 hover:bg-gray-100 rounded-lg transition-colors"
        >
          <font-awesome-icon icon="fas fa-chevron-right" />
        </button>
        
        <h3 class="text-lg font-semibold text-gray-900">
          {{ persianMonths[currentMonth - 1] }} {{ currentYear }}
        </h3>
        
        <button 
          @click="nextMonth($event)" 
          type="button"
          class="p-2 hover:bg-gray-100 rounded-lg transition-colors"
        >
          <font-awesome-icon icon="fas fa-chevron-left" />
        </button>
      </div>
      
      <!-- Calendar Grid -->
      <div class="grid grid-cols-7 gap-1 mb-2">
        <div 
          v-for="day in weekDays" 
          :key="day" 
          class="text-center text-sm font-medium text-gray-500 py-2"
        >
          {{ day }}
        </div>
      </div>
      
      <div class="grid grid-cols-7 gap-1">
        <button
          v-for="day in calendarDays"
          :key="day.value"
          @click="selectDate(day, $event)"
          type="button"
          :class="[
            'p-2 text-sm rounded-lg transition-colors',
            day.isCurrentMonth 
              ? 'text-gray-900 hover:bg-blue-100' 
              : 'text-gray-400',
            day.isToday 
              ? 'bg-blue-500 text-white font-semibold' 
              : '',
            day.isSelected 
              ? 'bg-blue-600 text-white font-semibold' 
              : ''
          ]"
        >
          {{ day.value }}
        </button>
      </div>
      
      <!-- Today Button -->
      <div class="mt-4 pt-4 border-t border-gray-200">
        <button 
          @click="selectToday($event)" 
          type="button"
          class="w-full py-2 px-4 bg-gray-100 hover:bg-gray-200 text-gray-700 rounded-lg transition-colors"
        >
          امروز
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'

const props = defineProps({
  modelValue: {
    type: String,
    default: ''
  },
  placeholder: {
    type: String,
    default: 'تاریخ شمسی را انتخاب کنید'
  },
  inputClass: {
    type: String,
    default: 'w-full px-4 py-3 pr-10 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent'
  }
})

const emit = defineEmits(['update:modelValue'])

const showCalendar = ref(false)
const currentYear = ref(1403)
const currentMonth = ref(1)
const selectedDate = ref('')

// Get current Persian date from server
const getCurrentPersianDate = async () => {
  try {
    const response = await axios.get('/current-date')
    if (response.data && response.data.persian_date) {
      const [year, month, day] = response.data.persian_date.split('/').map(Number)
      currentYear.value = year
      currentMonth.value = month
      return { year, month, day }
    }
  } catch (error) {
    console.error('Error fetching current date:', error)
  }
  
  // Fallback to approximate current Persian date
  const now = new Date()
  const persianYear = 1403 // Approximate
  const persianMonth = Math.floor(Math.random() * 12) + 1 // Random month for fallback
  const persianDay = Math.floor(Math.random() * 28) + 1 // Random day for fallback
  
  currentYear.value = persianYear
  currentMonth.value = persianMonth
  return { year: persianYear, month: persianMonth, day: persianDay }
}

// Persian calendar data
const persianMonths = [
  'فروردین', 'اردیبهشت', 'خرداد', 'تیر', 'مرداد', 'شهریور',
  'مهر', 'آبان', 'آذر', 'دی', 'بهمن', 'اسفند'
]

const weekDays = ['ش', 'ی', 'د', 'س', 'چ', 'پ', 'ج']

// Persian month days
const persianMonthDays = [31, 31, 31, 31, 31, 31, 30, 30, 30, 30, 30, 29]

const formattedDate = computed(() => {
  if (!selectedDate.value) return ''
  const [year, month, day] = selectedDate.value.split('/')
  return `${year}/${month.padStart(2, '0')}/${day.padStart(2, '0')}`
})

const calendarDays = computed(() => {
  const days = []
  const daysInMonth = persianMonthDays[currentMonth.value - 1]
  
  // Add previous month days
  const prevMonth = currentMonth.value === 1 ? 12 : currentMonth.value - 1
  const prevMonthDays = persianMonthDays[prevMonth - 1]
  
  for (let i = prevMonthDays - 6; i <= prevMonthDays; i++) {
    days.push({
      value: i,
      isCurrentMonth: false,
      isToday: false,
      isSelected: false,
      isClickable: true
    })
  }
  
  // Add current month days
  for (let i = 1; i <= daysInMonth; i++) {
    const dateStr = `${currentYear.value}/${currentMonth.value}/${i}`
    const isToday = isTodayDate(dateStr)
    const isSelected = selectedDate.value === dateStr
    
    days.push({
      value: i,
      isCurrentMonth: true,
      isToday,
      isSelected,
      isClickable: true
    })
  }
  
  // Add next month days to fill grid
  const remainingDays = 42 - days.length
  for (let i = 1; i <= remainingDays; i++) {
    days.push({
      value: i,
      isCurrentMonth: false,
      isToday: false,
      isSelected: false,
      isClickable: true
    })
  }
  
  return days
})

const isTodayDate = (dateStr) => {
  // Check if the date matches today's date
  const today = new Date()
  const todayStr = `${currentYear.value}/${currentMonth.value}/${today.getDate()}`
  return dateStr === todayStr
}

const selectDate = (day, event) => {
  // Prevent any form submission
  if (event) {
    event.preventDefault()
    event.stopPropagation()
  }
  
  // Allow selecting any day, not just current month
  const dateStr = `${currentYear.value}/${currentMonth.value}/${day.value}`
  selectedDate.value = dateStr
  emit('update:modelValue', formattedDate.value)
  // Only close calendar when selecting a date
  showCalendar.value = false
}

const selectToday = async (event) => {
  if (event) {
    event.preventDefault()
    event.stopPropagation()
  }
  
  const currentDate = await getCurrentPersianDate()
  const dateStr = `${currentDate.year}/${currentDate.month}/${currentDate.day}`
  selectedDate.value = dateStr
  emit('update:modelValue', formattedDate.value)
  showCalendar.value = false
}

const previousMonth = (event) => {
  if (event) {
    event.preventDefault()
    event.stopPropagation()
  }
  
  if (currentMonth.value === 1) {
    currentMonth.value = 12
    currentYear.value--
  } else {
    currentMonth.value--
  }
  // Don't close calendar when navigating
}

const nextMonth = (event) => {
  if (event) {
    event.preventDefault()
    event.stopPropagation()
  }
  
  if (currentMonth.value === 12) {
    currentMonth.value = 1
    currentYear.value++
  } else {
    currentMonth.value++
  }
  // Don't close calendar when navigating
}

const handleInput = (event) => {
  // Prevent this from triggering form validation
  event.stopPropagation()
  
  const value = event.target.value
  // Basic validation for Persian date format
  if (/^\d{4}\/\d{1,2}\/\d{1,2}$/.test(value)) {
    selectedDate.value = value
    emit('update:modelValue', value)
  }
}

const handleBlur = (event) => {
  // Check if the blur is caused by clicking inside the calendar
  const calendarElement = event.relatedTarget?.closest('.calendar-dropdown')
  if (calendarElement) {
    // Don't close if clicking inside calendar
    return
  }
  
  // Delay hiding calendar to allow clicks outside
  setTimeout(() => {
    showCalendar.value = false
  }, 200)
}

// Initialize with current value
onMounted(async () => {
  if (props.modelValue) {
    selectedDate.value = props.modelValue
  } else {
    // Initialize with current Persian date
    await getCurrentPersianDate()
  }
})
</script>
