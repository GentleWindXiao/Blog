<template>
  <div class="home">
    <!-- 英雄区域 -->
    <section class="hero">
      <div class="hero-content">
        <h1>欢迎来到我的博客</h1>
        <p>分享技术心得，记录成长历程</p>
        <div class="hero-actions">
          <button @click="goToBlog" class="btn-primary">浏览文章</button>
          <button @click="goToAbout" class="btn-secondary">了解更多</button>
        </div>
      </div>
      <div class="hero-image">
        <img src="/images/blog-hero.jpg" alt="博客首页" />
      </div>
    </section>

    <!-- 最新文章 -->
    <section class="latest-posts">
      <div class="section-header">
        <h2>最新文章</h2>
        <button @click="goToBlog" class="view-all-btn">查看全部 →</button>
      </div>
      
      <div class="posts-grid" v-if="!loading">
        <article 
          v-for="post in latestPosts" 
          :key="post.id" 
          class="post-card"
          @click="goToPost(post.id)"
        >
          <div class="post-image" v-if="post.featured_image">
            <img :src="post.featured_image" :alt="post.title" />
          </div>
          <div class="post-content">
            <div class="post-meta">
              <span class="post-date">{{ formatDate(post.created_at) }}</span>
              <span class="post-category">{{ post.category?.name || '未分类' }}</span>
            </div>
            <h3 class="post-title">{{ post.title }}</h3>
            <p class="post-excerpt">{{ post.excerpt || post.content?.substring(0, 120) + '...' }}</p>
            <div class="post-footer">
              <div class="post-author">
                <img :src="post.author?.avatar || '/default-avatar.png'" :alt="post.author?.name" />
                <span>{{ post.author?.name || '匿名用户' }}</span>
              </div>
              <div class="post-stats">
                <span>👁 {{ post.views || 0 }}</span>
                <span>❤️ {{ post.likes || 0 }}</span>
              </div>
            </div>
          </div>
        </article>
      </div>

      <!-- 加载状态 -->
      <div v-if="loading" class="loading">
        <div class="spinner"></div>
        <p>加载中...</p>
      </div>
    </section>

    <!-- 热门标签 -->
    <section class="popular-tags">
      <h2>热门标签</h2>
      <div class="tags-cloud">
        <span 
          v-for="tag in popularTags" 
          :key="tag.id" 
          class="tag"
          :style="{ fontSize: getTagSize(tag.count) + 'px' }"
          @click="searchByTag(tag.name)"
        >
          #{{ tag.name }}
        </span>
      </div>
    </section>

    <!-- 统计数据 -->
    <section class="stats">
      <div class="stats-grid">
        <div class="stat-item">
          <div class="stat-number">{{ totalPosts }}</div>
          <div class="stat-label">文章总数</div>
        </div>
        <div class="stat-item">
          <div class="stat-number">{{ totalViews }}</div>
          <div class="stat-label">总阅读量</div>
        </div>
        <div class="stat-item">
          <div class="stat-number">{{ totalComments }}</div>
          <div class="stat-label">评论总数</div>
        </div>
        <div class="stat-item">
          <div class="stat-number">{{ totalTags }}</div>
          <div class="stat-label">标签数量</div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

// 响应式数据
const loading = ref(false)
const latestPosts = ref([])
const popularTags = ref([])
const totalPosts = ref(0)
const totalViews = ref(0)
const totalComments = ref(0)
const totalTags = ref(0)

// 模拟数据
const mockLatestPosts = [
  {
    id: 1,
    title: 'Vue.js 3 组合式API完全指南',
    content: 'Vue.js 3 引入了组合式API，这是一个全新的方式来编写组件逻辑...',
    excerpt: 'Vue.js 3 引入了组合式API，这是一个全新的方式来编写组件逻辑，让我们来看看如何使用它。',
    created_at: '2024-01-15T10:00:00Z',
    views: 1250,
    likes: 45,
    category: { id: 'tech', name: '技术' },
    author: {
      id: 1,
      name: '张三',
      avatar: '/avatars/user1.jpg'
    },
    featured_image: '/images/vue3-guide.jpg'
  },
  {
    id: 2,
    title: 'Django REST Framework 最佳实践',
    content: '在构建API时，Django REST Framework提供了许多强大的功能...',
    excerpt: '在构建API时，Django REST Framework提供了许多强大的功能，本文将分享一些最佳实践。',
    created_at: '2024-01-12T14:30:00Z',
    views: 890,
    likes: 32,
    category: { id: 'tech', name: '技术' },
    author: {
      id: 1,
      name: '张三',
      avatar: '/avatars/user1.jpg'
    },
    featured_image: '/images/django-api.jpg'
  },
  {
    id: 3,
    title: '我的编程学习之路',
    content: '从零基础到成为一名程序员，这条路并不容易...',
    excerpt: '从零基础到成为一名程序员，这条路并不容易，但每一步都值得。',
    created_at: '2024-01-10T09:15:00Z',
    views: 567,
    likes: 28,
    category: { id: 'life', name: '生活' },
    author: {
      id: 1,
      name: '张三',
      avatar: '/avatars/user1.jpg'
    }
  }
]

const mockPopularTags = [
  { id: 1, name: 'Vue.js', count: 15 },
  { id: 2, name: 'JavaScript', count: 12 },
  { id: 3, name: 'Django', count: 10 },
  { id: 4, name: 'Python', count: 8 },
  { id: 5, name: '前端', count: 6 },
  { id: 6, name: '后端', count: 5 },
  { id: 7, name: '学习', count: 4 },
  { id: 8, name: '生活', count: 3 }
]

// 方法
const loadLatestPosts = async () => {
  loading.value = true
  try {
    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 1000))
    latestPosts.value = mockLatestPosts
  } catch (error) {
    console.error('加载最新文章失败:', error)
  } finally {
    loading.value = false
  }
}

const loadStats = async () => {
  try {
    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 500))
    totalPosts.value = 25
    totalViews.value = 15680
    totalComments.value = 342
    totalTags.value = 18
  } catch (error) {
    console.error('加载统计数据失败:', error)
  }
}

const loadPopularTags = async () => {
  try {
    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 300))
    popularTags.value = mockPopularTags
  } catch (error) {
    console.error('加载热门标签失败:', error)
  }
}

const goToBlog = () => {
  router.push('/blog')
}

const goToAbout = () => {
  router.push('/about')
}

const goToPost = (postId) => {
  router.push(`/post/${postId}`)
}

const searchByTag = (tagName) => {
  router.push(`/blog?tag=${encodeURIComponent(tagName)}`)
}

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

const getTagSize = (count) => {
  // 根据标签使用次数计算字体大小
  const minSize = 12
  const maxSize = 24
  const maxCount = Math.max(...popularTags.value.map(tag => tag.count))
  return minSize + (count / maxCount) * (maxSize - minSize)
}

// 生命周期
onMounted(() => {
  loadLatestPosts()
  loadStats()
  loadPopularTags()
})
</script>

<style scoped>
.home {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
}

/* 英雄区域 */
.hero {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 3rem;
  align-items: center;
  margin-bottom: 4rem;
  padding: 3rem 0;
}

.hero-content {
  text-align: left;
}

.hero-content h1 {
  font-size: 3.5rem;
  color: #2c3e50;
  margin-bottom: 1rem;
  line-height: 1.2;
}

.hero-content p {
  font-size: 1.3rem;
  color: #7f8c8d;
  margin-bottom: 2rem;
}

.hero-actions {
  display: flex;
  gap: 1rem;
}

.btn-primary, .btn-secondary {
  padding: 0.8rem 2rem;
  border-radius: 25px;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s;
  border: none;
}

.btn-primary {
  background: #3498db;
  color: white;
}

.btn-primary:hover {
  background: #2980b9;
  transform: translateY(-2px);
}

.btn-secondary {
  background: transparent;
  color: #3498db;
  border: 2px solid #3498db;
}

.btn-secondary:hover {
  background: #3498db;
  color: white;
}

.hero-image {
  text-align: center;
}

.hero-image img {
  max-width: 100%;
  height: 400px;
  object-fit: cover;
  border-radius: 12px;
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
}

/* 最新文章 */
.latest-posts {
  margin-bottom: 4rem;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.section-header h2 {
  font-size: 2.5rem;
  color: #2c3e50;
  margin: 0;
}

.view-all-btn {
  background: none;
  border: none;
  color: #3498db;
  font-size: 1rem;
  cursor: pointer;
  transition: color 0.3s;
}

.view-all-btn:hover {
  color: #2980b9;
}

.posts-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 2rem;
}

.post-card {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s, box-shadow 0.3s;
  cursor: pointer;
}

.post-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
}

.post-image {
  width: 100%;
  height: 200px;
  overflow: hidden;
}

.post-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.post-content {
  padding: 1.5rem;
}

.post-meta {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
  font-size: 0.9rem;
  color: #7f8c8d;
}

.post-title {
  font-size: 1.3rem;
  color: #2c3e50;
  margin-bottom: 0.5rem;
  line-height: 1.4;
}

.post-excerpt {
  color: #7f8c8d;
  line-height: 1.6;
  margin-bottom: 1rem;
}

.post-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.post-author {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.9rem;
  color: #7f8c8d;
}

.post-author img {
  width: 24px;
  height: 24px;
  border-radius: 50%;
}

.post-stats {
  display: flex;
  gap: 1rem;
  font-size: 0.9rem;
  color: #7f8c8d;
}

/* 热门标签 */
.popular-tags {
  margin-bottom: 4rem;
  text-align: center;
}

.popular-tags h2 {
  font-size: 2.5rem;
  color: #2c3e50;
  margin-bottom: 2rem;
}

.tags-cloud {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 1rem;
}

.tag {
  background: #ecf0f1;
  color: #7f8c8d;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  cursor: pointer;
  transition: all 0.3s;
  display: inline-block;
}

.tag:hover {
  background: #3498db;
  color: white;
  transform: scale(1.05);
}

/* 统计数据 */
.stats {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 12px;
  padding: 3rem;
  margin-bottom: 2rem;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 2rem;
}

.stat-item {
  text-align: center;
  color: white;
}

.stat-number {
  font-size: 3rem;
  font-weight: bold;
  margin-bottom: 0.5rem;
}

.stat-label {
  font-size: 1.1rem;
  opacity: 0.9;
}

/* 加载状态 */
.loading {
  text-align: center;
  padding: 3rem;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #3498db;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 1rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* 响应式设计 */
@media (max-width: 768px) {
  .hero {
    grid-template-columns: 1fr;
    text-align: center;
  }
  
  .hero-content h1 {
    font-size: 2.5rem;
  }
  
  .hero-actions {
    justify-content: center;
  }
  
  .section-header {
    flex-direction: column;
    gap: 1rem;
    text-align: center;
  }
  
  .posts-grid {
    grid-template-columns: 1fr;
  }
  
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .tags-cloud {
    justify-content: flex-start;
  }
}

@media (max-width: 480px) {
  .home {
    padding: 0 0.5rem;
  }
  
  .hero-content h1 {
    font-size: 2rem;
  }
  
  .hero-actions {
    flex-direction: column;
  }
  
  .stats-grid {
    grid-template-columns: 1fr;
  }
}
</style>
