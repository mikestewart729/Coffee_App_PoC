<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <div class="min-h-screen bg-mykonos-background">
    <nav class="py-10 px-8 bg-mykonos-background border-b border-mykonos-primary">
        <div class="max-w-7xl mx-auto">
            <div class="flex items-center justify-between">
              <div class="w-1/4">
                <div class="menu-left">
                    <a href="#" class="text-3xl text-mykonos-textPrimary"><strong>Brew'd</strong></a>
                </div>
              </div>

              <div class="w-2/4">
                <div class="menu-center flex space-x-12 justify-center">
                  <RouterLink to="#">
                      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                          <path stroke-linecap="round" stroke-linejoin="round" d="M2.25 12l8.954-8.955c.44-.439 1.152-.439 1.591 0L21.75 12M4.5 9.75v10.125c0 .621.504 1.125 1.125 1.125H9.75v-4.875c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125V21h4.125c.621 0 1.125-.504 1.125-1.125V9.75M8.25 21h8.25" />
                      </svg>
                  </RouterLink>

                  <RouterLink to="#">
                      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                          <!-- cup body -->
                          <path stroke-linecap="round" stroke-linejoin="round" d="M4 8h12v6a4 4 0 01-4 4H8a4 4 0 01-4-4V8z" />
                          <!-- handle -->
                          <path stroke-linecap="round" stroke-linejoin="round" d="M16 10a4 4 0 014 2v2a4 4 0 01-4 2" />
                          <!-- steam -->
                          <path stroke-linecap="round" stroke-linejoin="round" d="M8 3c0 1.5 1.2 2 1 3.5-.2 1.5-1 2-1 3" />
                          <path stroke-linecap="round" stroke-linejoin="round" d="M12 3c0 1.5 1.2 2 1 3.5-.2 1.5-1 2-1 3" />
                      </svg>
                  </RouterLink>

                  <RouterLink to="#">
                      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                          <path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-5.197-5.197m0 0A7.5 7.5 0 105.196 5.196a7.5 7.5 0 0010.607 10.607z"></path>
                      </svg>                                                         
                  </RouterLink>
                </div>
              </div>

              <div class="w-1/4 flex justify-end">
                <div class="menu-right">
                      <a href="#" class="mr-4 py-4 px-6 bg-mykonos-secondary text-mykonos-accent text-xl rounded-lg">Log in</a>
                      <RouterLink to="/signup" class="py-4 px-6 bg-mykonos-primary text-mykonos-accent text-xl rounded-lg">Sign up</RouterLink>
                </div>
              </div>
            </div>
        </div>
    </nav>

    <main class="px-8 py-6 bg-mykonos-background">
        <RouterView />
    </main>
  </div>
</template>
