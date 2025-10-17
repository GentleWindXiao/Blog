import { defineStore } from 'pinia'
import { fetchBlogDetail, likeBlog as likeBlogApi, viewBlog as viewBlogApi } from '@/api/blogs'

export const useBlogDetailStore = defineStore('blogDetail', {
  state: () => ({
    blog: null,
    loading: false,
    error: null
  }),

  getters: {
    getBlog: (state) => state.blog,
    isLoading: (state) => state.loading,
    hasError: (state) => state.error !== null
  },

  actions: {
    // 获取博客详情
    async fetchBlogBySlug(slug) {
      this.loading = true
      this.error = null
      try {
        const res = await fetchBlogDetail(slug)
        this.blog = res.data
      } catch (err) {
        this.error = err?.message || '获取博客详情失败'
        console.error('fetchBlogBySlug error:', err)
      } finally {
        this.loading = false
      }
    },

    // 点赞博客
    async likeBlog(slug) {
      try {
        await likeBlogApi(slug)
        if (this.blog && this.blog.slug === slug) {
          // 使用后端返回的字段名：likes_count
          this.blog.likes_count = (this.blog.likes_count || 0) + 1
        }
      } catch (err) {
        this.error = err?.message || '点赞失败'
        console.error('likeBlog error:', err)
      }
    },

    // 增加浏览量
    async viewBlog(slug) {
      try {
        await viewBlogApi(slug)
        if (this.blog && this.blog.slug === slug) {
          // 使用后端返回的字段名：views_count
          this.blog.views_count = (this.blog.views_count || 0) + 1
        }
      } catch (err) {
        this.error = err?.message || '记录浏览失败'
        console.error('viewBlog error:', err)
      }
    },

    // 清理当前详情
    clearBlog() {
      this.blog = null
      this.error = null
    }
  }
})