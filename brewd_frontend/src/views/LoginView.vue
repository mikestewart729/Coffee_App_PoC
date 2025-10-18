<template>
    <div class="max-w-7xl mx-auto grid grid-cols-2 gap-4 bg-mykonos-background">
        <div class="main-left">
            <div class="p-12 bg-mykonos-surface border border-mykonos-primary rounded-lg">
                <h1 class="mb-6 text-2xl text-mykonos-textPrimary">Sign up</h1>

                <p class="mb-6 text-mykonos-textSecondary">
                    Are you a <i class="text-mykonos-accent">pretentious coffee drinker</i>? You've come to the right place! Brew'd is your home for 
                    finding your next coffee obsession and tracking your café journey. Create an account to get started.
                </p>

                <p class="font-bold text-mykonos-textPrimary">
                    Don't have an account yet? <RouterLink :to="{name: 'signup'}" class="text-mykonos-accent underline">Click here</RouterLink>
                    to create one!
                </p>
            </div>
        </div>

        <div class="main-right">
            <div class="p-12 bg-mykonos-surface border border-mykonos-primary rounded-lg">
                <form class="space-y-6" @submit.prevent="submitForm">
                    <div>
                        <label class="text-mykonos-textPrimary">Username</label><br/>
                        <input type="username" v-model="form.username" placeholder="Your username" class="w-full mt-2 py-4 px-6 border border-mykonos-secondary rounded-lg text-mykonos-textSecondary"/>
                    </div>

                    <div>
                        <label class="text-mykonos-textPrimary">Password</label><br/>
                        <input type="password" v-model="form.password" placeholder="Your password" class="w-full mt-2 py-4 px-6 border border-mykonos-secondary rounded-lg text-mykonos-textSecondary"/>
                    </div>

                    <template v-if="this.errors.length > 0">
                        <div class="bg-mykonos-error text-mykonos-textPrimary rounded-lg p-6">
                            <p v-for="error in errors" v-bind:key="error">{{ error }}</p>
                        </div>
                    </template>

                    <div>
                        <button 
                            type="submit"
                            :disabled="isLoading"
                            class="py-4 px-6 bg-mykonos-secondary text-mykonos-accent rounded-lg"
                        >
                            {{ isLoading ? 'Logging in...' : 'Log in' }}
                        </button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios'
import { useUserStore } from '@/stores/user'
import { useToastStore } from '@/stores/toast'

export default {
    setup() {
        const userStore = useUserStore()
        const toastStore = useToastStore()

        return {
            userStore,
            toastStore,
        }
    },

    data() {
        return {
            form: {
                email: '',
                password: '',
            },
            errors: [],
            isLoading: false,
        }
    },

    methods: {
        async submitForm() {
            this.errors = []

            if (this.form.username === '') {
                this.errors.push('Your username is missing')
            }

            if (this.form.password === '') {
                this.errors.push('The password is missing')
            }

            if (this.errors.length > 0) {
                return this.errors
            }

            try {
                const response = await this.userStore.login(
                    this.form.username,
                    this.form.password
                )

                if (response.success) {
                    this.toastStore.showToast(
                        3000,
                        `Welcome back, ${this.userStore.user?.username || 'user'}!`,
                        'bg-mykonos-primary text-mykonos-accent'
                    )

                    // Clear form
                    this.form.username = ''
                    this.form.password = ''

                    // Redirect to home page
                    console.log('Redirecting to home...')
                    await this.$router.push('/')
                } else {
                    this.errors.push(result.error || 'Invalid username or password')
                    this.toastStore.showToast(
                        5000,
                        result.error || 'Invalid username or password',
                        'bg-mykonos-error text-mykonos-textPrimary'
                    )
                }
            } catch (error) {
                console.error('Login error:', error)
                this.errors.push('An unexpected error occurred. Please try again.')
                this.toastStore.showToast(
                    5000,
                    'Login failed. Please try again.',
                    'bg-mykonos-error text-mykonos-textPrimary'
                )
            } finally {
                this.isLoading = false
            }
        }
    }
}
</script>
