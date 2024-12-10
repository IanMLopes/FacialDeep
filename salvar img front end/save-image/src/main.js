import Vue from 'vue'
import App from './App.vue'
import axios from 'axios'
import VueAxios from 'vue-axios'
import DotEnv from 'dotenv'


// const BASE_URL = proces
const BASE_URL = process.env.VUE_APP_PROJECT_PRODUCTION
console.log(' BASE_URL ------>', BASE_URL)
axios.defaults.baseURL = BASE_URL;


// Vue.config.productionTip = false
Vue.use(VueAxios, axios)

DotEnv.config()

new Vue({
  render: h => h(App),
}).$mount('#app')
