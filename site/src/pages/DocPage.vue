<script setup lang="ts">
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { type Page, resolveMarkdownLink, resultOf } from '../content'
import MetricsTable from '../components/MetricsTable.vue'

const props = defineProps<{ page: Page }>()
const router = useRouter()

const result = computed(() => (props.page.section === 'experiments' ? resultOf(props.page) : undefined))
const meta = computed(() =>
  Object.entries(props.page.frontmatter).filter(([k]) => k !== 'title'),
)
const repoPath = computed(() => props.page.source)

/** Markdown 内の相対 .md リンクを SPA 遷移に置き換える */
function onClick(e: MouseEvent) {
  const a = (e.target as HTMLElement).closest('a')
  if (!a || e.metaKey || e.ctrlKey || a.target === '_blank') return
  const href = a.getAttribute('href')
  if (!href) return
  const to = resolveMarkdownLink(props.page.source, href)
  if (to) {
    e.preventDefault()
    router.push(to)
  }
}
</script>

<template>
  <article>
    <dl v-if="meta.length" class="meta">
      <template v-for="[k, v] in meta" :key="k">
        <dt>{{ k }}</dt>
        <dd>{{ v }}</dd>
      </template>
    </dl>
    <div @click="onClick">
      <component :is="page.component" />
    </div>
    <section v-if="result" class="results">
      <h2>results.json</h2>
      <MetricsTable :result="result" />
    </section>
    <p class="source"><code>{{ repoPath }}</code></p>
  </article>
</template>
