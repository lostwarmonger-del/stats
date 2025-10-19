import { defineStore } from 'pinia'
import axios from 'axios'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    token: localStorage.getItem('token'),
    isAuthenticated: !!localStorage.getItem('token')
  }),

  getters: {
    userName: (state) => state.user?.name || 'کاربر',
    userRole: (state) => state.user?.role || 'user',
    hasAnyRole: (state) => (roles) => {
      if (!state.user) return false
      return roles.includes(state.user.role)
    }
  },

  actions: {
    async login(credentials) {
      try {
        const response = await axios.post('/auth/login', credentials)
        const { access_token, user } = response.data
        
        this.token = access_token
        this.user = user
        this.isAuthenticated = true
        
        localStorage.setItem('token', access_token)
        axios.defaults.headers.common['Authorization'] = `Bearer ${access_token}`
        
        return { success: true }
      } catch (error) {
        console.error('Login error:', error)
        return { 
          success: false, 
          error: error.response?.data?.detail || 'خطا در ورود به سیستم' 
        }
      }
    },

    async checkAuth() {
      if (!this.token) {
        this.isAuthenticated = false
        return false
      }
      
      try {
        axios.defaults.headers.common['Authorization'] = `Bearer ${this.token}`
        const response = await axios.get('/auth/me')
        this.user = response.data
        this.isAuthenticated = true
        return true
      } catch (error) {
        console.error('Auth check error:', error)
        this.logout()
        return false
      }
    },

    logout() {
      this.user = null
      this.token = null
      this.isAuthenticated = false
      localStorage.removeItem('token')
      delete axios.defaults.headers.common['Authorization']
    }
  }
})





