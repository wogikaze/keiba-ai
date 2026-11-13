import type { Component } from 'vue'

/**
 * リポジトリ直下の docs/ と experiments/ を集めて、ルートとメタデータを作る。
 *
 * docs/index.md                       -> /
 * docs/literature/foo.md              -> /literature/foo
 * experiments/<name>/README.md        -> /experiments/<name>
 */

interface MdModule {
  default: Component
  frontmatter: Record<string, string>
}

// 研究ノートは小さいので全部まとめてバンドルする（frontmatter を一覧で使うため）
const mdModules = import.meta.glob<MdModule>(
  ['../../docs/**/*.md', '../../experiments/*/README.md', '!../../**/_template.md', '!../../**/_template/**'],
  { eager: true },
)
const results = import.meta.glob<ExperimentResult>(
  ['../../experiments/*/results.json', '!../../**/_template/**'],
  { import: 'default', eager: true },
)

export interface ExperimentResult {
  experiment?: string
  status?: string
  git_hash?: string | null
  data_version?: string | null
  seed?: number | null
  split?: string | null
  metrics?: Record<string, number>
}

export interface Page {
  /** ルートのパス */
  path: string
  /** リポジトリルートからの相対パス（docs/... / experiments/...） */
  source: string
  /** docs 直下のセクション名（literature, adr, experiments, ...） */
  section: string
  frontmatter: Record<string, string>
  component: Component
}

const norm = (key: string) => key.replace(/^(\.\.\/)+/, '')

function toRoute(rel: string): string {
  if (rel === 'docs/index.md') return '/'
  const exp = rel.match(/^experiments\/([^/]+)\/README\.md$/)
  if (exp) return `/experiments/${exp[1]}`
  return '/' + rel.replace(/^docs\//, '').replace(/(\/index)?\.md$/, '')
}

function sectionOf(path: string): string {
  return path.split('/')[1] ?? ''
}

export const pages: Page[] = Object.entries(mdModules).map(([key, mod]) => {
  const source = norm(key)
  const path = toRoute(source)
  return { path, source, section: sectionOf(path), frontmatter: mod.frontmatter ?? {}, component: mod.default }
})

const bySource = new Map(pages.map((p) => [p.source, p]))

export function pagesIn(section: string): Page[] {
  return pages
    .filter((p) => p.section === section && p.path !== `/${section}`)
    .sort((a, b) => b.path.localeCompare(a.path))
}

export function resultOf(page: Page): ExperimentResult | undefined {
  return results['../../' + page.source.replace(/README\.md$/, 'results.json')]
}

export function titleOf(page: Page): string {
  return page.frontmatter.title || page.path.split('/').pop() || page.path
}

/** Markdown 内の相対リンク（./foo.md など）をサイトのルートに解決する */
export function resolveMarkdownLink(fromSource: string, href: string): string | undefined {
  if (/^[a-z]+:/i.test(href) || href.startsWith('#') || href.startsWith('//')) return undefined
  // /literature のようなサイト内の絶対パスは base を付けて router で遷移させる
  if (href.startsWith('/') && !href.endsWith('.md')) return href
  const [pathPart, hash = ''] = href.split('#')
  if (!pathPart.endsWith('.md')) return undefined
  const target = new URL(pathPart, new URL(fromSource, 'https://x/')).pathname.slice(1)
  const page = bySource.get(decodeURIComponent(target))
  return page ? page.path + (hash ? `#${hash}` : '') : undefined
}
