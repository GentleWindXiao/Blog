<template>
  <div class="post">
    <!-- 加载状态 -->
    <div v-if="loading" class="loading">
      <div class="spinner"></div>
      <p>加载中...</p>
    </div>

    <!-- 文章内容 -->
    <article v-else-if="post" class="post-content">
      <!-- 文章头部 -->
      <header class="post-header">
        <div class="post-meta">
          <span class="post-date">{{ formatDate(post.created_at) }}</span>
          <span class="post-category">{{ post.category?.name || '未分类' }}</span>
          <span class="post-views">👁 {{ post.views || 0 }} 次阅读</span>
        </div>
        
        <h1 class="post-title">{{ post.title }}</h1>
        
        <div class="post-author">
          <img :src="post.author?.avatar || '/default-avatar.png'" :alt="post.author?.name" />
          <div class="author-info">
            <span class="author-name">{{ post.author?.name || '匿名用户' }}</span>
            <span class="author-title">{{ post.author?.title || '作者' }}</span>
          </div>
        </div>
      </header>

      <!-- 文章特色图片 -->
      <div v-if="post.featured_image" class="post-featured-image">
        <img :src="post.featured_image" :alt="post.title" />
      </div>

      <!-- 文章正文 -->
      <div class="post-body">
        <div v-html="post.content" class="post-text"></div>
      </div>

      <!-- 文章标签 -->
      <div v-if="post.tags && post.tags.length > 0" class="post-tags">
        <h3>标签</h3>
        <div class="tags-list">
          <span 
            v-for="tag in post.tags" 
            :key="tag.id" 
            class="tag"
            @click="searchByTag(tag.name)"
          >
            #{{ tag.name }}
          </span>
        </div>
      </div>

      <!-- 文章操作 -->
      <div class="post-actions">
        <button @click="toggleLike" :class="{ liked: isLiked }" class="action-btn like-btn">
          <span v-if="isLiked">❤️</span>
          <span v-else>🤍</span>
          {{ post.likes || 0 }}
        </button>
        
        <button @click="toggleBookmark" :class="{ bookmarked: isBookmarked }" class="action-btn bookmark-btn">
          <span v-if="isBookmarked">🔖</span>
          <span v-else>📑</span>
          {{ isBookmarked ? '已收藏' : '收藏' }}
        </button>
        
        <button @click="sharePost" class="action-btn share-btn">
          📤 分享
        </button>
      </div>

      <!-- 相关文章 -->
      <section v-if="relatedPosts.length > 0" class="related-posts">
        <h3>相关文章</h3>
        <div class="related-list">
          <div 
            v-for="relatedPost in relatedPosts" 
            :key="relatedPost.id"
            class="related-item"
            @click="goToPost(relatedPost.id)"
          >
            <div class="related-image" v-if="relatedPost.featured_image">
              <img :src="relatedPost.featured_image" :alt="relatedPost.title" />
            </div>
            <div class="related-content">
              <h4>{{ relatedPost.title }}</h4>
              <p>{{ relatedPost.excerpt || relatedPost.content?.substring(0, 100) + '...' }}</p>
              <span class="related-date">{{ formatDate(relatedPost.created_at) }}</span>
            </div>
          </div>
        </div>
      </section>

      <!-- 评论区 -->
      <section class="comments-section">
        <h3>评论 ({{ comments.length }})</h3>
        
        <!-- 发表评论 -->
        <div class="comment-form">
          <textarea 
            v-model="newComment" 
            placeholder="写下你的想法..."
            rows="4"
          ></textarea>
          <button @click="submitComment" :disabled="!newComment.trim()" class="submit-btn">
            发表评论
          </button>
        </div>

        <!-- 评论列表 -->
        <div class="comments-list">
          <div 
            v-for="comment in comments" 
            :key="comment.id" 
            class="comment-item"
          >
            <img :src="comment.author?.avatar || '/default-avatar.png'" :alt="comment.author?.name" />
            <div class="comment-content">
              <div class="comment-header">
                <span class="comment-author">{{ comment.author?.name || '匿名用户' }}</span>
                <span class="comment-date">{{ formatDate(comment.created_at) }}</span>
              </div>
              <div class="comment-text">{{ comment.content }}</div>
              <div class="comment-actions">
                <button @click="likeComment(comment.id)" class="comment-action">
                  👍 {{ comment.likes || 0 }}
                </button>
                <button @click="replyToComment(comment.id)" class="comment-action">
                  回复
                </button>
              </div>
            </div>
          </div>
        </div>
      </section>
    </article>

    <!-- 文章不存在 -->
    <div v-else class="not-found">
      <h2>文章不存在</h2>
      <p>抱歉，您访问的文章不存在或已被删除。</p>
      <button @click="goBack" class="back-btn">返回</button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

// 响应式数据
const post = ref(null)
const loading = ref(false)
const isLiked = ref(false)
const isBookmarked = ref(false)
const newComment = ref('')
const comments = ref([])
const relatedPosts = ref([])

// 模拟数据
const mockPost = {
  id: 1,
  title: 'Vue.js 3 组合式API完全指南',
  content: `
    <h2>什么是组合式API？</h2>
    <p>Vue.js 3 引入了组合式API，这是一个全新的方式来编写组件逻辑。与选项式API不同，组合式API允许我们使用函数来组织代码，使代码更加灵活和可复用。</p>
    
    <h3>为什么需要组合式API？</h3>
    <p>在大型项目中，选项式API可能会导致以下问题：</p>
    <ul>
      <li>代码逻辑分散在不同的选项中，难以追踪</li>
      <li>组件变得难以理解和维护</li>
      <li>逻辑复用变得困难</li>
    </ul>
    
    <h3>基本用法</h3>
    <p>让我们来看一个简单的例子：</p>
    <pre><code>
import { ref, computed, onMounted } from 'vue'

export default {
  setup() {
    const count = ref(0)
    const doubleCount = computed(() => count.value * 2)
    
    const increment = () => {
      count.value++
    }
    
    onMounted(() => {
      console.log('组件已挂载')
    })
    
    return {
      count,
      doubleCount,
      increment
    }
  }
}
    </code></pre>
    
    <h3>总结</h3>
    <p>组合式API为Vue.js带来了更强大的功能，让代码组织更加灵活。虽然学习曲线可能稍陡，但一旦掌握，它将大大提高开发效率。</p>
  `,
  created_at: '2024-01-15T10:00:00Z',
  updated_at: '2024-01-15T10:00:00Z',
  views: 1250,
  likes: 45,
  category: { id: 'tech', name: '技术' },
  tags: [
    { id: 1, name: 'Vue.js' },
    { id: 2, name: 'JavaScript' },
    { id: 3, name: '前端' }
  ],
  author: {
    id: 1,
    name: '张三',
    title: '前端工程师',
    avatar: '/avatars/user1.jpg'
  },
  featured_image: '/images/vue3-guide.jpg'
}

const mockComments = [
  {
    id: 1,
    content: '写得很好，学到了很多！',
    created_at: '2024-01-15T11:00:00Z',
    likes: 5,
    author: {
      id: 2,
      name: '李四',
      avatar: '/avatars/user2.jpg'
    }
  },
  {
    id: 2,
    content: '组合式API确实比选项式API更灵活，感谢分享！',
    created_at: '2024-01-15T12:30:00Z',
    likes: 3,
    author: {
      id: 3,
      name: '王五',
      avatar: '/avatars/user3.jpg'
    }
  }
]

const mockRelatedPosts = [
  {
    id: 2,
    title: 'Django REST Framework 最佳实践',
    excerpt: '在构建API时，Django REST Framework提供了许多强大的功能...',
    created_at: '2024-01-12T14:30:00Z',
    featured_image: '/images/django-api.jpg'
  },
  {
    id: 3,
    title: '我的编程学习之路',
    excerpt: '从零基础到成为一名程序员，这条路并不容易...',
    created_at: '2024-01-10T09:15:00Z'
  }
]

// 方法
const loadPost = async (postId) => {
  loading.value = true
  try {
    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 1000))
    post.value = mockPost
    comments.value = mockComments
    relatedPosts.value = mockRelatedPosts
  } catch (error) {
    console.error('加载文章失败:', error)
  } finally {
    loading.value = false
  }
}

const toggleLike = () => {
  isLiked.value = !isLiked.value
  if (isLiked.value) {
    post.value.likes++
  } else {
    post.value.likes--
  }
}

const toggleBookmark = () => {
  isBookmarked.value = !isBookmarked.value
}

const sharePost = () => {
  if (navigator.share) {
    navigator.share({
      title: post.value.title,
      text: post.value.excerpt,
      url: window.location.href
    })
  } else {
    // 复制链接到剪贴板
    navigator.clipboard.writeText(window.location.href)
    alert('链接已复制到剪贴板')
  }
}

const searchByTag = (tagName) => {
  router.push(`/blog?tag=${encodeURIComponent(tagName)}`)
}

const goToPost = (postId) => {
  router.push(`/post/${postId}`)
}

const goBack = () => {
  router.back()
}

const submitComment = () => {
  if (!newComment.value.trim()) return
  
  const comment = {
    id: Date.now(),
    content: newComment.value,
    created_at: new Date().toISOString(),
    likes: 0,
    author: {
      id: 1,
      name: '当前用户',
      avatar: '/avatars/current-user.jpg'
    }
  }
  
  comments.value.unshift(comment)
  newComment.value = ''
}

const likeComment = (commentId) => {
  const comment = comments.value.find(c => c.id === commentId)
  if (comment) {
    comment.likes++
  }
}

const replyToComment = (commentId) => {
  // 实现回复功能
  console.log('回复评论:', commentId)
}

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

// 监听路由变化
watch(() => route.params.id, (newId) => {
  if (newId) {
    loadPost(newId)
  }
}, { immediate: true })

// 生命周期
onMounted(() => {
  const postId = route.params.id
  if (postId) {
    loadPost(postId)
  }
})
</script>

<style scoped>
.post {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem;
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

.post-content {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.post-header {
  padding: 2rem;
  border-bottom: 1px solid #ecf0f1;
}

.post-meta {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
  font-size: 0.9rem;
  color: #7f8c8d;
}

.post-title {
  font-size: 2.5rem;
  color: #2c3e50;
  margin-bottom: 1.5rem;
  line-height: 1.3;
}

.post-author {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.post-author img {
  width: 48px;
  height: 48px;
  border-radius: 50%;
}

.author-info {
  display: flex;
  flex-direction: column;
}

.author-name {
  font-weight: bold;
  color: #2c3e50;
}

.author-title {
  font-size: 0.9rem;
  color: #7f8c8d;
}

.post-featured-image {
  width: 100%;
  height: 400px;
  overflow: hidden;
}

.post-featured-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.post-body {
  padding: 2rem;
}

.post-text {
  line-height: 1.8;
  color: #2c3e50;
}

.post-text h2 {
  color: #2c3e50;
  margin: 2rem 0 1rem;
  border-bottom: 2px solid #3498db;
  padding-bottom: 0.5rem;
}

.post-text h3 {
  color: #2c3e50;
  margin: 1.5rem 0 0.5rem;
}

.post-text p {
  margin-bottom: 1rem;
}

.post-text ul, .post-text ol {
  margin-bottom: 1rem;
  padding-left: 2rem;
}

.post-text pre {
  background: #f8f9fa;
  padding: 1rem;
  border-radius: 6px;
  overflow-x: auto;
  margin: 1rem 0;
}

.post-text code {
  background: #f8f9fa;
  padding: 0.2rem 0.4rem;
  border-radius: 3px;
  font-family: 'Courier New', monospace;
}

.post-tags {
  padding: 0 2rem 2rem;
  border-bottom: 1px solid #ecf0f1;
}

.post-tags h3 {
  color: #2c3e50;
  margin-bottom: 1rem;
}

.tags-list {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.tag {
  background: #ecf0f1;
  color: #7f8c8d;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  cursor: pointer;
  transition: all 0.3s;
}

.tag:hover {
  background: #3498db;
  color: white;
}

.post-actions {
  display: flex;
  gap: 1rem;
  padding: 2rem;
  border-bottom: 1px solid #ecf0f1;
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  border: 1px solid #ddd;
  background: white;
  border-radius: 25px;
  cursor: pointer;
  transition: all 0.3s;
}

.action-btn:hover {
  background: #f8f9fa;
}

.action-btn.liked {
  background: #e74c3c;
  color: white;
  border-color: #e74c3c;
}

.action-btn.bookmarked {
  background: #f39c12;
  color: white;
  border-color: #f39c12;
}

.related-posts {
  padding: 2rem;
  border-bottom: 1px solid #ecf0f1;
}

.related-posts h3 {
  color: #2c3e50;
  margin-bottom: 1.5rem;
}

.related-list {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1rem;
}

.related-item {
  display: flex;
  gap: 1rem;
  padding: 1rem;
  border: 1px solid #ecf0f1;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s;
}

.related-item:hover {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.related-image {
  width: 80px;
  height: 80px;
  overflow: hidden;
  border-radius: 6px;
  flex-shrink: 0;
}

.related-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.related-content h4 {
  color: #2c3e50;
  margin-bottom: 0.5rem;
  font-size: 1rem;
}

.related-content p {
  color: #7f8c8d;
  font-size: 0.9rem;
  margin-bottom: 0.5rem;
}

.related-date {
  font-size: 0.8rem;
  color: #bdc3c7;
}

.comments-section {
  padding: 2rem;
}

.comments-section h3 {
  color: #2c3e50;
  margin-bottom: 1.5rem;
}

.comment-form {
  margin-bottom: 2rem;
}

.comment-form textarea {
  width: 100%;
  padding: 1rem;
  border: 1px solid #ddd;
  border-radius: 8px;
  resize: vertical;
  font-family: inherit;
  margin-bottom: 1rem;
}

.submit-btn {
  background: #3498db;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  cursor: pointer;
  transition: background 0.3s;
}

.submit-btn:hover:not(:disabled) {
  background: #2980b9;
}

.submit-btn:disabled {
  background: #bdc3c7;
  cursor: not-allowed;
}

.comments-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.comment-item {
  display: flex;
  gap: 1rem;
  padding: 1rem;
  border: 1px solid #ecf0f1;
  border-radius: 8px;
}

.comment-item img {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  flex-shrink: 0;
}

.comment-content {
  flex: 1;
}

.comment-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.5rem;
}

.comment-author {
  font-weight: bold;
  color: #2c3e50;
}

.comment-date {
  font-size: 0.8rem;
  color: #7f8c8d;
}

.comment-text {
  color: #2c3e50;
  margin-bottom: 0.5rem;
  line-height: 1.6;
}

.comment-actions {
  display: flex;
  gap: 1rem;
}

.comment-action {
  background: none;
  border: none;
  color: #7f8c8d;
  cursor: pointer;
  font-size: 0.9rem;
  transition: color 0.3s;
}

.comment-action:hover {
  color: #3498db;
}

.not-found {
  text-align: center;
  padding: 3rem;
}

.not-found h2 {
  color: #2c3e50;
  margin-bottom: 1rem;
}

.back-btn {
  background: #3498db;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  cursor: pointer;
  margin-top: 1rem;
}

@media (max-width: 768px) {
  .post {
    padding: 1rem;
  }
  
  .post-title {
    font-size: 2rem;
  }
  
  .post-actions {
    flex-wrap: wrap;
  }
  
  .related-list {
    grid-template-columns: 1fr;
  }
  
  .comment-item {
    flex-direction: column;
  }
}
</style>
