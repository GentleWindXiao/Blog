<template>
  <div class="home-page">
    <!-- Hero 区 -->
    <Hero />

    <!-- 模块容器 -->
    <div class="module-container">
      <!-- Blog 模块 -->
      <BlogModule />

    </div>
  </div>
</template>

<script setup>
import Hero from '@/components/Home/Hero.vue'
import BlogModule from '@/components/Home/BlogModule.vue'

</script>


<style scoped>
.home-page {
  display: flex;
  flex-direction: column;
}

/* 区域间距（区分 Hero 与模块容器） */
.module-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem 1.5rem 3rem;
}

/* 模块区通用布局，可承载多个模块 */
.module-container :deep(.section) {
  margin-top: 2rem;
}

@media (max-width: 768px) {
  .module-container {
    padding: 1.25rem 1rem 2rem;
  }
}
</style>