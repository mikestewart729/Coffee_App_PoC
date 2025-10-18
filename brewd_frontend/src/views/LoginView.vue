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
                <form class="space-y-6">
                    <div>
                        <label class="text-mykonos-textPrimary">Username</label><br/>
                        <input type="username" v-model="form.username" placeholder="Your username" class="w-full mt-2 py-4 px-6 border border-mykonos-secondary rounded-lg text-mykonos-textSecondary"/>
                    </div>

                    <div>
                        <label class="text-mykonos-textPrimary">Password</label><br/>
                        <input type="password" v-model="form.password" placeholder="Your password" class="w-full mt-2 py-4 px-6 border border-mykonos-secondary rounded-lg text-mykonos-textSecondary"/>
                    </div>

                    <template v-if="errors.length > 0">
                        <div class="bg-mykonos-error text-mykonos-textPrimary rounded-lg p-6">
                            <p v-for="error in errors" v-bind:key="error">{{ error }}</p>
                        </div>
                    </template>

                    <div>
                        <button class="py-4 px-6 bg-mykonos-secondary text-mykonos-accent rounded-lg">Log in</button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios'
import { useUserStore } from '@/stores/user'

export default {
    setup() {
        const userStore = useUserStore()

        return {
            userStore
        }
    },

    data() {
        return {
            form: {
                email: '',
                password: '',
            },
            errors: []
        }
    },

    methods: {
        async submitForm() {
            this.errors = []

            if (this.form.email === '') {
                this.errors.push('Your e-mail is missing')
            }

            if (this.form.password === '') {
                this.errors.push('The password is missing')
            }

            if (this.errors.length > 0) {
                return this.errors
            }

            console.log('Submitting form', this.form)

            try {
                const response = await axios.post('/api/signup/', {
                    username: this.form.username,
                    password: this.form.password
                })

                console.log('Response:', response.data)

                this.form.username = ''
                this.form.password = ''
            } catch (error) {
                const errorData = error.response?.data

                console.log('Error response data:', errorData)

                if (errorData?.errors) {
                    // Handle Django serializer errors
                    Object.entries(errorData.errors).forEach(([field, messages]) => {
                        if (Array.isArray(messages)) {
                            messages.forEach(msg => this.errors.push(`${field}: ${msg}`))
                        }
                    })
                } else if (errorData?.error) {
                    this.errors.push(errorData.error)
                } else {
                    this.errors.push('Login failed. Please try again.')
                }

                // Show first error in toast
                this.toastStore.showToast(
                    5000, 
                    this.errors[0] || 'Login failed', 
                    'bg-mykonos-error text-mykonos-textPrimary'
                )
            }
        }
    }
}
</script>
