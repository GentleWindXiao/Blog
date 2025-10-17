<template>
  <div class="blog-container">
    <div v-if="isLoading" class="loading">加载中...</div>
    <div v-else-if="hasError" class="error">{{ error }}</div>
    <div v-else>
      <BlogList :blogs="blogs"/>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue';
import { storeToRefs } from 'pinia';
import { useBlogStore } from '@/stores/Blog/blogstore';
import BlogList from '@/components/Blog/BlogList.vue';

// 使用Pinia状态管理
const blogStore = useBlogStore();

// 从store中获取响应式状态
const { getBlogs: blogs, isLoading, hasError, error } = storeToRefs(blogStore);

// 组件挂载时获取博客列表
onMounted(() => {
  blogStore.fetchAllBlogs();
});
</script>

<style scoped>
.loading, .error {
  text-align: center;
  padding: 20px;
  font-size: 18px;
}

.error {
  color: red;
}

/* 为固定导航栏留出空间 */
/* .blog-container {
  padding-top: 80px;
} */
</style>