import Vue from 'vue'
import Router from 'vue-router'
const routerOptions = [
  { path: '/', component: 'Home' },
  { path: '/about', component: 'About' },
  { path: '/login', component: 'Login' },
  { path: '/register', component: 'Register' },
  { path: '/course/:courseid', component: 'Course', name: 'course' },
  { path: '/techstack', component: 'TechStack' },
  { path: '*', component: 'NotFound' }
]

const routes = routerOptions.map(route => {
  return {
    ...route,
    component: () => import(`@/components/${route.component}.vue`)
  }
})

Vue.use(Router)

export default new Router({
  routes,
  mode: 'history',
  linkActiveClass: 'mdl-navigation__link--current'
})
