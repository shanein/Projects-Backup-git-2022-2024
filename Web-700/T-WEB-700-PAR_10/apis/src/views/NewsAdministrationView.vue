<template>
  <div class="searchBar">
    <div v-if="currentUser.role == 'admin'" class="addNews">
      <form class="formAddCoin" @submit.prevent="addNews">
        <input v-model="coinname" type="text" placeholder="Crypto name" required />
        <p>
          <input class="create create-btn" type="submit" value="CREATE NEWS">
        </p>
        <p v-if="errorMessage" class="errorMessage" style="margin-bottom: 20px">{{ errorMessage }}</p>
      </form>
    </div>
    <div class="cryptolist">
      <table style="background-color:	#202020" v-if="news && news.length">
        <tr class="tab-index">
          <th style="width:3%; padding-left: 1%">#</th>
          <th style="width:37%">Coin</th>
          <th style="width: 50%">Link</th>
          <th style="width:5%"></th>
        </tr>
        <tr class="coin-list" v-for="(post, index) in news" :key="post.name">
          <td class="list-id">
            {{ index }}
          </td>
          <td class="coin">
            <div class="coin-image">
              <img :src="`${post.crypto.image}`">
            </div>
            <div class="coin-name">
              {{ post.crypto.name }}
            </div>
          </td>
          <td class="coin_link"><a v-bind:href="post.src" target="_blank">{{ post.src }}</a></td>
          <td><a href="javascript:void(0)" v-on:click="newsDelete(post.id)" style="line-height: 0;display: block;"><img src="@/img/Trash.svg" style="width:27px" /></a></td>
        </tr>
      </table>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import '../../globalVars.css';

export default {
  data() {
    return {
      news: [],
      // cryptoarrays: [],
      errors: [],
      currentUser: this.$store.state.user,
      errorMessage: "",
    }
  },


  // Fetches posts when the component is created.
  methods: {

    //Function to get all cryptocoins in table
    getNews: function () {
      //convert tab of crypto to url part
      // this.cryptoarrays.join('%2C')
      // console.log(this.cryptoarrays)
      //get api with tab value
      axios
          .get("http://localhost:4000/articles")
          // .get("https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids=" + this.cryptoarrays + "&order=market_cap_desc&per_page=10&page=1&sparkline=false")
          .then(response => {
            var news = response.data.data
            // console.log(news)
            this.news = news
          });
    },

    // Function to delte a cryptocoin (admin)
    newsDelete: function (value) {
      axios
          .delete("http://localhost:4000/articles/" + value + '?admin=' + this.currentUser.id)
          .then(() => {
            // const index = this.posts.map(post => post.id).indexOf(value);
            // only splice array when item is found
            let index = this.news.findIndex(posts => posts.id === value)
            // console.log(index)
            this.news.splice(index, 1); // 2nd parameter means remove one item only
            // if (this.posts.length == 0) {
            //   this.getCryptoApi();
            //
            // }
            // console.log(this.news.length)

          })
          .catch((errors) => {
            console.log(errors)
          })
    },

    // Function to add a cryptocoin (admin)
    addNews: function () {
      axios
        .post('http://localhost:4000/articles?admin=' + this.currentUser.id,
            {
                "article":{
                  "src":"https://cointext.com/fr/actualites/tag/" + this.coinname + "/feed/"
                },
                "crypto":this.coinname
            })
        .then((res) => {
          //faire en sorte de se connecter
          // console.log(res.data.data);
          let newNews = res.data.data
          // console.log(newNews)
          if (newNews) {
            // console.log(newNews)
            this.news.push(newNews)
            this.errorMessage = ""
            this.coinname = ""
          } else {
            this.errorMessage = "Crypto-currency not found, please check if the cryptocurrency exists"
          }

        })
        .catch((err) => {
          console.log(err)
          this.errorMessage = err.response.data.errors.unique_cryptos[0]
        })
    }
  },
  mounted: function () {
    this.getNews();
    // console.log(this.news)
  }
};

</script>

<style>
td.coin_link {
  color: white;
  text-align: left;
}
</style>
