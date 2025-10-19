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
              <h1 class="text-3xl font-bold mb-2">مدیریت کاربران</h1>
              <p class="text-blue-100 text-lg">مشاهده لیست کاربران سیستم</p>
            </div>
            <div class="w-20 h-20 bg-white/20 rounded-full flex items-center justify-center">
              <font-awesome-icon icon="fas fa-users" class="text-4xl text-yellow-400" />
            </div>
          </div>
        </div>

        <!-- Users Table -->
        <div class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
          <div class="px-6 py-4 border-b border-gray-200 flex justify-between items-center">
            <div>
              <h2 class="text-xl font-bold text-gray-900">لیست کاربران</h2>
              <p class="text-gray-600 text-sm mt-1">تمام کاربران ثبت شده در سیستم</p>
            </div>
            <!-- Only show add user button for admins -->
            <button 
              v-if="authStore.user?.role === 'admin'"
              @click="showCreateForm = true"
              class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg transition-colors flex items-center space-x-2 space-x-reverse"
            >
              <font-awesome-icon icon="fas fa-plus" class="text-sm" />
              <span>کاربر جدید</span>
            </button>
          </div>
          
          <div v-if="loading" class="p-8 text-center">
            <font-awesome-icon icon="fas fa-spinner" class="animate-spin text-2xl text-blue-600 mb-4" />
            <p class="text-gray-600">در حال بارگذاری...</p>
          </div>
          
          <div v-else-if="error" class="p-8 text-center">
            <font-awesome-icon icon="fas fa-exclamation-triangle" class="text-2xl text-red-500 mb-4" />
            <p class="text-red-600">{{ error }}</p>
          </div>
          
          <div v-else class="overflow-x-auto">
            <table class="w-full">
              <thead class="bg-gray-50">
                <tr>
                  <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">نام کاربری</th>
                  <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">نام</th>
                  <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">نقش</th>
                  <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">وضعیت</th>
                  <th v-if="authStore.user?.role === 'admin' || authStore.user?.id === 1" class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">عملیات</th>
                </tr>
              </thead>
              <tbody class="bg-white divide-y divide-gray-200">
                <tr v-for="user in users" :key="user.id" class="hover:bg-gray-50">
                  <td class="px-6 py-4 whitespace-nowrap">
                    <div class="flex items-center">
                      <div class="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center ml-3">
                        <font-awesome-icon icon="fas fa-user" class="text-blue-600 text-sm" />
                      </div>
                      <div class="text-sm font-medium text-gray-900">{{ user.username }}</div>
                    </div>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{{ user.name }}</td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <span :class="getRoleBadgeClass(user.role)" class="inline-flex px-2 py-1 text-xs font-semibold rounded-full">
                      {{ getRoleText(user.role) }}
                    </span>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <!-- Clickable status for admins, static for regular users -->
                    <button 
                      v-if="authStore.user?.role === 'admin' && user.id !== currentUserId"
                      @click="toggleUserStatus(user)"
                      :class="user.is_active ? 'bg-green-100 text-green-800 hover:bg-green-200' : 'bg-red-100 text-red-800 hover:bg-red-200'" 
                      class="inline-flex px-2 py-1 text-xs font-semibold rounded-full transition-colors cursor-pointer"
                      :title="user.is_active ? 'کلیک برای غیرفعال کردن' : 'کلیک برای فعال کردن'"
                    >
                      {{ user.is_active ? 'فعال' : 'غیرفعال' }}
                    </button>
                    <span 
                      v-else
                      :class="user.is_active ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'" 
                      class="inline-flex px-2 py-1 text-xs font-semibold rounded-full"
                    >
                      {{ user.is_active ? 'فعال' : 'غیرفعال' }}
                    </span>
                  </td>
                  <td v-if="authStore.user?.role === 'admin' || authStore.user?.id === 1" class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                    <div class="flex items-center space-x-2 space-x-reverse">
                      <!-- Edit button - show for admins or user ID 1 -->
                      <button 
                        @click="openEditForm(user)"
                        class="text-blue-600 hover:text-blue-900 transition-colors"
                        title="ویرایش کاربر"
                      >
                        <font-awesome-icon icon="fas fa-edit" class="text-lg" />
                      </button>
                      
                      <!-- Delete button - only for admins -->
                      <button 
                        v-if="authStore.user?.role === 'admin'"
                        @click="confirmDelete(user)"
                        class="text-red-600 hover:text-red-900 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                        :disabled="user.id === currentUserId"
                        :title="user.id === currentUserId ? 'نمی‌توانید خودتان را حذف کنید' : 'حذف کاربر'"
                      >
                        <font-awesome-icon icon="fas fa-trash" class="text-lg" />
                      </button>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
          
          <div v-if="users.length === 0 && !loading" class="p-8 text-center">
            <font-awesome-icon icon="fas fa-users" class="text-4xl text-gray-300 mb-4" />
            <p class="text-gray-500">هیچ کاربری یافت نشد</p>
          </div>
        </div>

        <!-- Create User Modal -->
        <div v-if="showCreateForm" class="fixed inset-0 bg-black/60 z-50 flex items-center justify-center p-4">
          <div class="bg-white rounded-2xl shadow-2xl max-w-lg w-full overflow-hidden">
            <!-- Modal Header -->
            <div class="bg-gradient-to-r from-blue-600 to-indigo-700 px-8 py-6">
              <div class="flex items-center justify-between">
                <div class="flex items-center space-x-3 space-x-reverse">
                  <div class="w-10 h-10 bg-white/20 rounded-full flex items-center justify-center">
                    <font-awesome-icon icon="fas fa-user-plus" class="text-white text-lg" />
                  </div>
                  <div>
                    <h3 class="text-xl font-bold text-white">ایجاد کاربر جدید</h3>
                    <p class="text-blue-100 text-sm">اطلاعات کاربر جدید را وارد کنید</p>
                  </div>
                </div>
                <button 
                  @click="closeCreateForm"
                  class="text-white/80 hover:text-white transition-colors p-2 hover:bg-white/10 rounded-lg"
                >
                  <font-awesome-icon icon="fas fa-times" class="text-xl" />
                </button>
              </div>
            </div>
            
            <!-- Modal Body -->
            <div class="p-8">
              <form @submit.prevent="createUser" class="space-y-6">
                <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div>
                    <label class="block text-sm font-semibold text-gray-700 mb-2">
                      <font-awesome-icon icon="fas fa-user" class="text-blue-600 ml-2" />
                      نام کاربری
                    </label>
                    <input
                      v-model="newUser.username"
                      type="text"
                      required
                      class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
                      placeholder="نام کاربری را وارد کنید"
                    />
                  </div>
                  
                  <div>
                    <label class="block text-sm font-semibold text-gray-700 mb-2">
                      <font-awesome-icon icon="fas fa-id-card" class="text-blue-600 ml-2" />
                      نام کامل
                    </label>
                    <input
                      v-model="newUser.name"
                      type="text"
                      required
                      class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
                      placeholder="نام کامل را وارد کنید"
                    />
                  </div>
                </div>
                
                <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div>
                    <label class="block text-sm font-semibold text-gray-700 mb-2">
                      <font-awesome-icon icon="fas fa-lock" class="text-blue-600 ml-2" />
                      رمز عبور
                    </label>
                    <input
                      v-model="newUser.password"
                      type="password"
                      required
                      class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
                      placeholder="رمز عبور را وارد کنید"
                    />
                  </div>
                  
                  <div>
                    <label class="block text-sm font-semibold text-gray-700 mb-2">
                      <font-awesome-icon icon="fas fa-user-tag" class="text-blue-600 ml-2" />
                      نقش کاربر
                    </label>
                    <select
                      v-model="newUser.role"
                      required
                      class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
                    >
                      <option value="user">کاربر عادی</option>
                      <option value="admin">مدیر سیستم</option>
                    </select>
                  </div>
                </div>
                
                <!-- Action Buttons -->
                <div class="flex space-x-4 space-x-reverse pt-6 border-t border-gray-200">
                  <button
                    type="submit"
                    :disabled="creating"
                    class="flex-1 bg-gradient-to-r from-blue-600 to-indigo-700 hover:from-blue-700 hover:to-indigo-800 text-white py-3 px-6 rounded-xl transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed font-semibold flex items-center justify-center space-x-2 space-x-reverse"
                  >
                    <font-awesome-icon v-if="creating" icon="fas fa-spinner" class="animate-spin" />
                    <font-awesome-icon v-else icon="fas fa-check" />
                    <span>{{ creating ? 'در حال ایجاد...' : 'ایجاد کاربر' }}</span>
                  </button>
                  <button
                    type="button"
                    @click="closeCreateForm"
                    class="flex-1 bg-gray-100 hover:bg-gray-200 text-gray-700 py-3 px-6 rounded-xl transition-all duration-200 font-semibold flex items-center justify-center space-x-2 space-x-reverse"
                  >
                    <font-awesome-icon icon="fas fa-times" />
                    <span>انصراف</span>
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>

        <!-- Delete Confirmation Modal -->
        <div v-if="showDeleteModal" class="fixed inset-0 bg-black/60 z-50 flex items-center justify-center p-4">
          <div class="bg-white rounded-2xl shadow-2xl max-w-md w-full overflow-hidden">
            <!-- Modal Header -->
            <div class="bg-gradient-to-r from-red-600 to-red-700 px-8 py-6">
              <div class="flex items-center justify-between">
                <div class="flex items-center space-x-3 space-x-reverse">
                  <div class="w-10 h-10 bg-white/20 rounded-full flex items-center justify-center">
                    <font-awesome-icon icon="fas fa-exclamation-triangle" class="text-white text-lg" />
                  </div>
                  <div>
                    <h3 class="text-xl font-bold text-white">تأیید حذف کاربر</h3>
                    <p class="text-red-100 text-sm">این عمل قابل بازگشت نیست</p>
                  </div>
                </div>
                <button 
                  @click="closeDeleteModal"
                  class="text-white/80 hover:text-white transition-colors p-2 hover:bg-white/10 rounded-lg"
                >
                  <font-awesome-icon icon="fas fa-times" class="text-xl" />
                </button>
              </div>
            </div>
            
            <!-- Modal Body -->
            <div class="p-8">
              <div class="text-center mb-6">
                <div class="w-16 h-16 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-4">
                  <font-awesome-icon icon="fas fa-user-times" class="text-red-600 text-2xl" />
                </div>
                <h4 class="text-lg font-semibold text-gray-900 mb-2">آیا مطمئن هستید؟</h4>
                <p class="text-gray-600">
                  کاربر <span class="font-semibold text-gray-900">{{ userToDelete?.name }}</span> 
                  با نام کاربری <span class="font-semibold text-gray-900">{{ userToDelete?.username }}</span> 
                  حذف خواهد شد.
                </p>
              </div>
              
              <!-- Action Buttons -->
              <div class="flex space-x-4 space-x-reverse">
                <button
                  @click="deleteUser"
                  :disabled="deleting"
                  class="flex-1 bg-gradient-to-r from-red-600 to-red-700 hover:from-red-700 hover:to-red-800 text-white py-3 px-6 rounded-xl transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed font-semibold flex items-center justify-center space-x-2 space-x-reverse"
                >
                  <font-awesome-icon v-if="deleting" icon="fas fa-spinner" class="animate-spin" />
                  <font-awesome-icon v-else icon="fas fa-trash" />
                  <span>{{ deleting ? 'در حال حذف...' : 'حذف کاربر' }}</span>
                </button>
                <button
                  @click="closeDeleteModal"
                  class="flex-1 bg-gray-100 hover:bg-gray-200 text-gray-700 py-3 px-6 rounded-xl transition-all duration-200 font-semibold flex items-center justify-center space-x-2 space-x-reverse"
                >
                  <font-awesome-icon icon="fas fa-times" />
                  <span>انصراف</span>
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Edit User Modal -->
        <div v-if="showEditForm" class="fixed inset-0 bg-black/60 z-50 flex items-center justify-center p-4">
          <div class="bg-white rounded-2xl shadow-2xl max-w-lg w-full overflow-hidden">
            <!-- Modal Header -->
            <div class="bg-gradient-to-r from-blue-600 to-indigo-700 px-8 py-6">
              <div class="flex items-center justify-between">
                <div class="flex items-center space-x-3 space-x-reverse">
                  <div class="w-10 h-10 bg-white/20 rounded-full flex items-center justify-center">
                    <font-awesome-icon icon="fas fa-user-edit" class="text-white text-lg" />
                  </div>
                  <div>
                    <h3 class="text-xl font-bold text-white">ویرایش کاربر</h3>
                    <p class="text-blue-100 text-sm">ویرایش اطلاعات {{ userToEdit?.name }}</p>
                  </div>
                </div>
                <button 
                  @click="closeEditForm"
                  class="text-white/80 hover:text-white transition-colors p-2 hover:bg-white/10 rounded-lg"
                >
                  <font-awesome-icon icon="fas fa-times" class="text-xl" />
                </button>
              </div>
            </div>
            
            <!-- Modal Body -->
            <div class="p-8">
              <form @submit.prevent="updateUser" class="space-y-6">
                <!-- Name Field -->
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">نام کامل</label>
                  <input 
                    v-model="editUser.name"
                    type="text" 
                    required
                    class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
                    placeholder="نام کامل کاربر را وارد کنید"
                  />
                </div>
                
                <!-- Password Field -->
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">رمز عبور جدید</label>
                  <input 
                    v-model="editUser.password"
                    type="password" 
                    class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
                    placeholder="رمز عبور جدید (اختیاری)"
                  />
                  <p class="text-xs text-gray-500 mt-1">اگر رمز عبور را تغییر نمی‌دهید، این فیلد را خالی بگذارید</p>
                </div>
                
                <!-- Role Field (Only for admins) -->
                <div v-if="authStore.user?.role === 'admin'">
                  <label class="block text-sm font-medium text-gray-700 mb-2">نقش کاربر</label>
                  <select 
                    v-model="editUser.role"
                    class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
                  >
                    <option value="user">کاربر عادی</option>
                    <option value="admin">مدیر سیستم</option>
                  </select>
                </div>
                
                <!-- Action Buttons -->
                <div class="flex space-x-4 space-x-reverse pt-4">
                  <button
                    type="submit"
                    :disabled="editing || !editUser.name.trim()"
                    class="flex-1 bg-gradient-to-r from-blue-600 to-indigo-700 hover:from-blue-700 hover:to-indigo-800 text-white py-3 px-6 rounded-xl transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed font-semibold flex items-center justify-center space-x-2 space-x-reverse"
                  >
                    <font-awesome-icon v-if="editing" icon="fas fa-spinner" class="animate-spin" />
                    <font-awesome-icon v-else icon="fas fa-save" />
                    <span>{{ editing ? 'در حال ذخیره...' : 'ذخیره تغییرات' }}</span>
                  </button>
                  <button
                    type="button"
                    @click="closeEditForm"
                    class="flex-1 bg-gray-100 hover:bg-gray-200 text-gray-700 py-3 px-6 rounded-xl transition-all duration-200 font-semibold flex items-center justify-center space-x-2 space-x-reverse"
                  >
                    <font-awesome-icon icon="fas fa-times" />
                    <span>انصراف</span>
                  </button>
                </div>
              </form>
            </div>
          </div>
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
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { useToast } from 'vue-toastification'
import Sidebar from './Sidebar.vue'
import AppHeader from './AppHeader.vue'
import axios from 'axios'

const router = useRouter()
const authStore = useAuthStore()
const toast = useToast()
const sidebarOpen = ref(false)
const users = ref([])
const loading = ref(false)
const error = ref('')
const showCreateForm = ref(false)
const creating = ref(false)
const showDeleteModal = ref(false)
const deleting = ref(false)
const userToDelete = ref(null)
const showEditForm = ref(false)
const editing = ref(false)
const userToEdit = ref(null)

const newUser = ref({
  username: '',
  name: '',
  password: '',
  role: 'user'
})

const editUser = ref({
  name: '',
  password: '',
  role: ''
})

const currentUserId = computed(() => {
  return authStore.user?.id
})

const toggleSidebar = () => {
  sidebarOpen.value = !sidebarOpen.value
}

const closeCreateForm = () => {
  showCreateForm.value = false
  newUser.value = {
    username: '',
    name: '',
    password: '',
    role: 'user'
  }
}

const createUser = async () => {
  creating.value = true
  
  try {
    console.log('Sending user data:', newUser.value)
    const response = await axios.post('/users', newUser.value)
    // Refresh the entire user list to ensure consistency
    await fetchUsers()
    toast.success('کاربر با موفقیت ایجاد شد')
    closeCreateForm()
  } catch (err) {
    console.error('Error creating user:', err.response?.data)
    console.error('Full error:', err)
    let errorMessage = 'خطا در ایجاد کاربر'
    
    if (err.response?.data?.detail) {
      if (Array.isArray(err.response.data.detail)) {
        console.log('Validation errors:', err.response.data.detail)
        errorMessage = err.response.data.detail.map(d => {
          if (typeof d === 'object') {
            return `${d.loc ? d.loc.join('.') : 'field'}: ${d.msg || d.type || 'error'}`
          }
          return d
        }).join(', ')
      } else {
        errorMessage = err.response.data.detail
      }
    }
    
    toast.error(errorMessage)
  } finally {
    creating.value = false
  }
}

const confirmDelete = (user) => {
  userToDelete.value = user
  showDeleteModal.value = true
}

const closeDeleteModal = () => {
  showDeleteModal.value = false
  userToDelete.value = null
}

const openEditForm = (user) => {
  userToEdit.value = user
  editUser.value = {
    name: user.name,
    password: '',
    role: user.role
  }
  showEditForm.value = true
}

const closeEditForm = () => {
  showEditForm.value = false
  userToEdit.value = null
  editUser.value = {
    name: '',
    password: '',
    role: ''
  }
}

const updateUser = async () => {
  if (!userToEdit.value) return
  
  editing.value = true
  
  try {
    const updateData = {
      name: editUser.value.name
    }
    
    // Only include password if it's provided
    if (editUser.value.password && editUser.value.password.trim()) {
      updateData.password = editUser.value.password
    }
    
    // Only include role if user is admin
    if (authStore.user?.role === 'admin') {
      updateData.role = editUser.value.role
    }
    
    await axios.patch(`/users/${userToEdit.value.id}/edit`, updateData)
    await fetchUsers()
    toast.success('اطلاعات کاربر با موفقیت به‌روزرسانی شد')
    closeEditForm()
  } catch (err) {
    const errorMessage = err.response?.data?.detail || 'خطا در به‌روزرسانی کاربر'
    toast.error(errorMessage)
  } finally {
    editing.value = false
  }
}

const deleteUser = async () => {
  if (!userToDelete.value) return
  
  deleting.value = true
  
  try {
    await axios.delete(`/users/${userToDelete.value.id}`)
    // Refresh the entire user list to ensure consistency
    await fetchUsers()
    toast.success('کاربر با موفقیت حذف شد')
    closeDeleteModal()
  } catch (err) {
    const errorMessage = err.response?.data?.detail || 'خطا در حذف کاربر'
    toast.error(errorMessage)
  } finally {
    deleting.value = false
  }
}

const toggleUserStatus = async (user) => {
  try {
    const response = await axios.patch(`/users/${user.id}/toggle-status`)
    // Refresh the entire user list to ensure consistency
    await fetchUsers()
    toast.success(response.data.message)
  } catch (err) {
    const errorMessage = err.response?.data?.detail || 'خطا در تغییر وضعیت کاربر'
    toast.error(errorMessage)
  }
}

const getRoleText = (role) => {
  const roles = {
    'admin': 'مدیر سیستم',
    'manager': 'مدیر',
    'user': 'کاربر'
  }
  return roles[role] || role
}

const getRoleBadgeClass = (role) => {
  const classes = {
    'admin': 'bg-purple-100 text-purple-800',
    'manager': 'bg-blue-100 text-blue-800',
    'user': 'bg-gray-100 text-gray-800'
  }
  return classes[role] || 'bg-gray-100 text-gray-800'
}

const fetchUsers = async () => {
  loading.value = true
  error.value = ''
  
  try {
    const response = await axios.get('/users')
    users.value = response.data
  } catch (err) {
    error.value = err.response?.data?.detail || 'خطا در بارگذاری کاربران'
    toast.error(error.value)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchUsers()
})
</script>
