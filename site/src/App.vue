<script setup lang="ts">
const nav = [
  { to: '/literature', label: '先行研究' },
  { to: '/ideas', label: 'アイデア' },
  { to: '/data', label: 'データ' },
  { to: '/adr', label: 'ADR' },
  { to: '/experiments', label: '実験' },
]
</script>

<template>
  <header class="header">
    <RouterLink to="/" class="brand">keiba-ai</RouterLink>
    <nav>
      <RouterLink v-for="n in nav" :key="n.to" :to="n.to">{{ n.label }}</RouterLink>
    </nav>
  </header>
  <main class="main">
    <RouterView :key="$route.path" />
  </main>
</template>
