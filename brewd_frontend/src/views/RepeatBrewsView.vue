<template>
  <div class="min-h-screen bg-mykonos-background p-6">
    <div class="max-w-7xl mx-auto bg-mykonos-background">
      <!-- Header with filters -->
      <div class="mb-8 bg-mykonos-surface border border-mykonos-primary rounded-lg p-6">
        <h1 class="text-3xl font-bold text-mykonos-textPrimary mb-4">Your Repeat Brews</h1>
        <p class="text-mykonos-textSecondary mb-6">5 favorite coffee shops saved</p>
        
        <!-- Filter/Sort Controls -->
        <div class="flex flex-wrap gap-4">
          <div class="flex items-center gap-2">
            <label class="text-sm text-mykonos-textSecondary">Sort by:</label>
            <select class="bg-mykonos-background border border-mykonos-primary rounded-lg px-4 py-2 text-mykonos-textPrimary">
              <option>Recent</option>
              <option>☕ Taste</option>
              <option>🎵 Vibe</option>
              <option>🤝 Service</option>
              <option>Overall Rating</option>
            </select>
          </div>
          
          <div class="flex items-center gap-2">
            <label class="text-sm text-mykonos-textSecondary">Filter:</label>
            <button class="bg-mykonos-secondary text-mykonos-accent px-4 py-2 rounded-lg text-sm">
              All Shops
            </button>
            <button class="bg-mykonos-background border border-mykonos-primary text-mykonos-textSecondary px-4 py-2 rounded-lg text-sm hover:bg-mykonos-surface">
              Top Rated
            </button>
          </div>
        </div>
      </div>

      <!-- Grid of Saved Coffee Shops -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 max-h-screen overflow-y-auto p-2 pb-6 bg-mykonos-primary rounded-lg">
        
        <!-- Shop Card 1 -->
        <div class="bg-mykonos-surface rounded-lg shadow-md hover:shadow-xl transition-shadow duration-300 overflow-hidden cursor-pointer">
          <div class="p-4">
            <!-- Header with name and favorite icon -->
            <div class="flex justify-between items-start mb-3">
              <h3 class="text-lg font-semibold text-mykonos-textPrimary truncate flex-1">
                Blue Bottle Coffee
              </h3>
              <button class="text-mykonos-accent ml-2">
                ❤️
              </button>
            </div>
            
            <!-- Address -->
            <p class="text-sm text-mykonos-textSecondary mb-4 line-clamp-2">
              123 Artisan Ave, Brooklyn, NY
            </p>

            <!-- Category Ratings -->
            <div class="space-y-2 mb-4">
              <!-- Taste -->
              <div class="flex items-center justify-between">
                <span class="text-sm text-mykonos-textSecondary">☕ Taste</span>
                <div class="flex items-center gap-1">
                  <span class="text-mykonos-accent">★★★★★</span>
                  <span class="text-xs text-mykonos-textSecondary ml-1">5.0</span>
                </div>
              </div>
              
              <!-- Vibe -->
              <div class="flex items-center justify-between">
                <span class="text-sm text-mykonos-textSecondary">🎵 Vibe</span>
                <div class="flex items-center gap-1">
                  <span class="text-mykonos-accent">★★★★☆</span>
                  <span class="text-xs text-mykonos-textSecondary ml-1">4.0</span>
                </div>
              </div>
              
              <!-- Service -->
              <div class="flex items-center justify-between">
                <span class="text-sm text-mykonos-textSecondary">🤝 Service</span>
                <div class="flex items-center gap-1">
                  <span class="text-mykonos-accent">★★★★★</span>
                  <span class="text-xs text-mykonos-textSecondary ml-1">5.0</span>
                </div>
              </div>
            </div>

            <!-- Overall Rating Bar -->
            <div class="pt-3 border-t border-mykonos-primary">
              <div class="flex items-center justify-between">
                <span class="text-sm font-medium text-mykonos-textPrimary">Overall</span>
                <span class="text-lg font-bold text-mykonos-accent">4.7</span>
              </div>
            </div>

            <!-- Last Visited -->
            <p class="text-xs text-mykonos-textSecondary mt-2">
              Last visited: 2 days ago
            </p>
          </div>
        </div>

        <!-- Shop Card 2 -->
        <div class="bg-mykonos-surface rounded-lg shadow-md hover:shadow-xl transition-shadow duration-300 overflow-hidden cursor-pointer">
          <div class="p-4">
            <div class="flex justify-between items-start mb-3">
              <h3 class="text-lg font-semibold text-mykonos-textPrimary truncate flex-1">
                Stumptown Coffee
              </h3>
              <button class="text-mykonos-accent ml-2">
                ❤️
              </button>
            </div>
            
            <p class="text-sm text-mykonos-textSecondary mb-4 line-clamp-2">
              456 Roaster Road, Manhattan, NY
            </p>

            <div class="space-y-2 mb-4">
              <div class="flex items-center justify-between">
                <span class="text-sm text-mykonos-textSecondary">☕ Taste</span>
                <div class="flex items-center gap-1">
                  <span class="text-mykonos-accent">★★★★☆</span>
                  <span class="text-xs text-mykonos-textSecondary ml-1">4.5</span>
                </div>
              </div>
              
              <div class="flex items-center justify-between">
                <span class="text-sm text-mykonos-textSecondary">🎵 Vibe</span>
                <div class="flex items-center gap-1">
                  <span class="text-mykonos-accent">★★★★★</span>
                  <span class="text-xs text-mykonos-textSecondary ml-1">5.0</span>
                </div>
              </div>
              
              <div class="flex items-center justify-between">
                <span class="text-sm text-mykonos-textSecondary">🤝 Service</span>
                <div class="flex items-center gap-1">
                  <span class="text-mykonos-accent">★★★★☆</span>
                  <span class="text-xs text-mykonos-textSecondary ml-1">4.0</span>
                </div>
              </div>
            </div>

            <div class="pt-3 border-t border-mykonos-primary">
              <div class="flex items-center justify-between">
                <span class="text-sm font-medium text-mykonos-textPrimary">Overall</span>
                <span class="text-lg font-bold text-mykonos-accent">4.5</span>
              </div>
            </div>

            <p class="text-xs text-mykonos-textSecondary mt-2">
              Last visited: 1 week ago
            </p>
          </div>
        </div>

        <!-- Shop Card 3 -->
        <div class="bg-mykonos-surface rounded-lg shadow-md hover:shadow-xl transition-shadow duration-300 overflow-hidden cursor-pointer">
          <div class="p-4">
            <div class="flex justify-between items-start mb-3">
              <h3 class="text-lg font-semibold text-mykonos-textPrimary truncate flex-1">
                Intelligentsia Coffee
              </h3>
              <button class="text-mykonos-accent ml-2">
                ❤️
              </button>
            </div>
            
            <p class="text-sm text-mykonos-textSecondary mb-4 line-clamp-2">
              789 Bean Boulevard, Queens, NY
            </p>

            <div class="space-y-2 mb-4">
              <div class="flex items-center justify-between">
                <span class="text-sm text-mykonos-textSecondary">☕ Taste</span>
                <div class="flex items-center gap-1">
                  <span class="text-mykonos-accent">★★★★★</span>
                  <span class="text-xs text-mykonos-textSecondary ml-1">5.0</span>
                </div>
              </div>
              
              <div class="flex items-center justify-between">
                <span class="text-sm text-mykonos-textSecondary">🎵 Vibe</span>
                <div class="flex items-center gap-1">
                  <span class="text-mykonos-accent">★★★☆☆</span>
                  <span class="text-xs text-mykonos-textSecondary ml-1">3.0</span>
                </div>
              </div>
              
              <div class="flex items-center justify-between">
                <span class="text-sm text-mykonos-textSecondary">🤝 Service</span>
                <div class="flex items-center gap-1">
                  <span class="text-mykonos-accent">★★★★☆</span>
                  <span class="text-xs text-mykonos-textSecondary ml-1">4.0</span>
                </div>
              </div>
            </div>

            <div class="pt-3 border-t border-mykonos-primary">
              <div class="flex items-center justify-between">
                <span class="text-sm font-medium text-mykonos-textPrimary">Overall</span>
                <span class="text-lg font-bold text-mykonos-accent">4.0</span>
              </div>
            </div>

            <p class="text-xs text-mykonos-textSecondary mt-2">
              Last visited: 3 weeks ago
            </p>
          </div>
        </div>

        <!-- Shop Card 4 -->
        <div class="bg-mykonos-surface rounded-lg shadow-md hover:shadow-xl transition-shadow duration-300 overflow-hidden cursor-pointer">
          <div class="p-4">
            <div class="flex justify-between items-start mb-3">
              <h3 class="text-lg font-semibold text-mykonos-textPrimary truncate flex-1">
                La Colombe Coffee
              </h3>
              <button class="text-mykonos-accent ml-2">
                ❤️
              </button>
            </div>
            
            <p class="text-sm text-mykonos-textSecondary mb-4 line-clamp-2">
              321 Espresso Street, Brooklyn, NY
            </p>

            <div class="space-y-2 mb-4">
              <div class="flex items-center justify-between">
                <span class="text-sm text-mykonos-textSecondary">☕ Taste</span>
                <div class="flex items-center gap-1">
                  <span class="text-mykonos-accent">★★★★☆</span>
                  <span class="text-xs text-mykonos-textSecondary ml-1">4.0</span>
                </div>
              </div>
              
              <div class="flex items-center justify-between">
                <span class="text-sm text-mykonos-textSecondary">🎵 Vibe</span>
                <div class="flex items-center gap-1">
                  <span class="text-mykonos-accent">★★★★★</span>
                  <span class="text-xs text-mykonos-textSecondary ml-1">5.0</span>
                </div>
              </div>
              
              <div class="flex items-center justify-between">
                <span class="text-sm text-mykonos-textSecondary">🤝 Service</span>
                <div class="flex items-center gap-1">
                  <span class="text-mykonos-accent">★★★★☆</span>
                  <span class="text-xs text-mykonos-textSecondary ml-1">4.5</span>
                </div>
              </div>
            </div>

            <div class="pt-3 border-t border-mykonos-primary">
              <div class="flex items-center justify-between">
                <span class="text-sm font-medium text-mykonos-textPrimary">Overall</span>
                <span class="text-lg font-bold text-mykonos-accent">4.5</span>
              </div>
            </div>

            <p class="text-xs text-mykonos-textSecondary mt-2">
              Last visited: 5 days ago
            </p>
          </div>
        </div>

        <!-- Shop Card 5 -->
        <div class="bg-mykonos-surface rounded-lg shadow-md hover:shadow-xl transition-shadow duration-300 overflow-hidden cursor-pointer">
          <div class="p-4">
            <div class="flex justify-between items-start mb-3">
              <h3 class="text-lg font-semibold text-mykonos-textPrimary truncate flex-1">
                Gregorys Coffee
              </h3>
              <button class="text-mykonos-accent ml-2">
                ❤️
              </button>
            </div>
            
            <p class="text-sm text-mykonos-textSecondary mb-4 line-clamp-2">
              555 Latte Lane, Manhattan, NY
            </p>

            <div class="space-y-2 mb-4">
              <div class="flex items-center justify-between">
                <span class="text-sm text-mykonos-textSecondary">☕ Taste</span>
                <div class="flex items-center gap-1">
                  <span class="text-mykonos-accent">★★★★☆</span>
                  <span class="text-xs text-mykonos-textSecondary ml-1">4.0</span>
                </div>
              </div>
              
              <div class="flex items-center justify-between">
                <span class="text-sm text-mykonos-textSecondary">🎵 Vibe</span>
                <div class="flex items-center gap-1">
                  <span class="text-mykonos-accent">★★★☆☆</span>
                  <span class="text-xs text-mykonos-textSecondary ml-1">3.5</span>
                </div>
              </div>
              
              <div class="flex items-center justify-between">
                <span class="text-sm text-mykonos-textSecondary">🤝 Service</span>
                <div class="flex items-center gap-1">
                  <span class="text-mykonos-accent">★★★★★</span>
                  <span class="text-xs text-mykonos-textSecondary ml-1">5.0</span>
                </div>
              </div>
            </div>

            <div class="pt-3 border-t border-mykonos-primary">
              <div class="flex items-center justify-between">
                <span class="text-sm font-medium text-mykonos-textPrimary">Overall</span>
                <span class="text-lg font-bold text-mykonos-accent">4.2</span>
              </div>
            </div>

            <p class="text-xs text-mykonos-textSecondary mt-2">
              Last visited: 1 month ago
            </p>
          </div>
        </div>

      </div>

      <!-- Empty State (hidden when shops exist) -->
      <!-- <div class="text-center py-20 bg-mykonos-surface border border-mykonos-primary rounded-lg">
        <svg class="mx-auto h-12 w-12 text-mykonos-textSecondary mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"/>
        </svg>
        <h3 class="text-lg font-medium text-mykonos-textPrimary mb-2">No saved coffee shops yet</h3>
        <p class="text-sm text-mykonos-textSecondary">Start exploring and save your favorite spots!</p>
      </div> -->
    </div>
  </div>
</template>

<script>
export default {
  name: 'RepeatBrewsView',
  data() {
    return {
      // Will eventually hold saved shops data
      savedShops: []
    }
  }
}
</script>