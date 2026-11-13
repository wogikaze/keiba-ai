<script setup lang="ts">
import { computed, ref } from 'vue'
import { type Page, pagesIn, titleOf } from '../content'

const props = defineProps<{ section: string; title: string }>()

const TOPIC_LABELS: Record<string, string> = {
  'market-efficiency': '市場の効率性・FLB',
  'probability-models': '着順の確率モデル',
  'machine-learning': '機械学習・深層学習',
  japan: '日本の競馬',
  'betting-strategy': '馬券戦略・資金管理',
  'evaluation-and-features': '評価方法・特徴量',
}
const IMPORTANCE_ORDER: Record<string, number> = { high: 0, medium: 1, low: 2 }

const query = ref('')
const onlyHigh = ref(false)
const withSource = ref(false)

const all = computed(() => pagesIn(props.section))
const filtered = computed(() => {
  const q = query.value.trim().toLowerCase()
  return all.value.filter((p) => {
    if (onlyHigh.value && p.frontmatter.importance !== 'high') return false
    if (withSource.value && !['downloaded', 'transcribed'].includes(p.frontmatter.source)) return false
    if (!q) return true
    const fm = p.frontmatter
    return [fm.title, fm.authors, fm.tags, fm.venue, String(fm.year ?? '')]
      .some((v) => v && String(v).toLowerCase().includes(q))
  })
})

const groups = computed(() => {
  const map = new Map<string, Page[]>()
  for (const p of filtered.value) {
    const t = p.frontmatter.topic || 'other'
    if (!map.has(t)) map.set(t, [])
    map.get(t)!.push(p)
  }
  for (const list of map.values()) {
    list.sort((a, b) =>
      (IMPORTANCE_ORDER[a.frontmatter.importance] ?? 9) - (IMPORTANCE_ORDER[b.frontmatter.importance] ?? 9)
      || Number(a.frontmatter.year ?? 0) - Number(b.frontmatter.year ?? 0))
  }
  const order = Object.keys(TOPIC_LABELS)
  return [...map.entries()].sort(
    ([a], [b]) => ((order.indexOf(a) + 1) || 99) - ((order.indexOf(b) + 1) || 99),
  )
})
const grouped = computed(() => all.value.some((p) => p.frontmatter.topic))
</script>

<template>
  <h1>{{ title }}</h1>
  <p v-if="!all.length">まだありません。</p>
  <template v-else>
    <div class="filters">
      <input v-model="query" type="search" placeholder="タイトル・著者・タグで絞り込み" />
      <label v-if="grouped"><input v-model="onlyHigh" type="checkbox" /> 必読のみ</label>
      <label v-if="grouped"><input v-model="withSource" type="checkbox" /> 原本を読んだもの</label>
      <span class="sub">{{ filtered.length }} / {{ all.length }} 件</span>
    </div>
    <section v-for="[topic, items] in groups" :key="topic">
      <h2 v-if="grouped">{{ TOPIC_LABELS[topic] ?? topic }} <small>({{ items.length }})</small></h2>
      <ul class="cards">
        <li v-for="p in items" :key="p.path">
          <span v-if="p.frontmatter.importance === 'high'" class="badge">必読</span>
          <span v-if="p.frontmatter.source === 'unavailable'" class="badge muted" title="原本未取得">要旨のみ</span>
          <RouterLink :to="p.path">{{ titleOf(p) }}</RouterLink>
          <span class="sub">
            {{ [p.frontmatter.authors, p.frontmatter.year ?? p.frontmatter.date, p.frontmatter.venue, p.frontmatter.status]
              .filter(Boolean).join(' · ') }}
          </span>
          <span v-if="p.frontmatter.tags" class="tags">{{ p.frontmatter.tags }}</span>
        </li>
      </ul>
    </section>
  </template>
</template>
