<template>
  <div class="min-h-screen bg-mykonos-background">
    <nav class="py-10 px-8 bg-mykonos-background border-b border-mykonos-primary">
        <div class="max-w-7xl mx-auto">
            <div class="flex items-center justify-between">
              <div class="w-1/4">
                <div class="menu-left">
                    <RouterLink to="/" class="text-2xl md:text-3xl text-mykonos-textPrimary"><strong>Brew'd</strong></RouterLink>
                </div>
              </div>

              <div class="w-2/4">
                <div v-if="userStore.user.isAuthenticated" class="menu-center flex space-x-6 md:space-x-12 justify-center">
                  <!-- Home/NearbyShopsView -->
                  <RouterLink to="/">
                      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5 md:w-6 md:h-6">
                          <path stroke-linecap="round" stroke-linejoin="round" d="M2.25 12l8.954-8.955c.44-.439 1.152-.439 1.591 0L21.75 12M4.5 9.75v10.125c0 .621.504 1.125 1.125 1.125H9.75v-4.875c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125V21h4.125c.621 0 1.125-.504 1.125-1.125V9.75M8.25 21h8.25" />
                      </svg>
                  </RouterLink>

                  <!-- Repeat Brews / Favorites View-->
                  <RouterLink to="/repeatbrews">
                      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5 md:w-6 md:h-6">
                          <!-- cup body -->
                          <path stroke-linecap="round" stroke-linejoin="round" d="M4 8h12v6a4 4 0 01-4 4H8a4 4 0 01-4-4V8z" />
                          <!-- handle -->
                          <path stroke-linecap="round" stroke-linejoin="round" d="M16 10a4 4 0 014 2v2a4 4 0 01-4 2" />
                          <!-- steam -->
                          <path stroke-linecap="round" stroke-linejoin="round" d="M8 3c0 1.5 1.2 2 1 3.5-.2 1.5-1 2-1 3" />
                          <path stroke-linecap="round" stroke-linejoin="round" d="M12 3c0 1.5 1.2 2 1 3.5-.2 1.5-1 2-1 3" />
                      </svg>
                  </RouterLink>

                  <!-- Search View -->
                  <RouterLink to="/search">
                      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5 md:w-6 md:h-6">
                          <path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-5.197-5.197m0 0A7.5 7.5 0 105.196 5.196a7.5 7.5 0 0010.607 10.607z"></path>
                      </svg>                                                         
                  </RouterLink>
                </div>
              </div>

              <div class="w-1/4 flex justify-end">
                <template  v-if="userStore.user.isAuthenticated">
                  <div class="menu-right flex flex-wrap gap-2 md:gap-0 justify-end">
                      <button @click="logout" class="md:mr-4 py-2 px-3 md:py-4 md:px-6 bg-mykonos-secondary text-mykonos-accent text-sm md:text-xl rounded-lg whitespace-nowrap">Log out</button>
                  </div>
                </template>

                <template v-else>
                  <div class="menu-right flex flex-wrap gap-2 md:gap-0 justify-end">
                    <RouterLink to="/login" class="md:mr-4 py-2 px-3 md:py-4 md:px-6 bg-mykonos-secondary text-mykonos-accent text-sm md:text-xl rounded-lg whitespace-nowrap">Log in</RouterLink>
                    <RouterLink to="/signup" class="py-2 px-3 md:py-4 md:px-6 bg-mykonos-primary text-mykonos-accent text-sm md:text-xl rounded-lg whitespace-nowrap">Sign up</RouterLink>
                  </div>
                </template>
              </div>
            </div>
        </div>
    </nav>

    <main class="px-8 py-6 bg-mykonos-background">
        <RouterView />
    </main>

    <Toast />
  </div>
</template>

<script>
    import axios from 'axios'
    import Toast from '@/components/Toast.vue'
    import { useUserStore } from '@/stores/user'

    export default {
        setup() {
            const userStore = useUserStore()

            return {
                userStore
            }
        },

        components: {
            Toast
        },

        beforeCreate() {
            this.userStore.initStore()

            const token = this.userStore.user.access

            if (token) {
                axios.defaults.headers.common["Authorization"] = "Bearer " + token;
            } else {
                axios.defaults.headers.common["Authorization"] = "";
            }
        },

        methods: {
          logout() {
            console.log('logout')

            this.userStore.removeToken()

            this.$router.push('/login')
          }
        },
    }
</script>
