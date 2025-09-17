<template>
  <div class="home">
    <div class="hero">
      <h1>欢迎来到我的博客</h1>
      <p>一个现代化的全栈博客系统</p>
    </div>
    
    <div class="features">
      <div class="feature-card">
        <h3>🚀 现代化技术栈</h3>
        <p>Vue.js + Django + Vercel + Render</p>
      </div>
      <div class="feature-card">
        <h3>📱 响应式设计</h3>
        <p>完美适配各种设备</p>
      </div>
      <div class="feature-card">
        <h3>⚡ 高性能</h3>
        <p>前后端分离，全球CDN加速</p>
      </div>
    </div>
  </div>
</template>

<script setup>
// 这里可以添加组件逻辑
</script>

<style scoped>
.home {
  text-align: center;
}

.hero {
  margin-bottom: 4rem;
}

.hero h1 {
  font-size: 3rem;
  color: #2c3e50;
  margin-bottom: 1rem;
}

.hero p {
  font-size: 1.2rem;
  color: #7f8c8d;
}

.features {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  margin-top: 3rem;
}

.feature-card {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s;
}

.feature-card:hover {
  transform: translateY(-5px);
}

.feature-card h3 {
  color: #2c3e50;
  margin-bottom: 1rem;
}

.feature-card p {
  color: #7f8c8d;
}
</style>
