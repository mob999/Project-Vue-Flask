import Vue from 'vue'
import Router from 'vue-router'
import ImageContainer from '@/components/ImageContainer'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'ImageContainer',
      component: ImageContainer
    }
  ]
})
