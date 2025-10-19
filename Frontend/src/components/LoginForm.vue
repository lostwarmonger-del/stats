<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-900 via-blue-800 to-indigo-900 flex items-center justify-center p-4">
    <div class="max-w-md w-full">
      <!-- Logo and Title -->
      <div class="text-center mb-8">
        <div class="w-20 h-20 bg-yellow-500 rounded-full flex items-center justify-center mx-auto mb-4">
          <font-awesome-icon icon="fas fa-crown" class="text-white text-3xl" />
        </div>
        <h1 class="text-3xl font-bold text-white mb-2">سیستم مدیریت</h1>
        <p class="text-blue-200">ورود به پنل مدیریت</p>
      </div>

      <!-- Login Form -->
      <div class="bg-white/10 backdrop-blur-lg rounded-2xl p-8 shadow-2xl border border-white/20">
        <form @submit.prevent="handleLogin" class="space-y-6">
          <!-- Initial Login Button -->
          <button
            v-if="!showCredentials"
            @click="showCredentials = true"
            type="button"
            class="w-full flex justify-center py-4 px-6 border border-transparent rounded-lg shadow-sm text-lg font-medium text-blue-900 bg-yellow-400 hover:bg-yellow-300 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-yellow-400 transition-all duration-300 transform hover:scale-105"
          >
            <font-awesome-icon icon="fas fa-sign-in-alt" class="ml-2" />
            ورود به سیستم
          </button>

          <!-- Username and Password Fields (shown after button click) -->
          <div v-if="showCredentials" class="space-y-6">
            <!-- Username Field -->
            <div>
              <label class="block text-white text-sm font-medium mb-2">نام کاربری</label>
              <div class="relative">
                <div class="absolute inset-y-0 right-0 pr-3 flex items-center pointer-events-none">
                  <font-awesome-icon icon="fas fa-user" class="h-5 w-5 text-blue-300" />
                </div>
                <input
                  v-model="form.username"
                  type="text"
                  required
                  class="block w-full pr-10 pl-3 py-3 bg-white/20 border border-white/30 rounded-lg text-white placeholder-blue-200 focus:outline-none focus:ring-2 focus:ring-yellow-400 focus:border-transparent transition-all duration-300"
                  placeholder="نام کاربری خود را وارد کنید"
                />
              </div>
            </div>

            <!-- Password Field -->
            <div>
              <label class="block text-white text-sm font-medium mb-2">رمز عبور</label>
              <div class="relative">
                <div class="absolute inset-y-0 right-0 pr-3 flex items-center pointer-events-none">
                  <font-awesome-icon icon="fas fa-lock" class="h-5 w-5 text-blue-300" />
                </div>
                <input
                  v-model="form.password"
                  type="password"
                  required
                  class="block w-full pr-10 pl-3 py-3 bg-white/20 border border-white/30 rounded-lg text-white placeholder-blue-200 focus:outline-none focus:ring-2 focus:ring-yellow-400 focus:border-transparent transition-all duration-300"
                  placeholder="رمز عبور خود را وارد کنید"
                />
              </div>
            </div>

            <!-- Login Button -->
            <button
              type="submit"
              :disabled="loading"
              class="w-full flex justify-center py-3 px-4 border border-transparent rounded-lg shadow-sm text-sm font-medium text-blue-900 bg-yellow-400 hover:bg-yellow-300 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-yellow-400 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-300 transform hover:scale-105"
            >
              <span v-if="loading" class="flex items-center">
                <font-awesome-icon icon="fas fa-spinner" class="animate-spin ml-2" />
                در حال ورود...
              </span>
              <span v-else class="flex items-center">
                <font-awesome-icon icon="fas fa-sign-in-alt" class="ml-2" />
                ورود به سیستم
              </span>
            </button>

            <!-- Back Button -->
            <button
              @click="showCredentials = false"
              type="button"
              class="w-full flex justify-center py-2 px-4 border border-white/30 rounded-lg text-sm font-medium text-white hover:bg-white/10 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-white/20 transition-all duration-300"
            >
              <font-awesome-icon icon="fas fa-arrow-right" class="ml-2" />
              بازگشت
            </button>
          </div>
        </form>

        <!-- Demo Credentials -->
        <div v-if="showCredentials" class="mt-6 p-4 bg-blue-500/20 rounded-lg border border-blue-400/30">
          <p class="text-blue-200 text-sm text-center">
            <font-awesome-icon icon="fas fa-info-circle" class="ml-1" />
            اطلاعات ورود: admin / admin123
          </p>
        </div>
      </div>

      <!-- Footer -->
      <div class="text-center mt-8">
        <p class="text-blue-300 text-sm">
          سیستم مدیریت پیشرفته - نسخه 1.0
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { useToast } from 'vue-toastification'

const router = useRouter()
const authStore = useAuthStore()
const toast = useToast()

const form = ref({
  username: '',
  password: ''
})

const loading = ref(false)
const showCredentials = ref(false)

const handleLogin = async () => {
  loading.value = true
  
  try {
    const result = await authStore.login(form.value)
    
    if (result.success) {
      toast.success('ورود موفقیت‌آمیز بود')
      router.push('/dashboard')
    } else {
      toast.error(result.error)
    }
  } catch (error) {
    toast.error('خطا در ورود به سیستم')
  } finally {
    loading.value = false
  }
}
</script>

