<template>
  <div class="toc-sidebar" v-if="headings && headings.length">
    <h3>目录</h3>
    <ul>
      <toc-item
        v-for="(item, index) in headings"
        :key="index"
        :item="item"
        :current-id="currentId"
        :expanded-ids="expandedIds"
        @scroll-to="$emit('scroll-to', $event)"
      />
    </ul>
  </div>
  <div class="toc-sidebar" v-else>
    <h3>目录</h3>
    <p>暂无目录</p>
  </div>
</template>

<script setup>
import { defineProps } from 'vue'
import TocItem from './TocItem.vue'

const props = defineProps({
  headings: { type: Array, default: () => [] },
  currentId: String,
  expandedIds: { type: Object } // Set
})

</script>

<style scoped>
.toc-sidebar {
  position: sticky;
  top: 80px;
  width: 250px;
  max-height: calc(100vh - 80px);
  overflow-y: auto;
  border-left: 1px solid #eef2f7;
  padding-left: 15px;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  padding: 20px;
}

#app.dark-theme .toc-sidebar {
  border-left: 1px solid var(--border-color);
  background: var(--card-bg);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}

.toc-sidebar h3 {
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 15px;
  color: #2c3e50;
  padding-bottom: 10px;
  border-bottom: 1px solid #eee;
}

#app.dark-theme .toc-sidebar h3 {
  color: var(--text-color);
  border-bottom: 1px solid var(--border-color);
}

.toc-sidebar ul {
  list-style: none;
  padding-left: 0;
  margin: 0;
}

.toc-sidebar .toc-empty {
  color: #95a5a6;
  font-style: italic;
  text-align: center;
  padding: 20px 0;
}

#app.dark-theme .toc-sidebar .toc-empty {
  color: var(--meta-color);
}
</style>
