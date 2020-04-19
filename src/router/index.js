import Vue from 'vue'
import Router from 'vue-router'
import watchList from '@/pages/watchList'
import search from '@/pages/search'
import routerDetail from '@/pages/routerDetail'
import help from '@/pages/help'

Vue.use(Router)

export default new Router({
	// mode: 'history',
  routes: [
    {
      path: '/',
      name: 'watchList',
      component: watchList
    },
    {
      path: '/search',
      name: 'search',
      component: search
    },
    {
      path: '/routerDetail',
      name: 'routerDetail',
      component: routerDetail
    },
    {
      path: '/help',
      name: 'help',
      component: help
    }
  ]
})
