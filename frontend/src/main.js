import { createApp } from 'vue'
import App from './App.vue'
import { createWebHistory, createRouter } from 'vue-router'
import firstPage from './routes/first_page.js'
import adminHome from './routes/admin_home.js'
import userHome from './routes/user_home.js'

const router = createRouter({
    history: createWebHistory(),
    routes:[
        ...firstPage,
        ...adminHome,
        ...userHome
    ]
})

const app = createApp(App)
app.use(router)
app.mount('#app')
