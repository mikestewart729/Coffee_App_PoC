import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'

import App from './App.vue'
import router from './router'
import axios from 'axios'

const app = createApp(App)

const baseURL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000/api/'; 
console.log(import.meta.env.VITE_API_URL)

axios.defaults.baseURL = baseURL;

const pinia = createPinia()
pinia.use(piniaPluginPersistedstate)

app.use(pinia)
app.use(router)

app.config.globalProperties.$axios = axios

app.mount('#app')
