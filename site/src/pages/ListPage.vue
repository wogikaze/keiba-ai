<script setup lang="ts">
import { computed } from 'vue'
import { pagesIn, titleOf } from '../content'

const props = defineProps<{ section: string; title: string }>()
const items = computed(() => pagesIn(props.section))
</script>

<template>
  <h1>{{ title }}</h1>
  <p v-if="!items.length">まだありません。</p>
  <ul class="cards">
    <li v-for="p in items" :key="p.path">
      <RouterLink :to="p.path">{{ titleOf(p) }}</RouterLink>
      <span class="sub">
        {{ [p.frontmatter.authors, p.frontmatter.year ?? p.frontmatter.date, p.frontmatter.status]
          .filter(Boolean).join(' · ') }}
      </span>
      <span v-if="p.frontmatter.tags" class="tags">{{ p.frontmatter.tags }}</span>
    </li>
  </ul>
</template>
