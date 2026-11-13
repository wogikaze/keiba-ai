<script setup lang="ts">
import { computed, ref } from 'vue'
import { pagesIn, resultOf, titleOf } from '../content'

const rows = computed(() =>
  pagesIn('experiments').map((p) => ({ page: p, title: titleOf(p), r: resultOf(p) ?? {} })),
)
const metricKeys = computed(() => [...new Set(rows.value.flatMap((x) => Object.keys(x.r.metrics ?? {})))].sort())

const sortKey = ref<string | null>(null)
const desc = ref(false)
function sortBy(k: string) {
  if (sortKey.value === k) desc.value = !desc.value
  else { sortKey.value = k; desc.value = false }
}
const sorted = computed(() => {
  const k = sortKey.value
  if (!k) return rows.value
  return [...rows.value].sort((a, b) => {
    const va = a.r.metrics?.[k], vb = b.r.metrics?.[k]
    if (va == null) return 1
    if (vb == null) return -1
    return desc.value ? vb - va : va - vb
  })
})
const fmt = (v: unknown) => (typeof v === 'number' && !Number.isInteger(v) ? v.toFixed(4) : (v ?? '-'))
</script>

<template>
  <h1>実験リーダーボード</h1>
  <p class="sub">指標の列見出しをクリックで並べ替え。元データは各実験の <code>results.json</code>。</p>
  <div class="table-wrap">
    <table>
      <thead>
        <tr>
          <th>experiment</th><th>status</th>
          <th v-for="k in metricKeys" :key="k" class="sortable" @click="sortBy(k)">
            {{ k }}<span v-if="sortKey === k">{{ desc ? ' ▼' : ' ▲' }}</span>
          </th>
          <th>split</th><th>data</th><th>seed</th><th>git</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="x in sorted" :key="x.page.path">
          <td><RouterLink :to="x.page.path">{{ x.title }}</RouterLink><br /><small>{{ x.page.path.split('/').pop() }}</small></td>
          <td>{{ fmt(x.r.status) }}</td>
          <td v-for="k in metricKeys" :key="k" class="num">{{ fmt(x.r.metrics?.[k]) }}</td>
          <td>{{ fmt(x.r.split) }}</td>
          <td>{{ fmt(x.r.data_version) }}</td>
          <td>{{ fmt(x.r.seed) }}</td>
          <td><code>{{ x.r.git_hash?.slice(0, 7) ?? '-' }}</code></td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
