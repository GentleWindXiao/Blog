<template>
  <li :class="'toc-level-' + item.level">
    <div
      class="toc-link"
      :class="{ active: item.id === currentId }"
      @click="handleClick"
    >
      {{ item.content }}
    </div>

    <!-- 递归渲染子项 - 优化条件判断 -->
    <ul v-show="isExpanded" v-if="item.children && item.children.length > 0">
      <toc-item
        v-for="(child, idx) in item.children"
        :key="child.id || idx"
        :item="child"
        :current-id="currentId"
        :expanded-ids="expandedIds"
        @scroll-to="$emit('scroll-to', $event)"
      />
    </ul>
  </li>
</template>

<script setup>
import { ref, watch, computed } from 'vue'

const props = defineProps({
  item: { type: Object, required: true },
  currentId: String,
  expandedIds: { type: Object } // Set
})
const emit = defineEmits(['scroll-to'])

// 使用计算属性确保响应式更新
const isExpanded = computed(() => {
  // 检查当前标题是否应该展开
  if (props.expandedIds && props.expandedIds.has) {
    return props.expandedIds.has(props.item.id)
  }
  // 默认展开所有标题
  return true
})

const handleClick = () => {
  // 点击标题时触发滚动
  emit('scroll-to', props.item.id)
}
</script>


<style scoped>
.toc-link {
  cursor: pointer;
  padding: 8px 12px;
  border-radius: 6px;
  margin: 4px 0;
  transition: all 0.3s ease;
  display: block;
  text-decoration: none;
  color: #34495e;
  font-weight: 400;
  border: 1px solid transparent;
}

#app.dark-theme .toc-link {
  color: var(--text-color);
}

/* 当前阅读段落高亮 */
.toc-link.active {
  background-color: #3498db;
  color: white;
  font-weight: 500;
  border-color: #3498db;
  box-shadow: 0 2px 4px rgba(52, 152, 219, 0.2);
}

#app.dark-theme .toc-link.active {
  background-color: var(--link-color);
  color: var(--card-bg);
  border-color: var(--link-color);
  box-shadow: 0 2px 4px rgba(111, 174, 152, 0.2);
}

/* 不同层级字体大小和缩进 */
.toc-level-1 > .toc-link {
  font-size: 15px;
  font-weight: 600;
  padding-left: 10px;
}
.toc-level-2 > .toc-link {
  font-size: 14px;
  padding-left: 25px;
}
.toc-level-3 > .toc-link {
  font-size: 13px;
  padding-left: 40px;
}
.toc-level-4 > .toc-link {
  font-size: 12px;
  padding-left: 55px;
}
.toc-level-5 > .toc-link {
  font-size: 11px;
  padding-left: 70px;
}
.toc-level-6 > .toc-link {
  font-size: 10px;
  padding-left: 85px;
}

/* 悬停效果 */
.toc-link:hover {
  background-color: #f8f9fa;
  color: #3498db;
  border-color: #eef2f7;
}

#app.dark-theme .toc-link:hover {
  background-color: var(--card-bg);
  color: var(--link-color);
  border-color: var(--border-color);
}

.toc-link.active:hover {
  background-color: #2980b9;
  border-color: #2980b9;
}

#app.dark-theme .toc-link.active:hover {
  background-color: #6fae98;
  border-color: #6fae98;
}
</style>
