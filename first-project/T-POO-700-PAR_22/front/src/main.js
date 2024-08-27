import { createApp } from 'vue'
import App from './App.vue'
import "bootstrap/dist/css/bootstrap.css"
import "bootstrap/dist/js/bootstrap.js"

// import Vuex from 'vuex'
// import Vue from 'vue'

// createApp(App).use(store).mount('#app')

import store from './store'

import router from './router'

const app = createApp(App).use(router)

app.use(store)

app.mount('#app')

/*

import "bootstrap/dist/js/bootstrap.js"

import { createStore } from 'vuex'

// import 'bootstrap/dist/css/bootstrap.css'
// import { createApp } from 'vue'
// import App from './App.vue'
// import router from './router'
// import store from './store/store'


// Create a new store instance.
const store = createStore({
    state () {
        return {
            state: {
                month: 8,
                day: 12,
                year: 2008
            }
        }
    },
    // mutations: {
    //     increment (state) {
    //         state.count++
    //     },
    //     defineUser (state, current) {
    //         state.user = current
    //     }
    // }

})

export default store

const app = createApp(App);
// app.use(router)
app.use(store)
app.mount('#app')

// app.use(store)

store.commit('increment')

console.log(store.state.count)*/
