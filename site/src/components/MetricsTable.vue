<script setup lang="ts">
import type { ExperimentResult } from '../content'

defineProps<{ result: ExperimentResult }>()
const fmt = (v: unknown) => (typeof v === 'number' && !Number.isInteger(v) ? v.toFixed(4) : (v ?? '-'))
</script>

<template>
  <table>
    <tbody>
      <tr><th>status</th><td>{{ fmt(result.status) }}</td></tr>
      <tr v-for="(v, k) in result.metrics" :key="k"><th>{{ k }}</th><td>{{ fmt(v) }}</td></tr>
      <tr><th>split</th><td>{{ fmt(result.split) }}</td></tr>
      <tr><th>data_version</th><td>{{ fmt(result.data_version) }}</td></tr>
      <tr><th>seed</th><td>{{ fmt(result.seed) }}</td></tr>
      <tr><th>git_hash</th><td><code>{{ fmt(result.git_hash) }}</code></td></tr>
    </tbody>
  </table>
</template>
