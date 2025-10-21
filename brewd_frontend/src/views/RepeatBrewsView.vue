<template>
  <div class="min-h-screen bg-mykonos-background p-6">
    <div class="max-w-7xl mx-auto bg-mykonos-background">
      
      <div v-if="loading" class="text-center py-20">
        <!-- Loading State -->
        <svg class="animate-spin h-8 w-8 text-mykonos-accent mx-auto" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
        <p class="text-mykonos-textSecondary mt-3">Loading your favorite brews...</p>
      </div>

      <div v-else-if="error" class="text-center py-20 bg-mykonos-surface border border-mykonos-error rounded-lg">
        <!-- Error State -->
        <h3 class="text-lg font-medium text-mykonos-textPrimary mb-2">Error Loading Favorites</h3>
        <p class="text-sm text-mykonos-textSecondary">{{ error }}</p>
        <button @click="fetchSavedShops" class="mt-4 bg-mykonos-primary text-mykonos-accent px-4 py-2 rounded-lg text-sm hover:bg-mykonos-secondary transition duration-150">
          Try Again
        </button>
      </div>
      
      <!-- Main Content -->
      <div v-else>
        <!-- Header with filters -->
        <div class="mb-8 bg-mykonos-surface border border-mykonos-primary rounded-lg p-6">
          <h1 class="text-3xl font-bold text-mykonos-textPrimary mb-4">Your Repeat Brews</h1>
          <p class="text-mykonos-textSecondary mb-6">{{ savedShops.length }} favorite coffee shops saved</p>
          
          <!-- Filter/Sort Controls -->
          <div class="flex flex-wrap gap-4 items-center">
            
            <!-- Sort By -->
            <div class="flex items-center gap-2">
              <label for="sort-select" class="text-sm text-mykonos-textSecondary">Sort by:</label>
              <select 
                id="sort-select"
                v-model="sortBy"
                class="bg-mykonos-background border border-mykonos-primary rounded-lg px-4 py-2 text-mykonos-textPrimary focus:ring-mykonos-accent focus:border-mykonos-accent">
                <option value="recent">Recent</option>
                <option value="taste">☕ Taste</option>
                <option value="vibe">🎵 Vibe</option>
                <option value="service">🤝 Service</option>
                <option value="overall">Overall Rating</option>
              </select>
            </div>
            
            <!-- Filter -->
            <div class="flex items-center gap-2">
              <label class="text-sm text-mykonos-textSecondary">Filter:</label>
              <button 
                @click="filterBy = 'all'" 
                :class="{'bg-mykonos-secondary border-mykonos-secondary': filterBy === 'all', 'bg-mykonos-background border-mykonos-primary text-mykonos-textSecondary hover:bg-mykonos-surface': filterBy !== 'all'}"
                class="text-mykonos-accent border px-4 py-2 rounded-lg text-sm transition duration-150">
                All Shops
              </button>
              <button 
                @click="filterBy = 'top_rated'" 
                :class="{'bg-mykonos-secondary border-mykonos-secondary': filterBy === 'top_rated', 'bg-mykonos-background border-mykonos-primary text-mykonos-textSecondary hover:bg-mykonos-surface': filterBy !== 'top_rated'}"
                class="text-mykonos-accent border px-4 py-2 rounded-lg text-sm transition duration-150">
                Top Rated (4.0+)
              </button>
            </div>
          </div>
        </div>

        <!-- Grid of Saved Coffee Shops -->
        <div v-if="sortedAndFilteredShops.length > 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 max-h-[80vh] overflow-y-auto p-2 pb-6 bg-mykonos-primary rounded-lg">
          
          <!-- Shop Card (Dynamically Rendered) -->
          <div v-for="favorite in sortedAndFilteredShops" :key="favorite.id" 
               class="bg-mykonos-surface rounded-lg shadow-md hover:shadow-xl transition-shadow duration-300 overflow-hidden cursor-pointer">
            <div class="p-4">
              <!-- Header with name and favorite icon -->
              <div class="flex justify-between items-start mb-3">
                <h3 class="text-lg font-semibold text-mykonos-textPrimary truncate flex-1" :title="favorite.shop.name">
                  {{ favorite.shop.name }}
                </h3>
                <!-- Button to remove the favorite shop -->
                <button 
                  @click.stop="removeFavorite(favorite.id)" 
                  class="text-mykonos-accent ml-2 hover:opacity-80 transition duration-150"
                  title="Remove from favorites">
                  ❤️
                </button>
              </div>
              
              <!-- Address -->
              <p class="text-sm text-mykonos-textSecondary mb-4 line-clamp-2">
                {{ favorite.shop.formatted_address || 'Address not available' }}
              </p>

              <!-- Category Ratings -->
              <div class="space-y-2 mb-4">
                <!-- Taste -->
                <div class="flex items-center justify-between">
                  <span class="text-sm text-mykonos-textSecondary">☕ Taste</span>
                  <div class="flex items-center gap-1">
                    <span class="text-mykonos-accent">{{ renderStarRating(favorite.taste_rating) }}</span>
                    <span class="text-xs text-mykonos-textSecondary ml-1">{{ favorite.taste_rating.toFixed(1) }}</span>
                  </div>
                </div>
                
                <!-- Vibe -->
                <div class="flex items-center justify-between">
                  <span class="text-sm text-mykonos-textSecondary">🎵 Vibe</span>
                  <div class="flex items-center gap-1">
                    <span class="text-mykonos-accent">{{ renderStarRating(favorite.vibe_rating) }}</span>
                    <span class="text-xs text-mykonos-textSecondary ml-1">{{ favorite.vibe_rating.toFixed(1) }}</span>
                  </div>
                </div>
                
                <!-- Service -->
                <div class="flex items-center justify-between">
                  <span class="text-sm text-mykonos-textSecondary">🤝 Service</span>
                  <div class="flex items-center gap-1">
                    <span class="text-mykonos-accent">{{ renderStarRating(favorite.service_rating) }}</span>
                    <span class="text-xs text-mykonos-textSecondary ml-1">{{ favorite.service_rating.toFixed(1) }}</span>
                  </div>
                </div>
              </div>

              <!-- Overall Rating Bar -->
              <div class="pt-3 border-t border-mykonos-primary">
                <div class="flex items-center justify-between">
                  <span class="text-sm font-medium text-mykonos-textPrimary">Overall</span>
                  <span class="text-lg font-bold text-mykonos-accent">{{ favorite.overall_rating.toFixed(1) }}</span>
                </div>
              </div>

              <!-- Saved Date -->
              <p class="text-xs text-mykonos-textSecondary mt-2">
                Saved on: {{ formatDate(favorite.created_at) }}
              </p>
            </div>
          </div>
        </div>

        <!-- Empty State (when shops exist but don't match filter) -->
        <div v-else-if="savedShops.length > 0" class="text-center py-20 bg-mykonos-surface border border-mykonos-primary rounded-lg">
          <h3 class="text-lg font-medium text-mykonos-textPrimary mb-2">No shops match the current filter.</h3>
          <p class="text-sm text-mykonos-textSecondary">Try selecting "All Shops" to see your full list.</p>
        </div>

        <!-- Truly Empty State (no shops saved) -->
        <div v-else class="text-center py-20 bg-mykonos-surface border border-mykonos-primary rounded-lg">
          <svg class="mx-auto h-12 w-12 text-mykonos-textSecondary mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"/>
          </svg>
          <h3 class="text-lg font-medium text-mykonos-textPrimary mb-2">No saved coffee shops yet</h3>
          <p class="text-sm text-mykonos-textSecondary">Start exploring and save your favorite spots!</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'
import { useUserStore } from '@/stores/user' 
import { useToastStore } from '@/stores/toast'

export default {
  name: 'RepeatBrewsView',
  
  setup() {
    const savedShops = ref([])
    const loading = ref(false)
    const error = ref(null)
    const sortBy = ref('recent') // 'recent', 'taste', 'vibe', 'service', 'overall'
    const filterBy = ref('all') // 'all', 'top_rated'
    
    // Assumed store setup
    const userStore = useUserStore()
    const toastStore = useToastStore()
    
    // --- Methods ---

    /**
     * Helper to convert a float rating (e.g., 4.7) into a 5-star string.
     * @param {number} rating - The rating value (0.0 to 5.0).
     */
    const renderStarRating = (rating) => {
      // Ensure rating is a number and clamp it between 0 and 5
      const rate = Math.max(0, Math.min(5, Number(rating) || 0));

      const fullStars = Math.floor(rate)
      // Check if the fractional part is 0.5 or greater for a half star
      const hasHalfStar = rate - fullStars >= 0.5
      
      let stars = '★'.repeat(fullStars)
      if (hasHalfStar) {
        stars += '½'
      }
      stars += '☆'.repeat(5 - fullStars - (hasHalfStar ? 1 : 0))
      return stars
    }

    /**
     * Helper to format the creation date.
     */
    const formatDate = (dateString) => {
        if (!dateString) return 'N/A'
        try {
            // Options for a shorter, cleaner date format
            return new Date(dateString).toLocaleDateString('en-US', {
              year: 'numeric',
              month: 'short',
              day: 'numeric'
            })
        } catch (e) {
            return dateString
        }
    }

    /**
     * Removes a shop from the user's favorites list.
     * @param {number} favoriteId - The ID of the favorite record to delete.
     */
    const removeFavorite = async (favoriteId) => {
      try {
        // Send DELETE request to the API. 
        // We use the favoriteId (the ID of the saved record) here, not the shop's place_id.
        await axios.delete(`/shops/favorites/${favoriteId}/`)
        
        // Optimistically update the UI: filter the deleted item out of the array
        savedShops.value = savedShops.value.filter(fav => fav.id !== favoriteId)
        
        // Show success toast
        toastStore.showToast(3000, 'Shop removed from Repeat Brews!', 'bg-mykonos-primary text-mykonos-accent')

      } catch (err) {
        console.error('Error removing favorite:', err)
        // Show error toast
        toastStore.showToast(5000, 'Failed to remove favorite. Please try again.', 'bg-mykonos-error text-mykonos-textPrimary')
      }
    }

    /**
     * Fetches the user's favorite shops from the backend API.
     */
    const fetchSavedShops = async () => {
      loading.value = true
      error.value = null
      savedShops.value = []

      try {
        const response = await axios.get('/shops/favorites/')
        
        // Handle paginated or direct array response
        const favorites = response.data.results || response.data || []
        
        // Enhance the data with calculated overall rating before storing
        savedShops.value = favorites.map(fav => {
          // Calculate overall rating, treating null/undefined as 0 for calculation purposes 
          // (though the DB should ensure they are 0-5)
          const taste = fav.taste_rating || 0
          const vibe = fav.vibe_rating || 0
          const service = fav.service_rating || 0
          
          const ratings = [taste, vibe, service].filter(r => r > 0);
          
          // Calculate overall rating only using provided ratings
          const overall_rating = ratings.length > 0 ? ratings.reduce((a, b) => a + b, 0) / ratings.length : 0;
          
          return {
            ...fav,
            // Ensure fields are numeric for display functions like .toFixed(1)
            taste_rating: taste,
            vibe_rating: vibe,
            service_rating: service,
            overall_rating: overall_rating
          }
        })
        
        console.log('Fetched and processed favorites:', savedShops.value)

      } catch (err) {
        console.error('Error fetching favorites:', err)
        error.value = err.response?.data?.detail || 'Failed to load favorite shops.'
        
        if (err.response?.status === 401) {
            toastStore?.showToast(5000, 'Please log in to view your favorites.', 'bg-mykonos-error text-mykonos-textPrimary')
        }

      } finally {
        loading.value = false
      }
    }

    // --- Computed Properties for Display Logic ---

    /**
     * Applies filtering logic to the list of shops.
     */
    const filteredShops = computed(() => {
      if (filterBy.value === 'all') {
        return savedShops.value
      }
      
      if (filterBy.value === 'top_rated') {
        // Filter for shops with an overall rating of 4.5 or higher
        return savedShops.value.filter(shop => shop.overall_rating >= 4.0)
      }
      
      return savedShops.value
    })

    /**
     * Applies sorting logic to the filtered list.
     */
    const sortedAndFilteredShops = computed(() => {
      // Use slice() to create a shallow copy for sorting without mutating the original array
      const shops = filteredShops.value.slice() 

      if (sortBy.value === 'recent') {
        // Sort by creation date (most recently saved, descending)
        return shops.sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
      }

      // Sorting by rating fields
      const sortKey = sortBy.value + '_rating' // e.g., 'taste_rating'
      if (['taste_rating', 'vibe_rating', 'service_rating', 'overall_rating'].includes(sortKey)) {
        // Sort descending (highest rating first)
        return shops.sort((a, b) => b[sortKey] - a[sortKey])
      }
      
      return shops
    })

    // --- Lifecycle Hook ---
    onMounted(() => {
      fetchSavedShops()
    })

    // --- Return reactive variables and methods for the template ---
    return {
      savedShops,
      sortedAndFilteredShops,
      loading,
      error,
      sortBy,
      filterBy,
      fetchSavedShops,
      removeFavorite,
      renderStarRating,
      formatDate
    }
  }
}
</script>
