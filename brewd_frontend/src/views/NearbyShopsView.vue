<template>
  <div class="min-h-screen bg-mykonos-background p-6">
    <div class="max-w-7xl mx-auto bg-mykonos-background">
      <!-- Header -->
      <div class="mb-8 bg-mykonos-primary border border-mykonos-primary rounded-lg p-6">
        <h1 class="text-3xl font-bold text-mykonos-accent mb-2">Nearby Coffee Shops</h1>
        <p class="text-mykonos-accent">{{ shops.length }} shops found</p>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="flex justify-center items-center py-20">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-mykonos-accent"></div>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="bg-red-100 border border-red-400 rounded-lg p-4 text-red-700">
        {{ error }}
      </div>

      <!-- Grid of Coffee Shops -->
      <div 
        v-else
        class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 max-h-screen overflow-y-auto p-4 bg-mykonos-primary rounded-lg"
      >
        <div
          v-for="shop in shops"
          :key="shop.place_id"
          class="bg-mykonos-surface rounded-lg shadow-md hover:shadow-xl transition-shadow duration-300 overflow-hidden"
        >
          <!-- Shop Info -->
          <div class="p-4 bg-mykonos-surface">
            <div class="flex justify-between items-start mb-2">
              <h3 class="text-lg font-semibold text-mykonos-textPrimary truncate flex-1">
                {{ shop.name }}
              </h3>
              
              <!-- Favorite Button -->
              <button 
                @click="toggleFavorite(shop)"
                :disabled="favoriteLoading[shop.place_id]"
                class="ml-2 text-2xl transition-transform hover:scale-110 disabled:opacity-50"
                :title="isFavorite(shop.place_id) ? 'Remove from favorites' : 'Add to favorites'"
              >
                {{ isFavorite(shop.place_id) ? '❤️' : '🤍' }}
              </button>
            </div>

            <!-- Address -->
            <p class="text-sm text-mykonos-textSecondary mb-2 line-clamp-2">
              {{ shop.address }}
            </p>
          </div>
        </div>
      </div>

      <!-- Empty State -->
      <div v-if="!loading && !error && shops.length === 0" class="text-center py-20">
        <svg class="mx-auto h-12 w-12 text-mykonos-textSecondary mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
        </svg>
        <h3 class="text-lg font-medium text-mykonos-textPrimary mb-2">No coffee shops found</h3>
        <p class="text-sm text-mykonos-textSecondary">Try adjusting your location or search radius.</p>
      </div>
    </div>

    <!-- Rating Modal (appears when adding to favorites) -->
    <div v-if="showRatingModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-mykonos-surface border border-mykonos-primary rounded-lg p-8 max-w-md w-full mx-4">
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
      favoriteShops: [], // List of favorited place_ids
      loading: false,
      error: null,
      favoriteLoading: {}, // Track loading state per shop
      
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
        // Get user's location
        const location = this.userStore.userLocation
        
        if (!location) {
          this.error = 'Location not available. Please enable location access.'
          return
        }

        const response = await axios.get('/api/shops/nearby/', {
          params: {
            lat: location.latitude,
            lng: location.longitude,
            radius: 1500
          }
        })

        this.shops = response.data.results || []
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
        const response = await axios.get('/api/shops/favorites/')
        console.log('Raw favorites response:', response.data)
        
        // Handle paginated response (DRF default)
        let favorites = []
        
        if (response.data.results) {
          // Paginated response
          favorites = response.data.results
          console.log('Paginated response detected')
        } else if (Array.isArray(response.data)) {
          // Direct array response
          favorites = response.data
          console.log('Direct array response detected')
        } else {
          console.error('Unexpected response format:', response.data)
          this.favoriteShops = []
          return
        }
        
        // Extract place_ids
        this.favoriteShops = favorites.map(fav => fav.shop.place_id)
        console.log('User favorite place_ids:', this.favoriteShops)
        
      } catch (error) {
        console.error('Error fetching favorites:', error)
        // Set empty array so the rest of the component works
        this.favoriteShops = []
        
        // Only show toast if it's not a 401 (unauthorized)
        if (error.response?.status !== 401) {
          this.toastStore?.showToast(
            3000,
            'Could not load favorites',
            'bg-mykonos-error text-mykonos-textPrimary'
          )
        }
      }
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
        // This is where FavoriteShopCreateSerializer is used!
        const response = await axios.post('/api/shops/favorites/', {
          shop_place_id: placeId,
          taste_rating: this.ratings.taste_rating || null,
          vibe_rating: this.ratings.vibe_rating || null,
          service_rating: this.ratings.service_rating || null
        })

        console.log('Favorite created:', response.data)

        // Add to local favorites list
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
        // First, find the favorite ID
        const response = await axios.get('/api/shops/favorites/')
        
        // Handle paginated response
        const favorites = response.data.results || response.data
        
        const favorite = favorites.find(
          fav => fav.shop.place_id === shop.place_id
        )

        if (favorite) {
          await axios.delete(`/api/shops/favorites/${favorite.id}/`)

          // Remove from local list
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
    }
  }
}
</script>