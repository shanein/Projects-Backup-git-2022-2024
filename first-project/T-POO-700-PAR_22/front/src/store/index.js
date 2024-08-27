import { createStore } from 'vuex'

// Create a new store instance.
const store = createStore({
  state () {
    return {
      user: []
    }
  },
  mutations: {
    DEFINE_USER(state, payload) {
      state.user = payload
    }
  },
  actions: {
    defineUser(context, amount) {
      context.commit('DEFINE_USER', amount)
    }
  }
})

export default store;
