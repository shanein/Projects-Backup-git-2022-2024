/* eslint-disable */
import { createStore } from 'vuex'
import * as cheerio from 'cheerio';

const SERVER_BASE_URL = process.env.VUE_APP_API_URL ?? "http://194.164.196.136:"
// Create a new store instance.
const store = createStore({
  state() {
    return {
      user: [],
      news: [],
      articles: []
    }
  },
  getters: {
    html_content: state => state.articles,
    posts: state => {
      return state.articles
    }
  },
  mutations: {
    DEFINE_USER(state, payload) {
      state.user = payload
    },
    MUTATE_ARTICLES(state, payload) {
      state.articles.push(payload)
    },
  },
  actions: {
    defineUser(context, amount) {
      context.commit('DEFINE_USER', amount)
    },
    async fetchAllArticles(context) {
      try {
        let response = await fetch(`${SERVER_BASE_URL}8080/kafka`);
        if (!response.ok)
          throw new Error('Network response was not ok');

        const tmp = []
        let data = await response.json()
        data.forEach((articles, i) => {
          const $ = cheerio.load(articles.html_content)
          const imageSources = []
          const tmp_object = {}
          let html_picture = ""

          tmp_object["html_content"] = articles.html_content
          tmp_object["h1"] = $("h1").text()

          html_picture = $('picture').map((index, element) => {
            return $.html(element);
          }).get();

          tmp_object["picture"] = html_picture
          tmp.push(tmp_object)
        })
      
        context.state.articles = tmp
      } catch (error) {
        console.error('There was a problem with the fetch operation:', error);
      }
    }

  }
})

export default store;
