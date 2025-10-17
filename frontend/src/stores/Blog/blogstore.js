import { defineStore } from 'pinia'
import { fetchBlogs, fetchBlogDetail, likeBlog, viewBlog } from '@/api/blogs'

export const useBlogStore = defineStore('blog', {
  state: () => ({
    blogs: [],
    currentBlog: null,
    loading: false,
    error: null
  }),
  
  getters: {
    getBlogs: (state) => state.blogs,
    getCurrentBlog: (state) => state.currentBlog,
    isLoading: (state) => state.loading,
    hasError: (state) => state.error !== null
  },
  
  actions: {
    /**
     * 获取所有博客列表
     * 从API获取所有博客并更新状态
     */
    async fetchAllBlogs() {
      this.loading = true
      this.error = null
      
      try {
        const response = await fetchBlogs()
        this.blogs = response.data.results
      } catch (error) {
        this.error = error.message || 'Failed to fetch blogs'
        console.error('Error fetching blogs:', error)
      } finally {
        this.loading = false
      }
    },
    
    /**
     * 根据slug获取单个博客详情
     * @param {string} slug - 博客的唯一标识符
     */
    async fetchBlogBySlug(slug) {
      this.loading = true
      this.error = null
      
      try {
        const response = await fetchBlogDetail(slug)
        this.currentBlog = response.data
      } catch (error) {
        this.error = error.message || 'Failed to fetch blog details'
        console.error('Error fetching blog details:', error)
      } finally {
        this.loading = false
      }
    },
    
    /**
     * 点赞博客
     * 发送点赞请求并更新本地状态
     * @param {string} slug - 要点赞的博客的唯一标识符
     */
    async likeBlogPost(slug) {
      try {
        await likeBlog(slug)
        
        // Update local state if the liked blog is the current blog
        if (this.currentBlog && this.currentBlog.slug === slug) {
          this.currentBlog.likes_count += 1
        }
        
        // Update in blogs list if present
        const blogIndex = this.blogs.findIndex(blog => blog.slug === slug)
        if (blogIndex !== -1) {
          this.blogs[blogIndex].likes_count += 1
        }
      } catch (error) {
        this.error = error.message || 'Failed to like blog'
        console.error('Error liking blog:', error)
      }
    },
    
    /**
     * 记录博客浏览量
     * 发送浏览请求并更新本地状态
     * @param {string} slug - 要记录浏览的博客的唯一标识符
     */
    async viewBlogPost(slug) {
      try {
        await viewBlog(slug)
        
        // Update local state if the viewed blog is the current blog
        if (this.currentBlog && this.currentBlog.slug === slug) {
          this.currentBlog.views_count += 1
        }
        
        // Update in blogs list if present
        const blogIndex = this.blogs.findIndex(blog => blog.slug === slug)
        if (blogIndex !== -1) {
          this.blogs[blogIndex].views_count += 1
        }
      } catch (error) {
        this.error = error.message || 'Failed to record blog view'
        console.error('Error recording blog view:', error)
      }
    },
    
    /**
     * 清除当前选中的博客
     * 重置currentBlog状态为null
     */
    clearCurrentBlog() {
      this.currentBlog = null
    },
    
    /**
     * 清除错误状态
     * 重置error状态为null
     */
    clearError() {
      this.error = null
    }
  }
})