import { defineStore } from 'pinia'
import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api'

export const useUserStore = defineStore('user', {
  state: () => ({
    user: null,
    access: null,
    refresh: null,
    isAuthenticated: false,
  }),

  actions: {
    async login(username, password) {
      try {
        const response = await axios.post(`${API_URL}/login/`, {
          username,
          password,
        })

        console.log('Login response:', response.data)

        // JWT tokens from Django's TokenObtainPairView
        this.access = response.data.access
        this.refresh = response.data.refresh
        this.isAuthenticated = true

        // Set axios default header for future requests
        axios.defaults.headers.common['Authorization'] = `Bearer ${this.access}`

        // Fetch user details
        await this.fetchUser()

        return { success: true }
      } catch (error) {
        console.error('Login error:', error.response?.data || error)
        return { 
          success: false, 
          error: error.response?.data?.detail || 'Invalid username or password'
        }
      }
    },

    async fetchUser() {
      try {
        const response = await axios.get(`${API_URL}/auth/user/`)
        this.user = response.data
        console.log('User fetched:', this.user)
      } catch (error) {
        console.error('Fetch user error:', error)
        this.logout()
      }
    },

    logout() {
      this.user = null
      this.access = null
      this.refresh = null
      this.isAuthenticated = false
      delete axios.defaults.headers.common['Authorization']
    },

    initializeAuth() {
      // Set axios header if token exists (on page reload)
      if (this.access) {
        axios.defaults.headers.common['Authorization'] = `Bearer ${this.access}`
        this.fetchUser()
      }
    },
  },

  persist: true, // Persists to localStorage
})