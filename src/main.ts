import Vue from 'vue'
import App from './App.vue'
import './registerServiceWorker'
import router from './router'

console.log(process.env)
if (process.env.VUE_APP_PYTHON_HOST_URL) {
    (window as any).baseURL = process.env.VUE_APP_PYTHON_HOST_URL
    console.log(process.env.VUE_APP_PYTHON_HOST_URL);
}

import {BootstrapVue, IconsPlugin} from 'bootstrap-vue'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

Vue.use(BootstrapVue)
Vue.use(IconsPlugin)
const vue = new Vue({
    router,
    render: h => h(App)
}).$mount('#app')
