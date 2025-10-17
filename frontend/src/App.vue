<template>
  <div id="app" :class="{ 'dark-theme': isDarkMode }">
    <!-- 导航栏 -->
    <nav class="navbar" :class="{ 'dark-theme': isDarkMode, 'hidden': isNavbarHidden }">
      <div class="nav-container">
        <div class="nav-logo" @click="$router.push('/')">
          云xuan阁
        </div>
        <div class="menu-toggle" @click="toggleMobileMenu">
          ☰
        </div>
        <div class="nav-menu" :class="{ 'mobile-menu-open': isMobileMenuOpen }">
          <router-link to="/home" class="nav-link" @click="isMobileMenuOpen = false">主页</router-link>
          <router-link to="/blog" class="nav-link" @click="isMobileMenuOpen = false">博客</router-link>
          <router-link to="/note" class="nav-link" @click="isMobileMenuOpen = false">笔记</router-link>
          <router-link to="/about" class="nav-link" @click="isMobileMenuOpen = false">关于</router-link>
          <div class="nav-controls">
            <div class="nav-search">
              <span class="search-icon">🔍</span>
              <input 
                type="text" 
                v-model="searchQuery" 
                @keyup.enter="performSearch"
                placeholder="搜索..." 
                class="search-input"
              />
            </div>
            <button @click="toggleTheme" class="theme-toggle">
              {{ isDarkMode ? '☀️' : '🌙' }}
            </button>
          </div>
        </div>
      </div>
    </nav>

    <!-- 主内容区域 -->
    <main class="main-content">
      <router-view :is-dark-mode="isDarkMode"/>
    </main>

    <!-- 页脚 -->
    <footer class="footer">
      <div class="footer-content">
        <div class="footer-info">
          <div class="copyright">
            &copy; {{ new Date().getFullYear() }} 云xuan阁. All rights reserved.
          </div>
          <div class="footer-description">
            分享技术与生活，记录成长与思考
          </div>
        </div>
        <div class="social-links">
          <a href="#" target="_blank" rel="noopener noreferrer">GitHub</a>
          <a href="#" target="_blank" rel="noopener noreferrer">Twitter</a>
          <a href="#" target="_blank" rel="noopener noreferrer">LinkedIn</a>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import { useRouter } from 'vue-router'

const searchQuery = ref('')
const isDarkMode = ref(false)
const isMobileMenuOpen = ref(false)
const router = useRouter()

// 导航栏隐藏相关状态
const isNavbarHidden = ref(false)
const lastScrollTop = ref(0)

// 切换主题模式
const toggleTheme = () => {
  isDarkMode.value = !isDarkMode.value
  document.body.classList.toggle('dark-theme', isDarkMode.value)
  
  // 保存用户偏好到本地存储
  localStorage.setItem('theme', isDarkMode.value ? 'dark' : 'light')
}

// 切换移动端菜单
const toggleMobileMenu = () => {
  isMobileMenuOpen.value = !isMobileMenuOpen.value
}

// 执行搜索
const performSearch = () => {
  if (searchQuery.value.trim()) {
    // 导航到搜索结果页面
    router.push(`/search?q=${encodeURIComponent(searchQuery.value)}`)
    // 清空搜索框
    searchQuery.value = ''
    // 在移动端关闭菜单
    isMobileMenuOpen.value = false
  }
}

// 页脚链接处理方法
const goToHome = () => {
  router.push('/home')
  isMobileMenuOpen.value = false
}

const goToBlog = () => {
  router.push('/blog')
  isMobileMenuOpen.value = false
}

const goToAbout = () => {
  router.push('/about')
  isMobileMenuOpen.value = false
}

// 处理滚动事件，实现导航栏隐藏效果
const handleScroll = () => {
  const scrollTop = window.pageYOffset || document.documentElement.scrollTop
  
  // 向下滚动时隐藏导航栏，向上滚动时显示导航栏
  if (scrollTop > lastScrollTop.value && scrollTop > 50) {
    // 向下滚动
    isNavbarHidden.value = true
  } else {
    // 向上滚动
    isNavbarHidden.value = false
  }
  
  lastScrollTop.value = scrollTop
}

// 页面加载时检查保存的主题偏好
onMounted(() => {
  const savedTheme = localStorage.getItem('theme')
  if (savedTheme === 'dark') {
    isDarkMode.value = true
    document.body.classList.add('dark-theme')
  }
  
  // 添加滚动事件监听器
  window.addEventListener('scroll', handleScroll)
  
  // 监听窗口大小变化，自动关闭移动端菜单
  window.addEventListener('resize', () => {
    if (window.innerWidth > 768) {
      isMobileMenuOpen.value = false
    }
  })
})

// 组件卸载前清理事件监听器
onBeforeUnmount(() => {
  window.removeEventListener('scroll', handleScroll)
})
</script>

<style>
#app.dark-theme {
  color: var(--text-color);
  transition: color 0.3s ease;
}

.navbar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 100;
  background: linear-gradient(135deg, rgba(163, 196, 168, 0.4), rgba(143, 199, 179, 0.4)); /* 进一步降低透明度 */
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border-bottom: 1px solid rgba(217, 224, 210, 0.3);
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  padding: 1rem 3rem;
  display: flex;
  justify-content: center;
  color: var(--text-color);
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
  transition: transform 0.3s ease, background 0.3s ease, border-color 0.3s ease, box-shadow 0.3s ease; /* 添加过渡效果 */
}

.navbar.hidden {
  transform: translateY(-100%);
}

.navbar.dark-theme {
  background: linear-gradient(135deg, rgba(54, 70, 59, 0.4), rgba(43, 65, 59, 0.4)); /* 进一步降低透明度 */
  border-bottom: 1px solid rgba(100, 110, 100, 0.3);
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
  color: var(--text-color);
}

.nav-container {
  max-width: 1400px;
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.nav-logo {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--text-color);
  text-decoration: none;
  transition: transform 0.3s ease;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  cursor: pointer;
}

.nav-logo:hover {
  transform: scale(1.05);
}

.nav-menu {
  display: flex;
  align-items: center;
  gap: 2rem;
}

.menu-toggle {
  display: none;
  font-size: 1.5rem;
  cursor: pointer;
  padding: 0.5rem;
  border-radius: 5px;
  background: rgba(255, 255, 255, 0.2);
  color: var(--text-color);
  transition: all 0.3s ease;
  position: absolute;
  right: 1rem;
  top: 1rem;
}

.menu-toggle:hover {
  background: rgba(255, 255, 255, 0.3);
}

.nav-link {
  color: var(--text-color);
  text-decoration: none;
  font-weight: 500;
  padding: 0.5rem 0;
  transition: all 0.3s ease;
  position: relative;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}

.nav-link::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 0;
  height: 2px;
  background-color: var(--link-color); /* 使用CSS变量 */
  transition: width 0.3s ease;
}

.nav-link:hover,
.nav-link.router-link-active {
  color: var(--link-color); /* 使用CSS变量 */
  text-decoration: none;
  transform: none;
  background: none;
}

.nav-link:hover::after,
.nav-link.router-link-active::after {
  width: 100%;
}

/* 已移除按钮样式 */

.nav-controls {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.nav-search {
  position: relative;
}

.search-input {
  padding: 0.5rem 1rem 0.5rem 2rem;
  border-radius: 20px;
  border: none;
  background: rgba(255, 255, 255, 0.25);
  color: var(--text-color);
  outline: none;
  transition: all 0.3s ease;
  width: 200px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.search-input::placeholder {
  color: rgba(255, 255, 255, 0.8);
}

.search-input:focus {
  background: rgba(255, 255, 255, 0.35);
  width: 250px;
  box-shadow: 0 0 0 3px rgba(255, 255, 255, 0.2);
}

.search-input:focus::placeholder {
  color: transparent;
}

#app.dark-theme .search-input {
  background: rgba(255, 255, 255, 0.15);
  color: var(--text-color);
}

#app.dark-theme .search-input::placeholder {
  color: rgba(215, 215, 215, 0.7);
}

#app.dark-theme .search-input:focus {
  background: rgba(255, 255, 255, 0.25);
  box-shadow: 0 0 0 3px rgba(255, 255, 255, 0.1);
}

.theme-toggle {
  background: transparent;
  border: none;
  color: var(--text-color);
  font-size: 1.2rem;
  cursor: pointer;
  padding: 0.5rem;
  border-radius: 50%;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.2);
  width: 40px;
  height: 40px;
}

.theme-toggle:hover {
  background: rgba(255, 255, 255, 0.3);
  transform: rotate(15deg);
}

.main-content {
  min-height: calc(100vh - 200px);
  max-width: 1200px;
  margin: 2rem auto;
  padding: 0 2rem;
  flex: 1;
  padding-top: 100px; /* 为固定导航栏留出空间 */
  background: transparent;
}

.footer {
  background: linear-gradient(135deg, rgba(163, 196, 168, 0.85), rgba(143, 199, 179, 0.85)); /* 苔藓绿到湖水青渐变 */
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border-top: 1px solid rgba(217, 224, 210, 0.3); /* 浅竹灰边框 */
  box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.05); /* 柔和阴影 */
  padding: 1rem 2rem;
  color: var(--text-color);
  font-size: 0.9rem;
}

#app.dark-theme .footer {
  background: linear-gradient(135deg, rgba(54, 70, 59, 0.85), rgba(43, 65, 59, 0.85));
  border-top: 1px solid rgba(100, 110, 100, 0.3);
  box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.2);
}

.footer-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 1rem;
}

.footer-info {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.social-links {
  display: flex;
  gap: 1rem;
}

.social-links a {
  color: var(--text-color);
  text-decoration: none;
  transition: color 0.3s ease;
}

.social-links a:hover {
  color: var(--link-color);
  text-decoration: underline;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .menu-toggle {
    display: block;
  }
  
  .nav-container {
    flex-direction: row;
    gap: 1rem;
    padding: 1rem;
  }
  
  .nav-menu {
    position: absolute;
    top: 100%;
    left: 0;
    right: 0;
    background: linear-gradient(135deg, var(--card-bg), var(--card-bg-secondary));
    flex-direction: column;
    width: 100%;
    gap: 1rem;
    padding: 1rem;
    border-bottom-left-radius: 10px;
    border-bottom-right-radius: 10px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    opacity: 0;
    visibility: hidden;
    transform: translateY(-10px);
    transition: all 0.3s ease;
    z-index: 1000;
  }
  
  .nav-menu.mobile-menu-open {
    opacity: 1;
    visibility: visible;
    transform: translateY(0);
  }
  
  .nav-controls {
    justify-content: flex-start;
    width: 100%;
  }
  
  .search-input {
    width: 150px;
  }
  
  .search-input:focus {
    width: 180px;
  }
  
  .main-content {
    padding: 1rem;
    margin: 1rem auto;
    padding-top: 80px;
  }
  
  .footer-content {
    flex-direction: column;
    text-align: center;
    gap: 1rem;
  }
  
  .footer-links {
    justify-content: center;
  }
  
  #app.dark-theme .nav-menu {
    background: linear-gradient(135deg, var(--card-bg), var(--card-bg-secondary));
  }
}

@media (max-width: 480px) {
  .nav-logo {
    font-size: 1.5rem;
  }
  
  .nav-link {
    padding: 0.3rem 0.8rem;
    font-size: 0.9rem;
  }
  
  .search-input {
    width: 120px;
    padding: 0.4rem 0.8rem 0.4rem 1.5rem;
  }
  
  .search-input:focus {
    width: 140px;
  }
}
</style>
