import { fileURLToPath } from 'node:url'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { oxContentVue } from '@ox-content/vite-plugin-vue'

const repoRoot = fileURLToPath(new URL('..', import.meta.url))

export default defineConfig({
  // GitHub Pages ではリポジトリ名配下で配信される（例: /keiba-ai/）
  base: process.env.BASE_PATH ?? '/',
  plugins: [
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
