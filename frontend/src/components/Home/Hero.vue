<template>
    <section class="hero">
      <h1>欢迎来到我的Web</h1>
      <p>这里是实验室、笔记、学习分享的汇总</p>
    </section>
</template>
<style scoped>
.hero {
  width: 100%;
  background: linear-gradient(135deg, #1f2937 0%, #0f172a 100%);
  color: #fff;
  padding: 72px 16px; /* 上下更大留白，明确与模块区分 */
  text-align: center;
}

.hero h1 {
  font-size: 40px;
  line-height: 1.2;
  font-weight: 700;
  letter-spacing: 0.5px;
  margin-bottom: 12px;
}

.hero p {
  font-size: 16px;
  opacity: 0.9;
}

@media (max-width: 768px) {
  .hero {
    padding: 56px 14px;
  }
  .hero h1 {
    font-size: 30px;
  }
}
</style>
  