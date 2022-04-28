import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import Microm from 'microm'

var microm = new Microm();

Vue.config.productionTip = false;

export default microm

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
