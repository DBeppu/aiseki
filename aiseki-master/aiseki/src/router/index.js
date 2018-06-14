import Vue from 'vue'
import Router from 'vue-router'
import Index from '@/components/Index'
import List from '@/components/List'
import LocationList from '@/components/LocationList'
import Item from '@/components/Item'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Index',
      component: Index
    },
    {
      path: '/list',
      name: 'List',
      component: List
    }, 
    {
      path: '/lolist',
      name: 'LocationList',
      component: LocationList
    },
    {
      path: '/item',
      name: 'Item',
      component: Item
    }
  ]
})
