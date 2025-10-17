import { createRouter, createWebHistory } from 'vue-router'
import Home from '@/views/Home.vue'
import Blog from '@/views/Blog.vue'
import BlogDetail from '@/components/Blog/BlogDetail.vue'
import Note from '@/views/Note.vue'
import About from '@/views/About.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      redirect: '/home'
    },
    {
      path: '/home',
      name: 'home',
      component: Home
    },
    {
      path: '/blog',
      name: 'blog',
      component: Blog
    },
    {
      path: '/blog/:slug',
      name: 'BlogDetail',
      component: BlogDetail,
      props: true
    },
    {
      path: '/note',
      name: 'note',
      component: Note
    },
    {
      path: '/note/:id',
      name: 'note-detail',
      component: Note,
      props: true
    },
    {
      path: '/about',
      name: 'about',
      component: About
    }
  ]
})

export default router
