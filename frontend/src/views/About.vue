<template>
  <div class="about">
    <h1>关于这个项目</h1>
    
    <div class="content">
      <section>
        <h2>技术栈</h2>
        <ul>
          <li><strong>前端:</strong> Vue.js 3 + Vite + Pinia</li>
          <li><strong>后端:</strong> Django + Django REST Framework</li>
          <li><strong>部署:</strong> Vercel (前端) + Render (后端)</li>
          <li><strong>数据库:</strong> PostgreSQL</li>
        </ul>
      </section>
      
      <section>
        <h2>项目特色</h2>
        <ul>
          <li>前后端分离架构</li>
          <li>响应式设计</li>
          <li>现代化开发工具链</li>
          <li>自动化部署</li>
          <li>AI 辅助开发</li>
        </ul>
      </section>
      
      <section>
        <h2>开发计划</h2>
        <ul>
          <li>用户认证系统</li>
          <li>文章管理功能</li>
          <li>评论系统</li>
          <li>搜索功能</li>
          <li>标签分类</li>
        </ul>
      </section>
    </div>
  </div>
</template>

<script setup>
// 这里可以添加组件逻辑
</script>

<style scoped>
.about {
  max-width: 800px;
  margin: 0 auto;
  text-align: left;
}

.about h1 {
  text-align: center;
  color: #2c3e50;
  margin-bottom: 2rem;
}

.content section {
  margin-bottom: 2rem;
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.content h2 {
  color: #2c3e50;
  margin-bottom: 1rem;
  border-bottom: 2px solid #3498db;
  padding-bottom: 0.5rem;
}

.content ul {
  list-style: none;
  padding: 0;
}

.content li {
  padding: 0.5rem 0;
  border-bottom: 1px solid #ecf0f1;
}

.content li:last-child {
  border-bottom: none;
}

.content strong {
  color: #2c3e50;
}
</style>
