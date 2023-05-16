import Vue from 'vue'
import App from './App.vue'
import './registerServiceWorker'
import router from './router'

if (Vue.config.devtools) {
    (window as any).baseURL = 'http://localhost:5000'
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
