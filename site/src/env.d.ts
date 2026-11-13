/// <reference types="vite/client" />
declare module '*.md' {
  import type { Component } from 'vue'
  export const frontmatter: Record<string, string>
  const component: Component
  export default component
}
declare module '*.vue' {
  import type { Component } from 'vue'
  const component: Component
  export default component
}
