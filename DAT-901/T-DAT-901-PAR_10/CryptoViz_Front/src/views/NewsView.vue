<template>
    <div class="grid news_main">
        <div class="main" v-for="(article, i) in articles" :key="i">
            <router-link :to="{ name: 'post', params: {id :i}}" >
            <MiniaturePost class="item" :h1="article.h1" :index="i" :picture="article.picture[0]"/>
            </router-link>
        </div>
    </div>
</template>
<script>
import MiniaturePost from '@/components/MiniaturePost.vue';

export default {
    data: function () {
        return {
        }
    },
    components:{
      MiniaturePost
    },
    mounted() {
        this.$store.dispatch("fetchAllArticles")
    },
    computed: {
    articles() {
      return this.$store.state.articles;
    }
  },
  methods: {
  }
}
</script>

<style scoped>
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
  grid-gap: 30px;
}
.news_main{
    /*margin:2%;*/
    /*padding-top: 126px;*/
}

</style>
