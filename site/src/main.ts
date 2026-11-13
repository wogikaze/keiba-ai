import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'
import DocPage from './pages/DocPage.vue'
import ListPage from './pages/ListPage.vue'
import ExperimentsPage from './pages/ExperimentsPage.vue'
import NotFound from './pages/NotFound.vue'
import { pages } from './content'
import 'katex/dist/katex.min.css'
import './style.css'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/literature', component: ListPage, props: { section: 'literature', title: '先行研究' } },
    { path: '/data', component: ListPage, props: { section: 'data', title: 'データ' } },
    { path: '/ideas', component: ListPage, props: { section: 'ideas', title: '研究アイデア' } },
    { path: '/adr', component: ListPage, props: { section: 'adr', title: '設計判断 (ADR)' } },
    { path: '/experiments', component: ExperimentsPage },
    ...pages.map((page) => ({ path: page.path, component: DocPage, props: { page } })),
    { path: '/:pathMatch(.*)*', component: NotFound },
  ],
  scrollBehavior: (to) => (to.hash ? { el: to.hash } : { top: 0 }),
})

createApp(App).use(router).mount('#app')
