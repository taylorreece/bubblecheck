// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import Navbar from './components/Navbar.vue'
import Drawer from './components/Drawer.vue'

Vue.config.productionTip = false

Vue.component('bubblecheck-navbar', Navbar)
Vue.component('bubblecheck-drawer', Drawer)

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})
