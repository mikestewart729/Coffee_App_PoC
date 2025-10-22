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
                    Already have an account? <RouterLink :to="{name: 'login'}" class="text-mykonos-accent underline">Click here</RouterLink>
                    to sign in!
                </p>
            </div>
        </div>

        <div class="main-right">
            <div class="p-12 bg-mykonos-surface border border-mykonos-primary rounded-lg">
                <form class="space-y-6" v-on:submit.prevent="submitForm">
                    <div>
                        <label class="text-mykonos-textPrimary">Username</label><br/>
                        <input type="text" v-model=form.username placeholder="Your desired username" class="w-full mt-2 py-4 px-6 border border-mykonos-secondary rounded-lg text-mykonos-textSecondary"/>
                    </div>

                    <div>
                        <label class="text-mykonos-textPrimary">E-mail</label><br/>
                        <input type="email" v-model=form.email placeholder="Your e-mail address" class="w-full mt-2 py-4 px-6 border border-mykonos-secondary rounded-lg text-mykonos-textSecondary"/>
                    </div>

                    <div>
                        <label class="text-mykonos-textPrimary">Password</label><br/>
                        <input type="password" v-model="form.password1" placeholder="Your desired password" class="w-full mt-2 py-4 px-6 border border-mykonos-secondary rounded-lg text-mykonos-textSecondary"/>
                    </div>

                    <div>
                        <label class="text-mykonos-textPrimary">Repeat password</label><br/>
                        <input type="password" v-model="form.password2" placeholder="Repeat your desired password" class="w-full mt-2 py-4 px-6 border border-mykonos-secondary rounded-lg text-mykonos-textSecondary"/>
                    </div>

                    <template v-if="errors.length > 0">
                        <div class="bg-mykonos-error text-mykonos-textPrimary rounded-lg p-6">
                            <p v-for="error in errors" v-bind:key="error">{{ error }}</p>
                        </div>
                    </template>

                    <div>
                        <button class="py-4 px-6 bg-mykonos-primary text-mykonos-accent rounded-lg">Sign up</button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios'
import { useToastStore } from '@/stores/toast'

export default {
    setup() {
        const toastStore = useToastStore()

        return {
            toastStore
        }
    },

    data() {
        return {
            form: {
                email: '', 
                username: '',
                password1: '',
                password2: ''
            },
            errors: [],
        }
    },

    methods: {
        async submitForm() {
            this.errors = []

            if (this.form.email === '') {
                this.errors.push('Your e-mail is missing')
            }

            if (this.form.username === '') {
                this.errors.push('Your name is missing')
            }

            if (this.form.password1 === '') {
                this.errors.push('The password is missing')
            }

            if (this.form.password1 !== this.form.password2) {
                this.errors.push('The passwords do not match')
            }

            if (this.errors.length > 0) {
                return this.errors
            }

            try {
                const response = await axios.post('/signup/', {
                    username: this.form.username,
                    email: this.form.email,
                    password: this.form.password1
                })

                this.toastStore.showToast(
                    5000, 
                    'The user is registered. Please sign in..', 
                    'bg-mykonos-primary text-mykonos-accent'
                )

                this.form.email = ''
                this.form.username = ''
                this.form.password1 = ''
                this.form.password2 = ''

                // Redirect to login page
                console.log('Redirecting to login...')
                await this.$router.push('/login')
            } catch (error) {
                const errorData = error.response?.data

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
                    this.errors.push('Registration failed. Please try again.')
                }

                // Show first error in toast
                this.toastStore.showToast(
                    5000, 
                    this.errors[0] || 'Registration failed', 
                    'bg-mykonos-error text-mykonos-textPrimary'
                )
            }
        }
    }
}
</script>
