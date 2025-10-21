<template>
  <div class="min-h-screen bg-mykonos-background p-6">
    <div class="max-w-7xl mx-auto bg-mykonos-background">
      <!-- Header with Controls -->
      <div class="mb-8 bg-mykonos-primary border border-mykonos-primary rounded-lg p-6">
        <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
          <div>
            <h1 class="text-3xl font-bold text-mykonos-accent mb-2">Nearby Coffee Shops</h1>
            <p class="text-mykonos-accent">
              {{ shops.length }} shops found within {{ (searchRadius / 1609.34).toFixed(1) }}mi
            </p>
          </div>
          
          <!-- Controls -->
          <div class="flex flex-wrap gap-3">
            <!-- Radius Selector -->
            <div class="flex items-center gap-2">
              <label class="text-mykonos-accent text-sm">Radius:</label>
              <select 
                v-model="searchRadius" 
                @change="onRadiusChange"
                class="bg-mykonos-surface border border-mykonos-accent text-mykonos-textPrimary rounded-lg px-3 py-2"
              >
                <option :value="402">0.25 mi</option>
                <option :value="805">0.5 mi</option>
                <option :value="1609">1 mi</option>
                <option :value="2414">1.5 mi</option>
                <option :value="3219">2 mi</option>
                <option :value="4828">3 mi</option>
                <option :value="8047">5 mi</option>
              </select>
            </div>
            
            <!-- Sort Selector -->
            <div class="flex items-center gap-2">
              <label class="text-mykonos-accent text-sm">Sort:</label>
              <select 
                v-model="sortBy" 
                @change="sortShops"
                class="bg-mykonos-surface border border-mykonos-accent text-mykonos-textPrimary rounded-lg px-3 py-2"
              >
                <option value="distance">Distance</option>
                <option value="name">Name</option>
              </select>
            </div>
            
            <!-- Refresh Button -->
            <button 
              @click="refreshShops"
              :disabled="loading"
              class="bg-mykonos-secondary text-mykonos-accent px-4 py-2 rounded-lg hover:opacity-80 disabled:opacity-50 flex items-center gap-2"
            >
              <svg class="w-5 h-5" :class="{ 'animate-spin': loading }" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
              </svg>
              <span class="hidden md:inline">Refresh</span>
            </button>
            
            <!-- Filter Toggle -->
            <button 
              @click="showFavoritesOnly = !showFavoritesOnly"
              class="px-4 py-2 rounded-lg flex items-center gap-2"
              :class="showFavoritesOnly ? 'bg-mykonos-accent text-mykonos-surface' : 'bg-mykonos-surface text-mykonos-textPrimary border border-mykonos-accent'"
            >
              <span>{{ showFavoritesOnly ? '❤️' : '🤍' }}</span>
              <span class="hidden md:inline">{{ showFavoritesOnly ? 'All' : 'Favorites' }}</span>
            </button>
          </div>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="flex justify-center items-center py-20">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-mykonos-accent"></div>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="bg-red-100 border border-red-400 rounded-lg p-4 text-red-700">
        <p class="font-semibold mb-2">{{ error }}</p>
        <button 
          @click="fetchNearbyShops"
          class="mt-2 bg-red-600 text-white px-4 py-2 rounded-lg hover:bg-red-700"
        >
          Try Again
        </button>
      </div>

      <!-- Grid of Coffee Shops -->
      <div 
        v-else
        class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 max-h-screen overflow-y-auto p-4 bg-mykonos-primary rounded-lg"
      >
        <div
          v-for="shop in filteredShops"
          :key="shop.place_id"
          class="bg-mykonos-surface rounded-lg shadow-md hover:shadow-xl transition-all duration-300 overflow-hidden transform hover:-translate-y-1"
        >
          <!-- Shop Info -->
          <div class="p-4 bg-mykonos-surface">
            <div class="flex justify-between items-start mb-2">
              <div class="flex-1">
                <h3 class="text-lg font-semibold text-mykonos-textPrimary truncate">
                  {{ shop.name }}
                </h3>
                <!-- Distance Badge -->
                <span 
                  v-if="shop.distance_formatted"
                  class="inline-block mt-1 text-xs bg-mykonos-accent text-mykonos-surface px-2 py-1 rounded-full font-medium"
                >
                  📍 {{ shop.distance_formatted }}
                </span>
              </div>
              
              <!-- Favorite Button -->
              <button 
                @click="toggleFavorite(shop)"
                :disabled="favoriteLoading[shop.place_id]"
                class="ml-2 text-2xl transition-transform hover:scale-110 disabled:opacity-50 flex-shrink-0"
                :title="isFavorite(shop.place_id) ? 'Remove from favorites' : 'Add to favorites'"
              >
                {{ isFavorite(shop.place_id) ? '❤️' : '🤍' }}
              </button>
            </div>

            <!-- Address -->
            <p class="text-sm text-mykonos-textSecondary mb-2 line-clamp-2">
              {{ shop.address }}
            </p>

            <!-- Action Buttons -->
            <div class="flex gap-2 mt-3">
              <button 
                @click="openInMaps(shop)"
                class="flex-1 text-xs bg-mykonos-primary text-mykonos-accent px-3 py-2 rounded-lg hover:opacity-80"
              >
                🗺️ Directions
              </button>
              <button 
                v-if="isFavorite(shop.place_id)"
                @click="viewFavoriteDetails(shop)"
                class="flex-1 text-xs bg-mykonos-secondary text-mykonos-accent px-3 py-2 rounded-lg hover:opacity-80"
              >
                ⭐ View Ratings
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Empty State -->
      <div v-if="!loading && !error && filteredShops.length === 0" class="text-center py-20">
        <svg class="mx-auto h-12 w-12 text-mykonos-textSecondary mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
        </svg>
        <h3 class="text-lg font-medium text-mykonos-textPrimary mb-2">
          {{ showFavoritesOnly ? 'No favorited shops nearby' : 'No coffee shops found' }}
        </h3>
        <p class="text-sm text-mykonos-textSecondary">
          {{ showFavoritesOnly ? 'Try showing all shops or expanding your search radius.' : 'Try expanding your search radius.' }}
        </p>
      </div>
    </div>

    <!-- Rating Modal -->
    <div v-if="showRatingModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-mykonos-surface border border-mykonos-primary rounded-lg p-8 max-w-md w-full mx-4 max-h-screen overflow-y-auto">
        <h2 class="text-2xl font-bold text-mykonos-textPrimary mb-4">
          Rate {{ selectedShop?.name }}
        </h2>
        
        <div class="space-y-4">
          <!-- Taste Rating -->
          <div>
            <label class="text-mykonos-textPrimary mb-2 block">☕ Taste</label>
            <div class="flex gap-2">
              <button 
                v-for="rating in 5" 
                :key="'taste-' + rating"
                @click="ratings.taste_rating = rating"
                class="text-3xl transition-transform hover:scale-110"
              >
                {{ rating <= ratings.taste_rating ? '★' : '☆' }}
              </button>
            </div>
          </div>

          <!-- Vibe Rating -->
          <div>
            <label class="text-mykonos-textPrimary mb-2 block">🎵 Vibe</label>
            <div class="flex gap-2">
              <button 
                v-for="rating in 5" 
                :key="'vibe-' + rating"
                @click="ratings.vibe_rating = rating"
                class="text-3xl transition-transform hover:scale-110"
              >
                {{ rating <= ratings.vibe_rating ? '★' : '☆' }}
              </button>
            </div>
          </div>

          <!-- Service Rating -->
          <div>
            <label class="text-mykonos-textPrimary mb-2 block">🤝 Service</label>
            <div class="flex gap-2">
              <button 
                v-for="rating in 5" 
                :key="'service-' + rating"
                @click="ratings.service_rating = rating"
                class="text-3xl transition-transform hover:scale-110"
              >
                {{ rating <= ratings.service_rating ? '★' : '☆' }}
              </button>
            </div>
          </div>
        </div>

        <!-- Modal Actions -->
        <div class="flex gap-4 mt-6">
          <button 
            @click="submitFavorite"
            :disabled="!hasAnyRating"
            class="flex-1 py-3 px-6 bg-mykonos-primary text-mykonos-accent rounded-lg hover:opacity-80 disabled:opacity-50"
          >
            Save to Favorites
          </button>
          <button 
            @click="closeRatingModal"
            class="flex-1 py-3 px-6 bg-mykonos-secondary text-mykonos-textSecondary rounded-lg hover:opacity-80"
          >
            Cancel
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import { useUserStore } from '@/stores/user'
import { useToastStore } from '@/stores/toast'

export default {
  name: 'NearbyShopsView',
  
  setup() {
    const userStore = useUserStore()
    const toastStore = useToastStore()
    return { userStore, toastStore }
  },

  data() {
    return {
      shops: [],
      favoriteShops: [],
      loading: false,
      error: null,
      favoriteLoading: {},
      
      // Search controls
      searchRadius: 402,
      sortBy: 'distance',
      showFavoritesOnly: false,
      
      // Rating modal
      showRatingModal: false,
      selectedShop: null,
      ratings: {
        taste_rating: 0,
        vibe_rating: 0,
        service_rating: 0
      }
    }
  },

  computed: {
    hasAnyRating() {
      return this.ratings.taste_rating > 0 || 
             this.ratings.vibe_rating > 0 || 
             this.ratings.service_rating > 0
    },
    
    filteredShops() {
      let filtered = [...this.shops]
      
      // Filter by favorites
      if (this.showFavoritesOnly) {
        filtered = filtered.filter(shop => this.isFavorite(shop.place_id))
      }
      
      return filtered
    }
  },

  mounted() {
    this.fetchNearbyShops()
    this.fetchUserFavorites()
  },

  methods: {
    async fetchNearbyShops() {
      this.loading = true
      this.error = null

      try {
        const location = this.userStore.userLocation
        
        if (!location) {
          this.error = 'Location not available. Please enable location access.'
          return
        }

        const response = await axios.get('/api/shops/nearby/', {
          params: {
            lat: location.latitude,
            lng: location.longitude,
            radius: this.searchRadius
          }
        })

        this.shops = response.data.results || []
        this.sortShops()
        console.log('Fetched shops:', this.shops)
      } catch (error) {
        console.error('Error fetching shops:', error)
        this.error = error.response?.data?.message || 'Failed to fetch nearby shops'
      } finally {
        this.loading = false
      }
    },

    async fetchUserFavorites() {
      try {
        const response = await axios.get('/shops/favorites/')
        
        let favorites = []
        if (response.data.results) {
          favorites = response.data.results
        } else if (Array.isArray(response.data)) {
          favorites = response.data
        } else {
          this.favoriteShops = []
          return
        }
        
        this.favoriteShops = favorites.map(fav => fav.shop.place_id)
        console.log('User favorite place_ids:', this.favoriteShops)
        
      } catch (error) {
        console.error('Error fetching favorites:', error)
        this.favoriteShops = []
      }
    },

    sortShops() {
      if (this.sortBy === 'distance') {
        this.shops.sort((a, b) => (a.distance_meters || 0) - (b.distance_meters || 0))
      } else if (this.sortBy === 'name') {
        this.shops.sort((a, b) => a.name.localeCompare(b.name))
      }
    },

    onRadiusChange() {
      this.fetchNearbyShops()
    },

    refreshShops() {
      this.fetchNearbyShops()
      this.fetchUserFavorites()
    },

    isFavorite(placeId) {
      return this.favoriteShops.includes(placeId)
    },

    toggleFavorite(shop) {
      if (this.isFavorite(shop.place_id)) {
        this.removeFavorite(shop)
      } else {
        this.openRatingModal(shop)
      }
    },

    openRatingModal(shop) {
      this.selectedShop = shop
      this.ratings = {
        taste_rating: 0,
        vibe_rating: 0,
        service_rating: 0
      }
      this.showRatingModal = true
    },

    closeRatingModal() {
      this.showRatingModal = false
      this.selectedShop = null
    },

    async submitFavorite() {
      if (!this.selectedShop) return

      const placeId = this.selectedShop.place_id
      this.favoriteLoading[placeId] = true

      try {
        const response = await axios.post('/shops/favorites/', {
          shop_place_id: placeId,
          taste_rating: this.ratings.taste_rating || null,
          vibe_rating: this.ratings.vibe_rating || null,
          service_rating: this.ratings.service_rating || null
        })

        this.favoriteShops.push(placeId)

        this.toastStore.showToast(
          3000,
          `Added ${this.selectedShop.name} to favorites!`,
          'bg-mykonos-primary text-mykonos-accent'
        )

        this.closeRatingModal()
      } catch (error) {
        console.error('Error adding favorite:', error)
        
        const errorMsg = error.response?.data?.shop_place_id?.[0] || 
                        error.response?.data?.message ||
                        'Failed to add to favorites'
        
        this.toastStore.showToast(
          5000,
          errorMsg,
          'bg-mykonos-error text-mykonos-textPrimary'
        )
      } finally {
        this.favoriteLoading[placeId] = false
      }
    },

    async removeFavorite(shop) {
      this.favoriteLoading[shop.place_id] = true

      try {
        const response = await axios.get('/shops/favorites/')
        const favorites = response.data.results || response.data
        
        const favorite = favorites.find(
          fav => fav.shop.place_id === shop.place_id
        )

        if (favorite) {
          await axios.delete(`/shops/favorites/${favorite.id}/`)

          this.favoriteShops = this.favoriteShops.filter(
            id => id !== shop.place_id
          )

          this.toastStore.showToast(
            3000,
            `Removed ${shop.name} from favorites`,
            'bg-mykonos-secondary text-mykonos-accent'
          )
        }
      } catch (error) {
        console.error('Error removing favorite:', error)
        this.toastStore.showToast(
          5000,
          'Failed to remove from favorites',
          'bg-mykonos-error text-mykonos-textPrimary'
        )
      } finally {
        this.favoriteLoading[shop.place_id] = false
      }
    },

    openInMaps(shop) {
      // Open in Google Maps
      const url = `https://www.google.com/maps/search/?api=1&query=${shop.latitude},${shop.longitude}&query_place_id=${shop.place_id}`
      window.open(url, '_blank')
    },

    viewFavoriteDetails(shop) {
      // Navigate to RepeatBrewsView or show a detail modal
      this.$router.push('/repeatbrews')
    }
  }
}
</script>
