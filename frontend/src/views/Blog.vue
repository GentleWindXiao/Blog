<template>
  <div class="blog">
    <div class="blog-header">
      <h1>博客文章</h1>
      <p>分享技术心得与生活感悟</p>
    </div>

    <!-- 搜索和筛选 -->
    <div class="blog-filters">
      <div class="search-box">
        <input 
          v-model="searchQuery" 
          type="text" 
          placeholder="搜索文章..." 
          @input="handleSearch"
        />
        <button @click="handleSearch">🔍</button>
      </div>
      
      <div class="filter-tabs">
        <button 
          v-for="category in categories" 
          :key="category.id"
          :class="{ active: selectedCategory === category.id }"
          @click="selectCategory(category.id)"
        >
          {{ category.name }}
        </button>
      </div>
    </div>

    <!-- 文章列表 -->
    <div class="blog-list" v-if="!loading">
      <article 
        v-for="post in filteredPosts" 
        :key="post.id" 
        class="blog-card"
        @click="goToPost(post.id)"
      >
        <div class="blog-card-image" v-if="post.featured_image">
          <img :src="post.featured_image" :alt="post.title" />
        </div>
        
        <div class="blog-card-content">
          <div class="blog-meta">
            <span class="blog-date">{{ formatDate(post.created_at) }}</span>
            <span class="blog-category">{{ post.category?.name || '未分类' }}</span>
            <span class="blog-views">👁 {{ post.views || 0 }}</span>
          </div>
          
          <h2 class="blog-title">{{ post.title }}</h2>
          <p class="blog-excerpt">{{ post.excerpt || post.content?.substring(0, 150) + '...' }}</p>
          
          <div class="blog-tags">
            <span 
              v-for="tag in post.tags" 
              :key="tag.id" 
              class="blog-tag"
            >
              #{{ tag.name }}
            </span>
          </div>
          
          <div class="blog-author">
            <img :src="post.author?.avatar || '/default-avatar.png'" :alt="post.author?.name" />
            <span>{{ post.author?.name || '匿名用户' }}</span>
          </div>
        </div>
      </article>
    </div>

    <!-- 加载状态 -->
    <div v-if="loading" class="loading">
      <div class="spinner"></div>
      <p>加载中...</p>
    </div>

    <!-- 空状态 -->
    <div v-if="!loading && filteredPosts.length === 0" class="empty-state">
      <h3>暂无文章</h3>
      <p>还没有发布任何文章，请稍后再来查看。</p>
    </div>

    <!-- 分页 -->
    <div v-if="totalPages > 1" class="pagination">
      <button 
        :disabled="currentPage === 1" 
        @click="changePage(currentPage - 1)"
      >
        上一页
      </button>
      
      <span class="page-info">
        第 {{ currentPage }} 页，共 {{ totalPages }} 页
      </span>
      
      <button 
        :disabled="currentPage === totalPages" 
        @click="changePage(currentPage + 1)"
      >
        下一页
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

// 响应式数据
const posts = ref([])
const loading = ref(false)
const searchQuery = ref('')
const selectedCategory = ref('all')
const currentPage = ref(1)
const pageSize = ref(10)

// 模拟数据
const categories = ref([
  { id: 'all', name: '全部' },
  { id: 'tech', name: '技术' },
  { id: 'life', name: '生活' },
  { id: 'tutorial', name: '教程' }
])

// 模拟文章数据
const mockPosts = ref([
  {
    id: 1,
    title: 'Vue.js 3 组合式API完全指南',
    content: 'Vue.js 3 引入了组合式API，这是一个全新的方式来编写组件逻辑...',
    excerpt: 'Vue.js 3 引入了组合式API，这是一个全新的方式来编写组件逻辑，让我们来看看如何使用它。',
    created_at: '2024-01-15T10:00:00Z',
    views: 1250,
    category: { id: 'tech', name: '技术' },
    tags: [
      { id: 1, name: 'Vue.js' },
      { id: 2, name: 'JavaScript' },
      { id: 3, name: '前端' }
    ],
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
    category: { id: 'tech', name: '技术' },
    tags: [
      { id: 4, name: 'Django' },
      { id: 5, name: 'Python' },
      { id: 6, name: 'API' }
    ],
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
    category: { id: 'life', name: '生活' },
    tags: [
      { id: 7, name: '学习' },
      { id: 8, name: '成长' },
      { id: 9, name: '感悟' }
    ],
    author: {
      id: 1,
      name: '张三',
      avatar: '/avatars/user1.jpg'
    }
  }
])

// 计算属性
const filteredPosts = computed(() => {
  let filtered = posts.value

  // 按分类筛选
  if (selectedCategory.value !== 'all') {
    filtered = filtered.filter(post => post.category?.id === selectedCategory.value)
  }

  // 按搜索关键词筛选
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(post => 
      post.title.toLowerCase().includes(query) ||
      post.content.toLowerCase().includes(query) ||
      post.tags.some(tag => tag.name.toLowerCase().includes(query))
    )
  }

  return filtered
})

const totalPages = computed(() => {
  return Math.ceil(filteredPosts.value.length / pageSize.value)
})

// 方法
const loadPosts = async () => {
  loading.value = true
  try {
    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 1000))
    posts.value = mockPosts.value
  } catch (error) {
    console.error('加载文章失败:', error)
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  currentPage.value = 1
}

const selectCategory = (categoryId) => {
  selectedCategory.value = categoryId
  currentPage.value = 1
}

const goToPost = (postId) => {
  router.push(`/post/${postId}`)
}

const changePage = (page) => {
  if (page >= 1 && page <= totalPages.value) {
    currentPage.value = page
  }
}

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

// 生命周期
onMounted(() => {
  loadPosts()
})
</script>

<style scoped>
.blog {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.blog-header {
  text-align: center;
  margin-bottom: 3rem;
}

.blog-header h1 {
  font-size: 2.5rem;
  color: #2c3e50;
  margin-bottom: 0.5rem;
}

.blog-header p {
  font-size: 1.1rem;
  color: #7f8c8d;
}

.blog-filters {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  flex-wrap: wrap;
  gap: 1rem;
}

.search-box {
  display: flex;
  align-items: center;
  background: white;
  border-radius: 25px;
  padding: 0.5rem 1rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.search-box input {
  border: none;
  outline: none;
  padding: 0.5rem;
  font-size: 1rem;
  width: 300px;
}

.search-box button {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1.2rem;
  padding: 0.5rem;
}

.filter-tabs {
  display: flex;
  gap: 0.5rem;
}

.filter-tabs button {
  padding: 0.5rem 1rem;
  border: 1px solid #ddd;
  background: white;
  border-radius: 20px;
  cursor: pointer;
  transition: all 0.3s;
}

.filter-tabs button:hover,
.filter-tabs button.active {
  background: #3498db;
  color: white;
  border-color: #3498db;
}

.blog-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 2rem;
  margin-bottom: 2rem;
}

.blog-card {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s, box-shadow 0.3s;
  cursor: pointer;
}

.blog-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
}

.blog-card-image {
  width: 100%;
  height: 200px;
  overflow: hidden;
}

.blog-card-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.blog-card-content {
  padding: 1.5rem;
}

.blog-meta {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
  font-size: 0.9rem;
  color: #7f8c8d;
}

.blog-title {
  font-size: 1.3rem;
  color: #2c3e50;
  margin-bottom: 0.5rem;
  line-height: 1.4;
}

.blog-excerpt {
  color: #7f8c8d;
  line-height: 1.6;
  margin-bottom: 1rem;
}

.blog-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.blog-tag {
  background: #ecf0f1;
  color: #7f8c8d;
  padding: 0.25rem 0.5rem;
  border-radius: 12px;
  font-size: 0.8rem;
}

.blog-author {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.9rem;
  color: #7f8c8d;
}

.blog-author img {
  width: 24px;
  height: 24px;
  border-radius: 50%;
}

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

.empty-state {
  text-align: center;
  padding: 3rem;
  color: #7f8c8d;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1rem;
  margin-top: 2rem;
}

.pagination button {
  padding: 0.5rem 1rem;
  border: 1px solid #ddd;
  background: white;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s;
}

.pagination button:hover:not(:disabled) {
  background: #3498db;
  color: white;
  border-color: #3498db;
}

.pagination button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.page-info {
  color: #7f8c8d;
  font-size: 0.9rem;
}

@media (max-width: 768px) {
  .blog {
    padding: 1rem;
  }
  
  .blog-filters {
    flex-direction: column;
    align-items: stretch;
  }
  
  .search-box input {
    width: 100%;
  }
  
  .blog-list {
    grid-template-columns: 1fr;
  }
}
</style>
