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
                <form class="space-y-6">
                    <div>
                        <label class="text-mykonos-textPrimary">Username</label><br/>
                        <input type="text" placeholder="Your desired username" class="w-full mt-2 py-4 px-6 border border-mykonos-secondary rounded-lg text-mykonos-textSecondary"/>
                    </div>

                    <div>
                        <label class="text-mykonos-textPrimary">E-mail</label><br/>
                        <input type="email" placeholder="Your e-mail address" class="w-full mt-2 py-4 px-6 border border-mykonos-secondary rounded-lg text-mykonos-textSecondary"/>
                    </div>

                    <div>
                        <label class="text-mykonos-textPrimary">Password</label><br/>
                        <input type="password"  placeholder="Your desired password" class="w-full mt-2 py-4 px-6 border border-mykonos-secondary rounded-lg text-mykonos-textSecondary"/>
                    </div>

                    <div>
                        <label class="text-mykonos-textPrimary">Repeat password</label><br/>
                        <input type="password" placeholder="Repeat your desired password" class="w-full mt-2 py-4 px-6 border border-mykonos-secondary rounded-lg text-mykonos-textSecondary"/>
                    </div>

                    <div>
                        <button class="py-4 px-6 bg-mykonos-primary text-mykonos-accent rounded-lg">Sign up</button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>

<script>
export default {
  name: 'SignupView'
}
</script>
