<template>
  <div class="home-page">
    <!-- Hero 区 -->
    <Hero />
    
    <!-- 主要内容区域 -->
    <main class="main-content">
      <BlogModule />
    </main>
  </div>
</template>

<script setup>
import Hero from '@/components/Home/Hero.vue'
import BlogModule from '@/components/Blog/BlogModule.vue'
</script>


<style scoped>
.home-page {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.main-content {
  flex: 1;
  background: transparent;
}


</style>