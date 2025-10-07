<template>
  <div id="app">
    <nav class="navbar">
      
    <div class="nav-container">
      <router-link to="/" class="nav-logo">xx实验室</router-link>
      <div class="nav-menu">
        <router-link to="/home" class="nav-link">首页</router-link>
        <router-link to="/blog" class="nav-link">博客</router-link>
        <router-link to="/post/1" class="nav-link">Post</router-link>
        <router-link to="/about" class="nav-link">关于</router-link>
        <form class="nav-search" @submit.prevent>
          <input type="text" placeholder="搜索..." v-model="searchQuery" class="search-input" />
        </form>
        <button class="theme-toggle" @click="toggleTheme">
          <span v-if="isDark">🌙</span>
          <span v-else>☀️</span>
        </button>
      </div>
    </div>
    </nav>
    
    <main class="main-content">
      <router-view />
    </main>
    
    <footer class="footer">
      <p>&copy; 2025 我的博客. 由 AI 生成的项目结构.</p>
    </footer>
  </div>
</template>

<script setup>
// 这里可以添加全局逻辑
</script>

<style scoped>
.navbar {
  background: #2c3e50;
  color: white;
  padding: 1rem 0;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.nav-container {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 2rem;
}

.nav-logo {
  font-size: 1.5rem;
  font-weight: bold;
  color: white;
  text-decoration: none;
}

.nav-menu {
  display: flex;
  gap: 2rem;
}

.nav-link {
  color: white;
  text-decoration: none;
  transition: color 0.3s;
}

.nav-link:hover,
.nav-link.router-link-active {
  color: #3498db;
}

.main-content {
  min-height: calc(100vh - 200px);
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.footer {
  background: #34495e;
  color: white;
  text-align: center;
  padding: 2rem;
  margin-top: auto;
}
</style>
