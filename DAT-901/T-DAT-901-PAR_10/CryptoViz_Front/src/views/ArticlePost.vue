<template>
  <div ref="wrapper" class="external-wrapper extended" v-html="current_post"></div>
</template>
  
<script>
import { mapGetters } from 'vuex';
export default {
  data(){
    return {
      current_post: ""
    }
  },
  mounted() {
    console.log(this.$route.params.id)
    this.current_post = this.posts[this.$route.params.id].html_content
    console.log(this.current_post)

  },
  computed: {
    ...mapGetters(["posts"]),
    postId() {
      return this.$route.params.id;
    },
  }
};
</script>
  
<style>

.external-wrapper main {
  width: initial;
  max-width: initial;
  margin: initial;
  padding-top: initial;
}
/* Styles communs à tous les éléments à cacher */
.external-wrapper svg,
.external-wrapper .sticky-banner,
.external-wrapper .post-meta,
.external-wrapper .absolute,
.external-wrapper input,
.external-wrapper blockquote,
.external-wrapper aside,
.external-wrapper .container>a,
.external-wrapper .uppercase,
.external-wrapper .breadcrumbs {
  display: none;
}

/* Styles spécifiques à .external-wrapper */
.external-wrapper {
  position: relative;
  /*margin: 12% auto;*/
  /*padding: 0 126px;*/
  text-align: left;
  /*border-radius: 15px;*/
  /* border-radius: 5px; /* Vous n'avez pas besoin de déclarer deux fois la même propriété */
}

/* Styles pour d'autres éléments */
.external-wrapper section.bg-cover.bg-center {
  font-size: 20px;
}
.external-wrapper .post-article-image picture{
  padding-top: 20px;
  margin-top: 20px;
}
.external-wrapper .post-article-image img{
  border-radius: 15px;
  max-height: 600px;
  width: auto;
  margin-left: auto;
  margin-right: auto;
  display: block;
}

.external-wrapper .mainStyle {
  border-radius: 15px;
}

.external-wrapper .articlePost {
  background-color: red;
  font-size: 34px;
  z-index: 1000;
}
</style>
