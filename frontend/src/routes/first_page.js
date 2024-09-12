import first_Page from '@/components/first_page/first_page.vue'
import user_auth_page from '@/components/auth_page/user_auth.vue'
import admin_auth_page from '@/components/auth_page/admin_auth.vue'

export default[
    {
        path: '/',
        component: first_Page
    },
    {
        name: 'user_auth',
        path: '/user',
        component: user_auth_page
    },
    {
        name: 'admin_auth',
        path: '/admin',
        component: admin_auth_page
    }
]