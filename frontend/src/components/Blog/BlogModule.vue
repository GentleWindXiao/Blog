<template>
    <section class="blog-module">
      <h2>最新博客</h2>
      <div class="blog-list">
        <div class="blog-card" v-for="post in posts" :key="post.id">
          <h3>{{ post.title }}</h3>
          <p>{{ post.summary }}</p>
        </div>
      </div>
    </section>
  </template>
  
  <script setup>
  const posts = [
    { id: 1, title: '博客标题1', summary: '摘要1' },
    { id: 2, title: '博客标题2', summary: '摘要2' },
    { id: 3, title: '博客标题3', summary: '摘要3' }
  ]
  </script>
  
  <style scoped>
.blog-module {
  max-width: 1200px;
  margin: 0 auto;
}

.blog-module h2 {
  font-size: 24px;
  color: #111827;
  margin: 24px 0 16px;
}

.blog-list {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
}

.blog-card {
  background: #ffffff;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 16px;
  box-shadow: 0 1px 2px rgba(0,0,0,0.04);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.blog-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 14px rgba(0,0,0,0.08);
}

.blog-card h3 {
  font-size: 18px;
  color: #111827;
  margin-bottom: 8px;
}

.blog-card p {
  color: #6b7280;
  font-size: 14px;
}

@media (max-width: 1024px) {
  .blog-list {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 640px) {
  .blog-list {
    grid-template-columns: 1fr;
  }
}
</style>
  