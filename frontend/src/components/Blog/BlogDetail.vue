<template>
  <div class="blog-detail-container">
    <!-- 左侧目录导航栏 -->
    <aside class="toc-sidebar" :class="{ 'fixed': isTocFixed }">
      <div class="toc-header">
        <h3>目录</h3>
      </div>
      <div class="toc-content" v-if="tocAst && tocAst.length">
        <ul class="toc-list">
          <toc-item
            v-for="(item, index) in tocAst"
            :key="index"
            :item="item"
            :current-id="currentId"
            :expanded-ids="expandedIds"
            @scroll-to="scrollToHeading"
          />
        </ul>
      </div>
      <div class="toc-content empty" v-else>
        <p>暂无目录</p>
      </div>
    </aside>

    <!-- 主内容区域 -->
    <main class="main-content">
      <div v-if="isLoading" class="loading-state">
        <div class="spinner"></div>
        <p>加载中...</p>
      </div>
      
      <div v-else-if="hasError" class="error-state">
        <div class="error-icon">⚠️</div>
        <p>加载失败：{{ error }}</p>
        <button @click="retryFetch" class="retry-button">重新加载</button>
      </div>

      <article v-else-if="blog" class="blog-article">
        <!-- 文章标题 -->
        <header class="article-header">
          <h1 class="article-title">{{ blog.title }}</h1>
          
          <!-- 文章元信息 -->
          <div class="article-meta">
            <div class="meta-item">
              <i class="icon">👤</i>
              <span>{{ blog.author }}</span>
            </div>
            <div class="meta-item">
              <i class="icon">📅</i>
              <span>{{ formatDate(blog.created_at) }}</span>
            </div>
            <div class="meta-item">
              <i class="icon">👁️</i>
              <span>{{ blog.views_count }} 次浏览</span>
            </div>
            <div class="meta-item">
              <i class="icon">👍</i>
              <span>{{ blog.likes_count }} 次点赞</span>
            </div>
          </div>
        </header>

        <!-- 文章内容 -->
        <div class="article-content" v-html="renderedContent"></div>

        <!-- 点赞按钮 -->
        <div class="article-actions">
          <button 
            @click="handleLike" 
            :disabled="isLoading" 
            :class="['like-button', { liked: userLiked }]"
          >
            <span class="heart">❤️</span>
            <span>点赞</span>
            <span class="count">({{ blog.likes_count }})</span>
          </button>
        </div>
      </article>
    </main>
  </div>
  <BackToTop />
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount, nextTick } from 'vue'
import { useRoute } from 'vue-router'
import { storeToRefs } from 'pinia'
import { useBlogDetailStore } from '@/stores/Blog/blogDetailStore'
import MarkdownIt from 'markdown-it'
import mk from '@iktakahiro/markdown-it-katex'
import 'katex/dist/katex.min.css'
import anchor from 'markdown-it-anchor'
import toc from 'markdown-it-table-of-contents'
import TocItem from './TocItem.vue'
import BackToTop from '../common/BackToTop.vue'

const route = useRoute()
const slug = route.params.slug
const detailStore = useBlogDetailStore()
const { getBlog: blog, isLoading, hasError, error } = storeToRefs(detailStore)

// 目录相关状态
const tocAst = ref([])
const expandedIds = ref(new Set())
const currentId = ref('')
const isTocFixed = ref(false)

// 用户交互状态
const userLiked = ref(false)

// Markdown 渲染器
const md = new MarkdownIt({ 
  html: true, 
  linkify: true, 
  typographer: true,
  breaks: true
})

md.use(mk, { throwOnError: false, errorColor: '#cc0000' })

// 配置锚点插件
md.use(anchor, { 
  permalink: anchor.permalink.ariaHidden({ placement: 'before', symbol: '' }),
  tabIndex: false,
  slugify: (s) => encodeURIComponent(String(s).trim().toLowerCase().replace(/\s+/g, '-'))
})

// 渲染 Markdown 并生成 TOC
const renderedContent = computed(() => {
  if (!blog.value?.content_markdown) return ''
  console.log('Rendering markdown content:', blog.value.content_markdown);
  
  const result = md.render(blog.value.content_markdown);
  console.log('Rendered content result:', result);
  return result;
})

// 手动解析Markdown标题的函数
function parseMarkdownHeadings(markdown) {
  const lines = markdown.split('\n');
  const headings = [];
  const headingStack = []; // 用于跟踪标题层级
  
  lines.forEach((line, index) => {
    // 匹配Markdown标题 (#, ##, ###, etc.) - 改进正则表达式以处理各种情况
    // 包括标题前后空格、特殊字符、末尾#等情况
    const headingMatch = line.trim().match(/^(#{1,6})\s+(.+?)\s*#*\s*$/);
    if (headingMatch) {
      const level = headingMatch[1].length;
      let title = headingMatch[2].trim();
      
      // 移除末尾可能的 # 字符（Markdown 标题格式）
      title = title.replace(/\s+#*$/, '');
      
      // 生成ID（与markdown-it-anchor插件保持一致）
      const id = encodeURIComponent(title.toLowerCase().replace(/\s+/g, '-'));
      
      const heading = {
        content: title,
        anchor: id,
        level: level,
        id: id
      };
      
      // 处理层级关系 - 修复多级标题嵌套逻辑
      while (headingStack.length > 0 && headingStack[headingStack.length - 1].level >= level) {
        headingStack.pop();
      }
      
      if (headingStack.length === 0) {
        // 顶级标题
        headings.push(heading);
        headingStack.push(heading);
      } else {
        // 子标题
        const parent = headingStack[headingStack.length - 1];
        if (!parent.children) {
          parent.children = [];
        }
        parent.children.push(heading);
        headingStack.push(heading);
      }
    }
  });
  
  console.log('Generated headings structure:', headings);
  return headings;
}

// 格式化日期
function formatDate(dateStr) {
  return new Date(dateStr).toLocaleDateString('zh-CN', {
    year: 'numeric', month: 'long', day: 'numeric'
  })
}

// 滚动监听 & 高亮 & 父子折叠
function onScroll() {
  // 目录栏固定逻辑
  const scrollTop = window.pageYOffset || document.documentElement.scrollTop
  isTocFixed.value = scrollTop > 100

  // 标题高亮逻辑 - 改进可见性判断逻辑
  const headingElements = document.querySelectorAll('.article-content h1, .article-content h2, .article-content h3, .article-content h4, .article-content h5, .article-content h6')
  let current = ''
  
  // 找到当前可见的第一个标题 - 使用更精确的可见性判断
  for (let i = 0; i < headingElements.length; i++) {
    const el = headingElements[i]
    const rect = el.getBoundingClientRect()
    // 改进可见性判断逻辑，确保标题在视口中且不被导航栏遮挡
    if (rect.top >= 100 && rect.top <= window.innerHeight) {  // 标题元素在视口可见区域内
      current = el.id
      break // 找到第一个可见标题就停止
    }
    // 处理页面顶部的情况
    else if (rect.top <= 100 && rect.bottom >= 100) {
      current = el.id
    }
  }
  
  currentId.value = current

  // 展开当前标题的父级（只有在tocAst不为空时才执行）
  if (tocAst.value && tocAst.value.length > 0) {
    expandedIds.value.clear()

    function expandParents(items) {
      items.forEach(item => {
        // 检查当前项是否为活动项或其子项包含活动项
        const isCurrentOrHasCurrent = item.id === current || 
          (item.children && item.children.some(child => child.id === current))
        
        if (isCurrentOrHasCurrent) {
          expandedIds.value.add(item.id)
          // 递归展开子项
          if (item.children) {
            expandParents(item.children)
          }
        }
        // 递归检查子项
        else if (item.children && item.children.length > 0) {
          expandParents(item.children)
        }
      })
    }
    
    expandParents(tocAst.value)
  }
}

// 点击 TOC 跳转
function scrollToHeading(id) {
  const el = document.getElementById(id)
  if (el) {
    // 考虑固定导航栏的高度
    const navbarHeight = 100
    const elementPosition = el.getBoundingClientRect().top + window.pageYOffset
    const offsetPosition = elementPosition - navbarHeight

    window.scrollTo({
      top: offsetPosition,
      behavior: 'smooth'
    })
    
    // 点击后立即展开对应的目录项及其父级
    currentId.value = id
    
    // 展开当前标题的父级
    if (tocAst.value && tocAst.value.length > 0) {
      function expandParents(items) {
        items.forEach(item => {
          // 检查当前项是否为活动项或其子项包含活动项
          const isCurrentOrHasCurrent = item.id === id || 
            (item.children && item.children.some(child => child.id === id))
          
          if (isCurrentOrHasCurrent) {
            expandedIds.value.add(item.id)
            // 递归展开子项
            if (item.children) {
              expandParents(item.children)
            }
          }
          // 递归检查子项
          else if (item.children && item.children.length > 0) {
            expandParents(item.children)
          }
        })
      }
      
      expandParents(tocAst.value)
    }
  }
}

// 点赞功能
const handleLike = () => {
  if (slug && !userLiked.value) {
    detailStore.likeBlog(slug)
    userLiked.value = true
  }
}

// 重新加载
const retryFetch = () => {
  if (slug) {
    detailStore.fetchBlogBySlug(slug)
  }
}

// 组件挂载时获取数据
onMounted(async () => {
  if (!slug) return
  await detailStore.fetchBlogBySlug(slug)
  await detailStore.viewBlog(slug)
  
  // 在获取博客数据后生成目录
  if (blog.value?.content_markdown) {
    // 使用 nextTick 确保 DOM 更新后再生成目录
    nextTick(() => {
      const headings = parseMarkdownHeadings(blog.value.content_markdown);
      console.log('Parsed headings:', headings);
      tocAst.value = headings;
      
      // 初始化展开状态
      onScroll()
    })
  }
  
  window.addEventListener('scroll', onScroll)
  // 初始化展开当前段落
  onScroll()
})

// 组件卸载前清理事件监听器
onBeforeUnmount(() => {
  window.removeEventListener('scroll', onScroll)
})
</script>

<style scoped>
/* 整体布局 */
.blog-detail-container {
  display: flex;
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  gap: 40px;
}

/* 左侧目录导航栏 */
.toc-sidebar {
  width: 250px;
  flex-shrink: 0;
  position: absolute;
  left: calc(50% - 600px + 20px);
  top: 120px;
  transition: all 0.3s ease;
  background: rgba(255, 255, 255, 0.5);
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  padding: 20px;
  max-height: calc(100vh - 140px);
  overflow-y: auto;
  z-index: 10;
  border: 1px solid #eef2f7;
}

#app.dark-theme .toc-sidebar {
  background: rgba(40, 51, 46, 0.5);
  border: 1px solid var(--border-color);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.toc-sidebar.fixed {
  position: fixed;
  top: 20px;
  left: calc(50% - 600px + 20px);
}

.toc-header h3 {
  font-size: 18px;
  font-weight: 600;
  margin: 0 0 15px 0;
  padding-bottom: 10px;
  border-bottom: 1px solid #eee;
  color: #2c3e50;
}

#app.dark-theme .toc-header h3 {
  color: var(--text-color);
  border-bottom: 1px solid var(--border-color);
}

.toc-content {
  max-height: calc(100vh - 200px);
  overflow-y: auto;
}

.toc-content.empty {
  text-align: center;
  color: #999;
  font-style: italic;
  padding: 20px 0;
}

/* 目录列表样式 */
.toc-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

/* 主内容区域 */
.main-content {
  flex: 1;
  max-width: calc(100% - 290px);
  margin-left: 290px;
}

.blog-article {
  background: rgba(255, 255, 255, 0.5);
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  padding: 40px;
  border: 1px solid #eef2f7;
}

#app.dark-theme .blog-article {
  background: rgba(40, 51, 46, 0.5);
  border: 1px solid var(--border-color);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.article-title {
  font-size: 32px;
  font-weight: 700;
  color: #2c3e50;
  margin-bottom: 20px;
  line-height: 1.3;
}

#app.dark-theme .article-title {
  color: var(--text-color);
}

/* 文章元信息 */
.article-meta {
  display: flex;
  gap: 20px;
  padding: 15px 0;
  border-top: 1px solid #eee;
  border-bottom: 1px solid #eee;
  margin-bottom: 30px;
  color: #7f8c8d;
}

#app.dark-theme .article-meta {
  border-top: 1px solid var(--border-color);
  border-bottom: 1px solid var(--border-color);
  color: var(--meta-color);
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 14px;
}

.meta-item .icon {
  font-size: 16px;
}

/* 文章内容样式 */
.article-content {
  font-size: 16px;
  line-height: 1.8;
  color: #34495e;
}

#app.dark-theme .article-content {
  color: var(--text-color);
}

.article-content :deep(h1) {
  font-size: 28px;
  font-weight: 700;
  margin: 30px 0 20px 0;
  color: #2c3e50;
  padding-bottom: 10px;
  border-bottom: 2px solid #3498db;
}

#app.dark-theme .article-content :deep(h1) {
  color: var(--text-color);
  border-bottom: 2px solid var(--link-color);
}

.article-content :deep(h2) {
  font-size: 24px;
  font-weight: 600;
  margin: 25px 0 15px 0;
  color: #34495e;
  padding-bottom: 8px;
  border-bottom: 1px solid #eee;
}

#app.dark-theme .article-content :deep(h2) {
  color: var(--text-color);
  border-bottom: 1px solid var(--border-color);
}

.article-content :deep(h3) {
  font-size: 20px;
  font-weight: 600;
  margin: 20px 0 12px 0;
  color: #555;
}

#app.dark-theme .article-content :deep(h3) {
  color: var(--text-color);
}

.article-content :deep(h4) {
  font-size: 18px;
  font-weight: 600;
  margin: 18px 0 10px 0;
  color: #666;
}

#app.dark-theme .article-content :deep(h4) {
  color: var(--text-color);
}

.article-content :deep(p) {
  margin: 15px 0;
  text-align: justify;
}

.article-content :deep(ul), .article-content :deep(ol) {
  margin: 15px 0;
  padding-left: 30px;
}

.article-content :deep(li) {
  margin: 8px 0;
}

.article-content :deep(code) {
  background-color: #f8f9fa;
  padding: 2px 6px;
  border-radius: 4px;
  font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace;
  font-size: 14px;
  color: #e74c3c;
}

#app.dark-theme .article-content :deep(code) {
  background-color: var(--card-bg);
  color: #e74c3c;
}

.article-content :deep(pre) {
  background-color: #2c3e50;
  color: #ecf0f1;
  padding: 16px;
  border-radius: 8px;
  overflow-x: auto;
  margin: 20px 0;
  font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace;
  font-size: 14px;
}

#app.dark-theme .article-content :deep(pre) {
  background-color: var(--card-bg);
  color: var(--text-color);
}

.article-content :deep(blockquote) {
  border-left: 4px solid #3498db;
  padding: 10px 20px;
  margin: 20px 0;
  background-color: #f8f9fa;
  color: #7f8c8d;
  border-radius: 0 4px 4px 0;
}

#app.dark-theme .article-content :deep(blockquote) {
  border-left: 4px solid var(--link-color);
  background-color: var(--card-bg);
  color: var(--text-color);
}

.article-content :deep(img) {
  max-width: 100%;
  height: auto;
  border-radius: 8px;
  margin: 20px 0;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.article-content :deep(table) {
  width: 100%;
  border-collapse: collapse;
  margin: 20px 0;
}

#app.dark-theme .article-content :deep(table) {
  border-color: var(--border-color);
}

.article-content :deep(th), .article-content :deep(td) {
  border: 1px solid #ddd;
  padding: 12px;
  text-align: left;
}

#app.dark-theme .article-content :deep(th), 
#app.dark-theme .article-content :deep(td) {
  border: 1px solid var(--border-color);
}

.article-content :deep(th) {
  background-color: #f8f9fa;
  font-weight: 600;
}

#app.dark-theme .article-content :deep(th) {
  background-color: var(--card-bg);
  font-weight: 600;
}

.article-content :deep(tr:nth-child(even)) {
  background-color: #f8f9fa;
}

#app.dark-theme .article-content :deep(tr:nth-child(even)) {
  background-color: var(--card-bg);
}

/* 点赞按钮 */
.article-actions {
  margin-top: 40px;
  padding-top: 20px;
  border-top: 1px solid #eee;
  text-align: center;
}

#app.dark-theme .article-actions {
  border-top: 1px solid var(--border-color);
}

.like-button {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 12px 24px;
  background: #3498db;
  color: white;
  border: none;
  border-radius: 30px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 16px;
  font-weight: 500;
  box-shadow: 0 4px 6px rgba(52, 152, 219, 0.2);
}

#app.dark-theme .like-button {
  background: var(--link-color);
  color: var(--card-bg);
}

.like-button:hover:not(:disabled) {
  background: #2980b9;
  transform: translateY(-2px);
  box-shadow: 0 6px 8px rgba(52, 152, 219, 0.3);
}

#app.dark-theme .like-button:hover:not(:disabled) {
  background: #6fae98;
  box-shadow: 0 6px 8px rgba(111, 174, 152, 0.3);
}

.like-button:disabled {
  background: #bdc3c7;
  cursor: not-allowed;
}

#app.dark-theme .like-button:disabled {
  background: #3a4a42;
  cursor: not-allowed;
}

.like-button.liked {
  background: #e74c3c;
}

#app.dark-theme .like-button.liked {
  background: #e74c3c;
}

.like-button.liked:hover:not(:disabled) {
  background: #c0392b;
  box-shadow: 0 6px 8px rgba(231, 76, 60, 0.3);
}

#app.dark-theme .like-button.liked:hover:not(:disabled) {
  background: #c0392b;
  box-shadow: 0 6px 8px rgba(231, 76, 60, 0.3);
}

.like-button .heart {
  font-size: 18px;
  transition: transform 0.3s ease;
}

.like-button:hover:not(:disabled) .heart {
  transform: scale(1.2);
}

.like-button .count {
  font-size: 14px;
  background: rgba(255, 255, 255, 0.2);
  padding: 2px 8px;
  border-radius: 10px;
}

/* 加载状态 */
.loading-state {
  text-align: center;
  padding: 60px 20px;
  background: rgba(255, 255, 255, 0.3);
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  border: 1px solid #eef2f7;
}

#app.dark-theme .loading-state {
  background: rgba(40, 51, 46, 0.3);
  border: 1px solid var(--border-color);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #3498db;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 20px;
}

#app.dark-theme .spinner {
  border: 4px solid var(--card-bg);
  border-top: 4px solid var(--link-color);
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* 错误状态 */
.error-state {
  text-align: center;
  padding: 60px 20px;
  background: rgba(255, 255, 255, 0.3);
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  border: 1px solid #eef2f7;
}

#app.dark-theme .error-state {
  background: rgba(40, 51, 46, 0.3);
  border: 1px solid var(--border-color);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.error-icon {
  font-size: 48px;
  margin-bottom: 20px;
}

.retry-button {
  padding: 12px 24px;
  background: #3498db;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background 0.3s;
  font-size: 16px;
  margin-top: 20px;
}

.retry-button:hover {
  background: #2980b9;
}

/* 响应式设计 */
@media (max-width: 1024px) {
  .blog-detail-container {
    padding: 15px;
    gap: 20px;
  }
  
  .toc-sidebar {
    width: 200px;
    left: calc(50% - 512px + 15px);
    max-height: calc(100vh - 120px);
    padding: 15px;
  }
  
  .toc-sidebar.fixed {
    left: calc(50% - 512px + 15px);
  }
  
  .main-content {
    max-width: calc(100% - 220px);
    margin-left: 220px;
  }
  
  .blog-article {
    padding: 30px;
  }
  
  .article-title {
    font-size: 28px;
  }
}

@media (max-width: 768px) {
  .blog-detail-container {
    flex-direction: column;
    padding: 10px;
  }
  
  .toc-sidebar {
    position: relative;
    width: 100%;
    left: 0;
    top: 0;
    max-height: none;
    margin-bottom: 30px;
    padding: 20px;
  }
  
  .toc-sidebar.fixed {
    position: relative;
    top: 0;
    left: 0;
  }
  
  .main-content {
    max-width: 100%;
    margin-left: 0;
  }
  
  .blog-article {
    padding: 20px;
  }
  
  .article-title {
    font-size: 24px;
  }
  
  .article-meta {
    flex-direction: column;
    gap: 10px;
  }
  
  .article-content {
    font-size: 15px;
  }
  
  .article-content :deep(h1) {
    font-size: 24px;
  }
  
  .article-content :deep(h2) {
    font-size: 20px;
  }
  
  .article-content :deep(h3) {
    font-size: 18px;
  }
  
  .article-content :deep(h4) {
    font-size: 16px;
  }
}

</style>

