import { fileURLToPath } from 'node:url'
import { defineConfig, type Plugin } from 'vite'
import vue from '@vitejs/plugin-vue'
import { oxContentVue } from '@ox-content/vite-plugin-vue'

const repoRoot = fileURLToPath(new URL('..', import.meta.url))

/**
 * Markdown は `\,` `\{` などの「バックスラッシュ + 記号」をエスケープとして解釈し、
 * バックスラッシュを消してしまう。数式（$...$ / $$...$$）の中だけバックスラッシュを二重にして、
 * Markdown を通った後に KaTeX（ブラウザ側）が元の LaTeX を受け取れるようにする。
 * コード（`...` と ```...```）の中は変えない。
 */
function protectMath(): Plugin {
  return {
    name: 'keiba-ai:protect-math',
    enforce: 'pre',
    transform(code, id) {
      if (!id.endsWith('.md')) return
      const body = code.replace(/```[\s\S]*?```|`[^`\n]*`|\$\$[\s\S]*?\$\$|\$[^$\n]+?\$/g, (m) =>
        m.startsWith('`')
          ? m
          : m
              .replace(/\\([!-\/:-@\[-`{-~])/g, '\\\\$1')
              // _ と * は強調として解釈されないようにエスケープする
              .replace(/[_*]/g, '\\$&'),
      )
      return { code: body, map: null }
    },
  }
}

export default defineConfig({
  // GitHub Pages ではリポジトリ名配下で配信される（例: /keiba-ai/）
  base: process.env.BASE_PATH ?? '/',
  plugins: [
    protectMath(),
    vue(),
    oxContentVue({
      srcDir: repoRoot,
      gfm: true,
      toc: true,
      embeds: false,
    }),
  ],
  resolve: {
    alias: { '@repo': repoRoot },
  },
  server: {
    // docs/ と experiments/ はリポジトリ直下にあるので site/ の外を読めるようにする
    fs: { allow: [repoRoot] },
  },
})
