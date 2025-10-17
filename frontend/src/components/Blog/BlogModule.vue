<template>
    <section class="blog-module">
      <div class="module-header">
        <h2>最新博客</h2>
        <router-link to="/blog" class="view-all">查看全部</router-link>
      </div>
      <div class="blog-list">
        <div 
          class="blog-card" 
          v-for="post in displayedPosts" 
          :key="post.id" 
          @click="viewBlog(post.slug)"
        >
          <h3>{{ post.title }}</h3>
          <p class="blog-excerpt">{{ post.excerpt || '暂无摘要' }}</p>
          <div class="blog-meta">
            <span class="blog-date">{{ formatDate(post.created_at) }}</span>
            <div class="blog-stats">
              <span class="blog-views"><i class="icon-eye">👁️</i> {{ post.views_count }}</span>
              <span class="blog-likes"><i class="icon-heart">❤️</i> {{ post.likes_count }}</span>
            </div>
          </div>
        </div>
      </div>
      <div v-if="isLoading" class="loading">加载中...</div>
      <div v-if="hasError" class="error">加载失败: {{ error }}</div>
    </section>
  </template>
  
  <script setup>
  import { onMounted } from 'vue'
  import { storeToRefs } from 'pinia'
  import { useBlogStore } from '@/stores/Blog/blogstore'
  import { useRouter } from 'vue-router'
  
  const blogStore = useBlogStore()
  const { getBlogs: blogs, isLoading, hasError, error } = storeToRefs(blogStore)
  const router = useRouter()
  
  // 获取前3篇博客用于展示
  const displayedPosts = blogs.value?.slice(0, 3) || []
  
  // 格式化日期
  const formatDate = (dateString) => {
    const date = new Date(dateString)
    return date.toLocaleDateString('zh-CN', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    })
  }
  
  // 查看博客详情
  const viewBlog = (slug) => {
    router.push({ name: 'BlogDetail', params: { slug } })
  }
  
  // 组件挂载时获取博客数据
  onMounted(() => {
    if (blogs.value.length === 0) {
      blogStore.fetchAllBlogs()
    }
  })
  </script>
  
  <style scoped>
.blog-module {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem 1rem;
}

.module-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.module-header h2 {
  font-size: 2rem;
  font-weight: 700;
  color: var(--header-color);
  margin: 0;
}

.view-all {
  color: var(--text-color);
  text-decoration: none;
  font-weight: 500;
  transition: all 0.3s ease;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  background: rgba(135, 203, 185, 0.15);
}

.view-all:hover {
  color: var(--text-color);
  background: rgba(135, 203, 185, 0.3);
}

.blog-list {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
}

.blog-card {
  background: var(--card-bg);
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 4px 12px var(--shadow-color);
  transition: all 0.3s ease;
  cursor: pointer;
  border: 1px solid var(--border-color);
}

.blog-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 12px 24px var(--shadow-color);
  border-color: #a3d9a5;
}

.blog-card h3 {
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--header-color);
  margin-bottom: 12px;
  line-height: 1.4;
}

.blog-excerpt {
  color: var(--meta-color);
  font-size: 0.95rem;
  line-height: 1.6;
  margin-bottom: 16px;
}

.blog-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.85rem;
  color: var(--meta-color);
  border-top: 1px solid var(--border-color);
  padding-top: 16px;
}

.blog-date {
  font-weight: 500;
}

.blog-stats {
  display: flex;
  gap: 12px;
}

.blog-views, .blog-likes {
  display: flex;
  align-items: center;
  gap: 4px;
}

.loading, .error {
  text-align: center;
  padding: 2rem;
  font-size: 1.1rem;
  color: #6b7280;
}

.error {
  color: #ef4444;
}

@media (max-width: 1024px) {
  .blog-list {
    grid-template-columns: repeat(2, 1fr);
    gap: 20px;
  }
  
  .module-header h2 {
    font-size: 1.75rem;
  }
}

@media (max-width: 768px) {
  .blog-module {
    padding: 1.5rem 1rem;
  }
  
  .module-header {
    flex-direction: column;
    gap: 1rem;
    align-items: flex-start;
  }
  
  .blog-list {
    grid-template-columns: 1fr;
    gap: 20px;
  }
  
  .blog-card {
    padding: 20px;
  }
  
  .module-header h2 {
    font-size: 1.5rem;
  }
}
</style>
  