import user_home from '@/components/user/user_home.vue'
import my_book from '@/components/user/my_books.vue'
import stat_page from '@/components/admin/admin_stat.vue'
export default [
    {
        path: '/user/home',
        component: user_home
    },
    {
        name: 'myBooks',
        path: '/my_books',
        component: my_book
    },

    {
        name: 'statPage',
        path: '/statUser',
        component : stat_page
    }
]