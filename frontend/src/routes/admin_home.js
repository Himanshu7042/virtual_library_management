import admin_home from '@/components/admin/admin_home.vue'
import first_Page from '@/components/first_page/first_page.vue'
import request_page from '@/components/admin/book_requests.vue'
import stat_page from '@/components/admin/admin_stat.vue'

export default [
    {
        path: '/admin/home',
        component: admin_home
    },
    {
        name: 'firstPage',
        path: '/',
        component: first_Page
    },
    {
        name: 'requestPage',
        path: '/book_requests',
        component: request_page
    },
    {
        name: 'statPage',
        path: '/statAdmin',
        component : stat_page
    }
]