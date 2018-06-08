import Vue from 'vue'
import App from './App.vue'
import {
  Select,
  Option,
  Dropdown,
  DropdownMenu,
  DropdownItem,
} from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'


Vue.use(Select)
Vue.use(Option)
Vue.use(Dropdown)
Vue.use(DropdownMenu)
Vue.use(DropdownItem)
Vue.config.productionTip = false


const eventHub = new Vue()
Vue.mixin({
  data: () => ({eventHub})
})
new Vue({
  el: '#app',
  components: { App },
  template: '<App/>'
})
