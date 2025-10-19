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
              <h1 class="text-3xl font-bold mb-2">برنامه 404640758</h1>
              <p class="text-blue-100 text-lg">فرم ثبت اطلاعات برنامه 404640758</p>
            </div>
            <div class="w-20 h-20 bg-white/20 rounded-full flex items-center justify-center">
              <font-awesome-icon icon="fas fa-user" class="text-4xl text-yellow-400" />
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
            <!-- Personal Information Section -->
            <div class="bg-white rounded-xl p-6 border border-gray-200 shadow-sm">
              <h3 class="text-lg font-semibold text-gray-900 mb-4 flex items-center">
                <font-awesome-icon icon="fas fa-user" class="text-blue-600 ml-2" />
                اطلاعات شخصی
              </h3>
              
              <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">نام <span class="text-red-500">*</span></label>
                  <input 
                    v-model="formData.first_name" 
                    type="text" 
                    :class="['w-full px-4 py-3 border rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all', errors.first_name ? 'border-red-500' : 'border-gray-300']"
                    placeholder="نام را وارد کنید"
                  />
                  <p v-if="errors.first_name" class="text-red-500 text-sm mt-1">{{ errors.first_name }}</p>
                </div>
                
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">نام خانوادگی <span class="text-red-500">*</span></label>
                  <input 
                    v-model="formData.last_name" 
                    type="text" 
                    :class="['w-full px-4 py-3 border rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all', errors.last_name ? 'border-red-500' : 'border-gray-300']"
                    placeholder="نام خانوادگی را وارد کنید"
                  />
                  <p v-if="errors.last_name" class="text-red-500 text-sm mt-1">{{ errors.last_name }}</p>
                </div>
                
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">نام پدر <span class="text-red-500">*</span></label>
                  <input 
                    v-model="formData.father_name" 
                    type="text" 
                    :class="['w-full px-4 py-3 border rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all', errors.father_name ? 'border-red-500' : 'border-gray-300']"
                    placeholder="نام پدر را وارد کنید"
                  />
                  <p v-if="errors.father_name" class="text-red-500 text-sm mt-1">{{ errors.father_name }}</p>
                </div>
                
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">شماره شناسنامه <span class="text-red-500">*</span></label>
                  <input 
                    v-model="formData.id_number" 
                    type="number" 
                    :class="['w-full px-4 py-3 border rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all', errors.id_number ? 'border-red-500' : 'border-gray-300']"
                    placeholder="شماره شناسنامه را وارد کنید"
                  />
                  <p v-if="errors.id_number" class="text-red-500 text-sm mt-1">{{ errors.id_number }}</p>
                </div>
                
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">تاریخ تولد <span class="text-red-500">*</span></label>
                  <ShamsiDatePicker 
                    v-model="formData.birth_date"
                    placeholder="تاریخ شمسی (مثال: 1403/01/15)"
                    :class="errors.birth_date ? 'border-red-500' : ''"
                  />
                  <p v-if="errors.birth_date" class="text-red-500 text-sm mt-1">{{ errors.birth_date }}</p>
                </div>
                
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">کد ملی <span class="text-red-500">*</span></label>
                  <input 
                    v-model="formData.national_id" 
                    type="number" 
                    :class="['w-full px-4 py-3 border rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all', errors.national_id ? 'border-red-500' : 'border-gray-300']"
                    placeholder="کد ملی را وارد کنید"
                  />
                  <p v-if="errors.national_id" class="text-red-500 text-sm mt-1">{{ errors.national_id }}</p>
                </div>
              </div>
            </div>

            <!-- ID Card Information Section -->
            <div class="bg-white rounded-xl p-6 border border-gray-200 shadow-sm">
              <h3 class="text-lg font-semibold text-gray-900 mb-4 flex items-center">
                <font-awesome-icon icon="fas fa-id-card" class="text-green-600 ml-2" />
                اطلاعات شناسنامه
              </h3>
              
              <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">تاریخ صدور شناسنامه <span class="text-red-500">*</span></label>
                  <ShamsiDatePicker 
                    v-model="formData.id_issue_date"
                    placeholder="تاریخ شمسی (مثال: 1403/01/15)"
                    :class="errors.id_issue_date ? 'border-red-500' : ''"
                  />
                  <p v-if="errors.id_issue_date" class="text-red-500 text-sm mt-1">{{ errors.id_issue_date }}</p>
                </div>
                
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">محل صدور شناسنامه <span class="text-red-500">*</span></label>
                  <input 
                    v-model="formData.id_issue_place" 
                    type="text" 
                    :class="['w-full px-4 py-3 border rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all', errors.id_issue_place ? 'border-red-500' : 'border-gray-300']"
                    placeholder="محل صدور شناسنامه را وارد کنید"
                  />
                  <p v-if="errors.id_issue_place" class="text-red-500 text-sm mt-1">{{ errors.id_issue_place }}</p>
                </div>
                
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">دین (مذهب) <span class="text-red-500">*</span></label>
                  <select 
                    v-model="formData.religion" 
                    :class="['w-full px-4 py-3 border rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all', errors.religion ? 'border-red-500' : 'border-gray-300']"
                  >
                    <option value="">انتخاب کنید</option>
                    <option value="اسلام">اسلام</option>
                    <option value="مسیحیت">مسیحیت</option>
                    <option value="یهودیت">یهودیت</option>
                    <option value="زرتشتی">زرتشتی</option>
                    <option value="سایر">سایر</option>
                  </select>
                  <p v-if="errors.religion" class="text-red-500 text-sm mt-1">{{ errors.religion }}</p>
                </div>
              </div>
            </div>

            <!-- Location Information Section -->
            <div class="bg-white rounded-xl p-6 border border-gray-200 shadow-sm">
              <h3 class="text-lg font-semibold text-gray-900 mb-4 flex items-center">
                <font-awesome-icon icon="fas fa-map-marker-alt" class="text-purple-600 ml-2" />
                اطلاعات مکانی
              </h3>
              
              <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">استان <span class="text-red-500">*</span></label>
                  <input 
                    v-model="formData.province" 
                    type="text" 
                    :class="['w-full px-4 py-3 border rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all', errors.province ? 'border-red-500' : 'border-gray-300']"
                    placeholder="استان را وارد کنید"
                  />
                  <p v-if="errors.province" class="text-red-500 text-sm mt-1">{{ errors.province }}</p>
                </div>
                
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">شهر <span class="text-red-500">*</span></label>
                  <input 
                    v-model="formData.city" 
                    type="text" 
                    :class="['w-full px-4 py-3 border rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all', errors.city ? 'border-red-500' : 'border-gray-300']"
                    placeholder="شهر را وارد کنید"
                  />
                  <p v-if="errors.city" class="text-red-500 text-sm mt-1">{{ errors.city }}</p>
                </div>
                
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">آدرس محل سکونت <span class="text-red-500">*</span></label>
                  <textarea 
                    v-model="formData.address" 
                    rows="3"
                    :class="['w-full px-4 py-3 border rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all', errors.address ? 'border-red-500' : 'border-gray-300']"
                    placeholder="آدرس کامل محل سکونت را وارد کنید"
                  ></textarea>
                  <p v-if="errors.address" class="text-red-500 text-sm mt-1">{{ errors.address }}</p>
                </div>
                
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">شماره تماس <span class="text-red-500">*</span></label>
                  <input 
                    v-model="formData.phone_number" 
                    type="tel" 
                    :class="['w-full px-4 py-3 border rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all', errors.phone_number ? 'border-red-500' : 'border-gray-300']"
                    placeholder="شماره تماس را وارد کنید"
                  />
                  <p v-if="errors.phone_number" class="text-red-500 text-sm mt-1">{{ errors.phone_number }}</p>
                </div>
              </div>
            </div>

            <!-- Personal Status Section -->
            <div class="bg-white rounded-xl p-6 border border-gray-200 shadow-sm">
              <h3 class="text-lg font-semibold text-gray-900 mb-4 flex items-center">
                <font-awesome-icon icon="fas fa-user-check" class="text-orange-600 ml-2" />
                وضعیت شخصی
              </h3>
              
              <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">وضعیت تأهل <span class="text-red-500">*</span></label>
                  <select 
                    v-model="formData.marital_status" 
                    :class="['w-full px-4 py-3 border rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all', errors.marital_status ? 'border-red-500' : 'border-gray-300']"
                  >
                    <option value="">انتخاب کنید</option>
                    <option value="مجرد">مجرد</option>
                    <option value="متأهل">متأهل</option>
                    <option value="مطلقه">مطلقه</option>
                    <option value="بیوه">بیوه</option>
                  </select>
                  <p v-if="errors.marital_status" class="text-red-500 text-sm mt-1">{{ errors.marital_status }}</p>
                </div>
                
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">وضعیت خدمت وظیفه <span class="text-red-500">*</span></label>
                  <select 
                    v-model="formData.military_service_status" 
                    :class="['w-full px-4 py-3 border rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all', errors.military_service_status ? 'border-red-500' : 'border-gray-300']"
                  >
                    <option value="">انتخاب کنید</option>
                    <option value="انجام داده">انجام داده</option>
                    <option value="معاف">معاف</option>
                    <option value="در حال انجام">در حال انجام</option>
                    <option value="مشمول نشده">مشمول نشده</option>
                  </select>
                  <p v-if="errors.military_service_status" class="text-red-500 text-sm mt-1">{{ errors.military_service_status }}</p>
                </div>
                
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">وضعیت جسمانی <span class="text-red-500">*</span></label>
                  <select 
                    v-model="formData.physical_status" 
                    :class="['w-full px-4 py-3 border rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all', errors.physical_status ? 'border-red-500' : 'border-gray-300']"
                  >
                    <option value="">انتخاب کنید</option>
                    <option value="سالم">سالم</option>
                    <option value="نابینا">نابینا</option>
                    <option value="ناشنوا">ناشنوا</option>
                    <option value="معلول جسمی">معلول جسمی</option>
                    <option value="سایر">سایر</option>
                  </select>
                  <p v-if="errors.physical_status" class="text-red-500 text-sm mt-1">{{ errors.physical_status }}</p>
                </div>
                
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">توضیح سطح سلامت <span class="text-red-500">*</span></label>
                  <textarea 
                    v-model="formData.health_description" 
                    rows="3"
                    :class="['w-full px-4 py-3 border rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all', errors.health_description ? 'border-red-500' : 'border-gray-300']"
                    placeholder="توضیح سطح سلامت را وارد کنید"
                  ></textarea>
                  <p v-if="errors.health_description" class="text-red-500 text-sm mt-1">{{ errors.health_description }}</p>
                </div>
                
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">ملیت <span class="text-red-500">*</span></label>
                  <input 
                    v-model="formData.nationality" 
                    type="text" 
                    :class="['w-full px-4 py-3 border rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all', errors.nationality ? 'border-red-500' : 'border-gray-300']"
                    placeholder="ملیت را وارد کنید"
                  />
                  <p v-if="errors.nationality" class="text-red-500 text-sm mt-1">{{ errors.nationality }}</p>
                </div>
              </div>
            </div>

            <!-- Professional Information Section -->
            <div class="bg-white rounded-xl p-6 border border-gray-200 shadow-sm">
              <h3 class="text-lg font-semibold text-gray-900 mb-4 flex items-center">
                <font-awesome-icon icon="fas fa-briefcase" class="text-indigo-600 ml-2" />
                اطلاعات حرفه‌ای
              </h3>
              
              <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">حوزه فعالیت <span class="text-red-500">*</span></label>
                  <select 
                    v-model="formData.activity_field" 
                    :class="['w-full px-4 py-3 border rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all', errors.activity_field ? 'border-red-500' : 'border-gray-300']"
                  >
                    <option value="">انتخاب کنید</option>
                    <option value="برنامه نویسی وب">برنامه نویسی وب</option>
                    <option value="تست و نفوذ وب">تست و نفوذ وب</option>
                    <option value="برنامه نویسی موبایل">برنامه نویسی موبایل</option>
                    <option value="هک و نفوذ شبکه های اجتماعی">هک و نفوذ شبکه های اجتماعی</option>
                    <option value="برنامه نویسی ویندوز">برنامه نویسی ویندوز</option>
                    <option value="تست و نفوذ موبایل">تست و نفوذ موبایل</option>
                    <option value="داده کاوی">داده کاوی</option>
                    <option value="متن کاوی">متن کاوی</option>
                    <option value="پردازش تصویر">پردازش تصویر</option>
                    <option value="پردازش صوت">پردازش صوت</option>
                    <option value="سایر">سایر</option>
                  </select>
                  <p v-if="errors.activity_field" class="text-red-500 text-sm mt-1">{{ errors.activity_field }}</p>
                </div>
                
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">سوابق تحصیلی <span class="text-red-500">*</span></label>
                  <textarea 
                    v-model="formData.educational_background" 
                    rows="3"
                    :class="['w-full px-4 py-3 border rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all', errors.educational_background ? 'border-red-500' : 'border-gray-300']"
                    placeholder="سوابق تحصیلی را وارد کنید"
                  ></textarea>
                  <p v-if="errors.educational_background" class="text-red-500 text-sm mt-1">{{ errors.educational_background }}</p>
                </div>
                
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">تجربیات شغلی <span class="text-red-500">*</span></label>
                  <textarea 
                    v-model="formData.work_experience" 
                    rows="3"
                    :class="['w-full px-4 py-3 border rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all', errors.work_experience ? 'border-red-500' : 'border-gray-300']"
                    placeholder="تجربیات شغلی را وارد کنید"
                  ></textarea>
                  <p v-if="errors.work_experience" class="text-red-500 text-sm mt-1">{{ errors.work_experience }}</p>
                </div>
                
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">زبان های خارجی <span class="text-red-500">*</span></label>
                  <textarea 
                    v-model="formData.foreign_languages" 
                    rows="3"
                    :class="['w-full px-4 py-3 border rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all', errors.foreign_languages ? 'border-red-500' : 'border-gray-300']"
                    placeholder="زبان های خارجی را وارد کنید"
                  ></textarea>
                  <p v-if="errors.foreign_languages" class="text-red-500 text-sm mt-1">{{ errors.foreign_languages }}</p>
                </div>
                
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">گواهینامه دوره های گذرانده شده <span class="text-red-500">*</span></label>
                  <textarea 
                    v-model="formData.certificates" 
                    rows="3"
                    :class="['w-full px-4 py-3 border rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all', errors.certificates ? 'border-red-500' : 'border-gray-300']"
                    placeholder="گواهینامه دوره های گذرانده شده را وارد کنید"
                  ></textarea>
                  <p v-if="errors.certificates" class="text-red-500 text-sm mt-1">{{ errors.certificates }}</p>
                </div>
                
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">همکاری پیشنهادی مورد درخواست <span class="text-red-500">*</span></label>
                  <textarea 
                    v-model="formData.requested_cooperation" 
                    rows="3"
                    :class="['w-full px-4 py-3 border rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all', errors.requested_cooperation ? 'border-red-500' : 'border-gray-300']"
                    placeholder="همکاری پیشنهادی مورد درخواست را وارد کنید"
                  ></textarea>
                  <p v-if="errors.requested_cooperation" class="text-red-500 text-sm mt-1">{{ errors.requested_cooperation }}</p>
                </div>
                
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">حقوق پیشنهادی <span class="text-red-500">*</span></label>
                  <input 
                    v-model="formData.proposed_salary" 
                    type="number" 
                    :class="['w-full px-4 py-3 border rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all', errors.proposed_salary ? 'border-red-500' : 'border-gray-300']"
                    placeholder="حقوق پیشنهادی را وارد کنید"
                  />
                  <p v-if="errors.proposed_salary" class="text-red-500 text-sm mt-1">{{ errors.proposed_salary }}</p>
                </div>
                
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">فعالیت های علمی <span class="text-red-500">*</span></label>
                  <textarea 
                    v-model="formData.scientific_activities" 
                    rows="3"
                    :class="['w-full px-4 py-3 border rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all', errors.scientific_activities ? 'border-red-500' : 'border-gray-300']"
                    placeholder="فعالیت های علمی (ارائه سمینار، تدوین کتاب یا مقاله علمی، سایر فعالیت های علمی) را وارد کنید"
                  ></textarea>
                  <p v-if="errors.scientific_activities" class="text-red-500 text-sm mt-1">{{ errors.scientific_activities }}</p>
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
  <ProgramDataModal404640758 
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
import ProgramDataModal404640758 from './ProgramDataModal404640758.vue'
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
  first_name: '',
  last_name: '',
  father_name: '',
  id_number: '',
  birth_date: '',
  national_id: '',
  id_issue_date: '',
  id_issue_place: '',
  religion: '',
  province: '',
  city: '',
  marital_status: '',
  military_service_status: '',
  physical_status: '',
  health_description: '',
  nationality: '',
  activity_field: '',
  educational_background: '',
  work_experience: '',
  foreign_languages: '',
  certificates: '',
  requested_cooperation: '',
  proposed_salary: '',
  scientific_activities: '',
  address: '',
  phone_number: ''
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
    'first_name',
    'last_name',
    'father_name',
    'id_number',
    'birth_date',
    'national_id',
    'id_issue_date',
    'id_issue_place',
    'religion',
    'province',
    'city',
    'marital_status',
    'military_service_status',
    'physical_status',
    'health_description',
    'nationality',
    'activity_field',
    'educational_background',
    'work_experience',
    'foreign_languages',
    'certificates',
    'requested_cooperation',
    'proposed_salary',
    'scientific_activities',
    'address',
    'phone_number'
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

const saveData = async () => {
  // Validate form
  if (!validateForm()) {
    toast.error('لطفاً تمام فیلدهای الزامی را پر کنید')
    return
  }

  saving.value = true
  try {
    // Prepare form data and ensure all fields are strings
    const dataToSend = {}
    Object.keys(formData.value).forEach(key => {
      const value = formData.value[key]
      // Convert null/undefined to empty string
      dataToSend[key] = value === null || value === undefined ? '' : String(value)
    })
    
    await axios.post('/programs/404640758', dataToSend)
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
    first_name: '',
    last_name: '',
    father_name: '',
    id_number: '',
    birth_date: '',
    national_id: '',
    id_issue_date: '',
    id_issue_place: '',
    religion: '',
    province: '',
    city: '',
    marital_status: '',
    military_service_status: '',
    physical_status: '',
    health_description: '',
    nationality: '',
    activity_field: '',
    educational_background: '',
    work_experience: '',
    foreign_languages: '',
    certificates: '',
    requested_cooperation: '',
    proposed_salary: '',
    scientific_activities: '',
    address: '',
    phone_number: ''
  }
  errors.value = {}
  hasExistingData.value = false
}

const loadData = async () => {
  loading.value = true
  try {
    // Get the latest saved data to show in "Last Updated"
    const response = await axios.get('/programs/404640758/all')
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