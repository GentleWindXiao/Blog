<template>
    <section class="hero">
      <div class="hero-content">
        <h1 class="hero-title">云xuan阁</h1>
        <p class="hero-subtitle">记录学习点滴，分享知识与思考</p>
        <div class="hero-buttons">
          <router-link to="/blog" class="btn primary">浏览博客</router-link>
          <router-link to="/about" class="btn secondary">了解更多</router-link>
        </div>
      </div>
    </section>
</template>
<style scoped>
.hero {
  width: 100%;
  color: var(--text-color);
  padding: 100px 16px;
  text-align: center;
  position: relative;
  overflow: hidden;
}

/* 日间模式下的背景样式 - 早晨太阳升起的背景色 */
.hero {
  background: linear-gradient(135deg, rgba(255, 215, 135, 0.5) 0%, rgba(255, 185, 105, 0.5) 100%);
}

/* 夜间模式下的背景样式 - 星空紫 */
.dark-theme .hero {
  background: linear-gradient(135deg, rgba(65, 45, 115, 0.5) 0%, rgba(45, 25, 85, 0.5) 100%);
}

.btn.primary {
  background: var(--card-bg);
  color: #764ba2;
  box-shadow: 0 4px 15px var(--shadow-color);
}

.btn.secondary {
  background: transparent;
  color: var(--text-color);
  border-color: rgba(255,255,255,0.5);
}

.hero::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTAwJSIgaGVpZ2h0PSIxMDAlIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciPjxkZWZzPjxwYXR0ZXJuIGlkPSJwYXR0ZXJuIiB3aWR0aD0iNjAiIGhlaWdodD0iNjAiIHBhdHRlcm5Vbml0cz0idXNlclNwYWNlT25Vc2UiIHBhdHRlcm5UcmFuc2Zvcm09InJvdGF0ZSg0NSkiPjxjaXJjbGUgY3g9IjMwIiBjeT0iMzAiIHI9IjAuNSIgZmlsbD0iI2ZmZiIgZmlsbC1vcGFjaXR5PSIwLjEiLz48L3BhdHRlcm4+PC9kZWZzPjxyZWN0IHdpZHRoPSIxMDAlIiBoZWlnaHQ9IjEwMCUiIGZpbGw9InVybCgjcGF0dGVybikiLz48L3N2Zz4=') repeat;
  opacity: 0.2;
}

.hero-content {
  position: relative;
  max-width: 800px;
  margin: 0 auto;
}

.hero-title {
  font-size: 3.5rem;
  font-weight: 800;
  margin-bottom: 1rem;
  text-shadow: 0 2px 4px rgba(0,0,0,0.1);
  letter-spacing: 1px;
}

.hero-subtitle {
  font-size: 1.5rem;
  margin-bottom: 2.5rem;
  opacity: 0.9;
  font-weight: 300;
}

.hero-buttons {
  display: flex;
  justify-content: center;
  gap: 1rem;
  flex-wrap: wrap;
}

.btn {
  padding: 12px 30px;
  border-radius: 50px;
  text-decoration: none;
  font-weight: 600;
  transition: all 0.3s ease;
  border: 2px solid transparent;
  font-size: 1rem;
}

.btn.primary {
  background: #fff;
  color: #764ba2;
  box-shadow: 0 4px 15px rgba(0,0,0,0.2);
}

.btn.primary:hover {
  background: transparent;
  color: #fff;
  transform: translateY(-3px);
  box-shadow: 0 6px 20px rgba(0,0,0,0.3);
}

.btn.secondary {
  background: transparent;
  color: #fff;
  border-color: rgba(255,255,255,0.5);
}

.btn.secondary:hover {
  background: rgba(255,255,255,0.1);
  transform: translateY(-3px);
}

@media (max-width: 768px) {
  .hero {
    padding: 70px 16px;
  }
  
  .hero-title {
    font-size: 2.5rem;
  }
  
  .hero-subtitle {
    font-size: 1.2rem;
  }
  
  .hero-buttons {
    flex-direction: column;
    align-items: center;
  }
  
  .btn {
    width: 80%;
    max-width: 250px;
  }
}
</style>
  