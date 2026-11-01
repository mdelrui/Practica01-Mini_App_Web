import { createApp } from 'vue'
import { clerkPlugin } from '@clerk/vue'
import App from './App.vue'
import './style.css'

const publishableKey = import.meta.env.VITE_CLERK_PUBLISHABLE_KEY?.trim()

if (!publishableKey) {
  throw new Error('Falta VITE_CLERK_PUBLISHABLE_KEY')
}

const app = createApp(App)
app.use(clerkPlugin, { publishableKey })
app.mount('#app')
