<template>
  <div class="min-h-screen bg-mykonos-background p-6">
    <div class="max-w-7xl mx-auto bg-mykonos-background">
      <!-- Header -->
      <div class="mb-8 bg-mykonos-primary border border-mykonos-primary rounded-lg p-6">
        <h1 class="text-3xl font-bold text-mykonos-accent mb-2">Nearby Coffee Shops</h1>
        <p class="text-mykonos-accent">10 shops found</p>
      </div>

      <div 
        class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 max-h-screen overflow-y-auto p-4 bg-mykonos-primary rounded-lg"
      >
        <div
          class="bg-mykonos-surface rounded-lg shadow-md hover:shadow-xl transition-shadow duration-300 overflow-hidden cursor-pointer"
        >
          <!-- Shop Info -->
          <div class="p-4 bg-mykonos-surface">
            <h3 class="text-lg font-semibold text-mykonos-textPrimary mb-2 truncate">
              Test Café
            </h3>
            
            <!-- Rating -->
            <div class="flex items-center mb-2">
                <div class="flex text-myonoks-textSecondary">
                    <span class="text-mykonos-accent">
                        ★★★★☆
                    </span>
                </div>
            </div>

            <!-- Address -->
            <p class="text-sm text-mykonos-textSecondary mb-2 line-clamp-2">
                123 Coffee St, Caffeine City, NY
            </p>
          </div>
        </div>

        <div
          class="bg-mykonos-surface rounded-lg shadow-md hover:shadow-xl transition-shadow duration-300 overflow-hidden cursor-pointer"
        >
          <!-- Shop Info -->
          <div class="p-4 bg-mykonos-surface">
            <h3 class="text-lg font-semibold text-mykonos-textPrimary mb-2 truncate">
              Test Café 2
            </h3>
            
            <!-- Rating -->
            <div class="flex items-center mb-2">
                <div class="flex text-myonoks-textSecondary">
                    <span class="text-mykonos-accent">
                        ★☆☆☆☆
                    </span>
                </div>
            </div>

            <!-- Address -->
            <p class="text-sm text-mykonos-textSecondary mb-2 line-clamp-2">
                125 Coffee St, Caffeine City, NY
            </p>
          </div>
        </div>

        <div
          class="bg-mykonos-surface rounded-lg shadow-md hover:shadow-xl transition-shadow duration-300 overflow-hidden cursor-pointer"
        >
          <!-- Shop Info -->
          <div class="p-4 bg-mykonos-surface">
            <h3 class="text-lg font-semibold text-mykonos-textPrimary mb-2 truncate">
              Yet Another Café
            </h3>
            
            <!-- Rating -->
            <div class="flex items-center mb-2">
                <div class="flex text-myonoks-textSecondary">
                    <span class="text-mykonos-accent">
                        ★★★★☆
                    </span>
                </div>
            </div>

            <!-- Address -->
            <p class="text-sm text-mykonos-textSecondary mb-2 line-clamp-2">
                123 Bean Way, Caffeine City, NY
            </p>
          </div>
        </div>

        <div
          class="bg-mykonos-surface rounded-lg shadow-md hover:shadow-xl transition-shadow duration-300 overflow-hidden cursor-pointer"
        >
          <!-- Shop Info -->
          <div class="p-4 bg-mykonos-surface">
            <h3 class="text-lg font-semibold text-mykonos-textPrimary mb-2 truncate">
              Beans and Beans on Beans
            </h3>
            
            <!-- Rating -->
            <div class="flex items-center mb-2">
                <div class="flex text-myonoks-textSecondary">
                    <span class="text-mykonos-accent">
                        ★★★★★
                    </span>
                </div>
            </div>

            <!-- Address -->
            <p class="text-sm text-mykonos-textSecondary mb-2 line-clamp-2">
                444 Roastery Place, Caffeine City, NY
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
    name: 'NearbyShopsView'
}
</script>