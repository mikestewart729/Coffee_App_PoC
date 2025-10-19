import { defineStore } from 'pinia'
import axios from 'axios'
import { getCurrentPosition } from '@/utils/geolocation'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api'

export const useUserStore = defineStore('user', {
  state: () => ({
    user: null,
    access: null,
    refresh: null,
    isAuthenticated: false,
    userLocation: null,
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

        // Get the geolocation using new util function
        await this.updateUserLocation()

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

    async updateUserLocation() {
        try {
            console.log('Getting user location...')
            const position = await getCurrentPosition()

            this.userLocation = {
                latitude: position.latitude,
                longitude: position.longitude,
            }

            console.log('User location obtained:', this.userLocation)

            // Send location to baackend
            await this.saveUserLocationToBackend(position.latitude, position.longitude)

            return { success: true, location: this.userLocation }
        } catch (error) {
            console.error('Location error:', error.message)
            // Don't fail login if location fails
            return { success: false, error: error.message }
        }
    },

    async saveUserLocationToBackend(latitude, longitude) {
        try {
            // PATCH the user's location latitude and longitude
            const response = await axios.patch(`${API_URL}/user/update_location/`, {
                location_lat: latitude,
                location_lng: longitude,
            })

            // Update local user object
            if (this.user) {
                this.user.location_lat = response.data.location_lat
                this.user.location_lng = response.data.location_lng
            }

            console.log('User location saved in backend:', response.data)
        } catch (error) {
            console.error('Error saving location to backend:', error)
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

        // Update location on initialization if user is already authenticated
        this.updateUserLocation()
      }
    },
  },

  persist: true, // Persists to localStorage
})