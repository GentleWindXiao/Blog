<template>
  <div class="blog-list">
    <!-- <h1 class="title">博客列表</h1> -->
    <div v-if="blogs && blogs.length > 0" class="blogs-container">
      <div v-for="blog in blogs" :key="blog.id" class="blog-card" @click="viewBlog(blog.slug)">
        <h2 class="blog-title">{{ blog.title }}</h2>
        <div class="blog-meta">
          <span class="blog-author">作者: {{ blog.author }}</span>
          <span class="blog-date">发布于: {{ formatDate(blog.created_at) }}</span>
        </div>
        <p class="blog-excerpt">{{ blog.excerpt || '暂无摘要' }}</p>
        <div class="blog-stats">
          <span class="blog-views"><i class="icon-eye"></i> {{ blog.views_count }} 阅读</span>
          <span class="blog-likes"><i class="icon-heart"></i> {{ blog.likes_count }} 喜欢</span>
        </div>
      </div>
    </div>
    <div v-else class="no-blogs">
      <p>暂无博客内容</p>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router';
import { defineProps } from 'vue';

const props = defineProps({
  blogs: {
    type: Array,
    default: () => []
  }
});

const router = useRouter();

// 格式化日期
const formatDate = (dateString) => {
  const date = new Date(dateString);
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  });
};

// 查看博客详情
const viewBlog = (slug) => {
  router.push({ name: 'BlogDetail', params: { slug } });
};
</script>

<style scoped>
.blog-list {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
}

.title {
  text-align: center;
  margin-bottom: 30px;
  color: #333;
  font-size: 2rem;
}

#app.dark-theme .title {
  color: var(--text-color);
}

.blogs-container {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.blog-card {
  background-color: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  padding: 18px;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  cursor: pointer;
  max-width: 100%;
}

#app.dark-theme .blog-card {
  background-color: var(--card-bg);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
  border: 1px solid var(--border-color);
}

.blog-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
}

#app.dark-theme .blog-card:hover {
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
}

.blog-title {
  margin-top: 0;
  margin-bottom: 8px;
  color: #333;
  font-size: 1.3rem;
  line-height: 1.2;
}

#app.dark-theme .blog-title {
  color: var(--text-color);
}

.blog-meta {
  display: flex;
  justify-content: space-between;
  margin-bottom: 15px;
  font-size: 0.85rem;
  color: #666;
}

#app.dark-theme .blog-meta {
  color: var(--meta-color);
}

.blog-excerpt {
  color: #555;
  margin-bottom: 15px;
  line-height: 1.5;
  font-size: 0.9rem;
}

#app.dark-theme .blog-excerpt {
  color: var(--text-color);
}

.blog-stats {
  display: flex;
  justify-content: space-between;
  color: #888;
  font-size: 0.9rem;
}

#app.dark-theme .blog-stats {
  color: var(--meta-color);
}

.blog-views, .blog-likes {
  display: flex;
  align-items: center;
}

.icon-eye, .icon-heart {
  margin-right: 5px;
}

.no-blogs {
  text-align: center;
  padding: 50px;
  color: #666;
  font-size: 1.2rem;
}

#app.dark-theme .no-blogs {
  color: var(--text-color);
}
</style>