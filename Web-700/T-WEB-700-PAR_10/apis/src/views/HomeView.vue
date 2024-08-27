<template>
  <div class="searchBar">
    <div v-if="currentUser.role == 'admin'" class="addCoin">
      <form class="formAddCoin" @submit.prevent="addCoin">
        <input v-model="coinname" type="text" placeholder="Crypto name" required />
        <p>
          <input class="create create-btn" type="submit" value="CREATE CRYPTO">
        </p>
        <div v-if="errorMessage" class="errorMessage" style="margin-bottom: 20px">{{ errorMessage }}</div>
      </form>
    </div>
    <div class="inputSearch">
      <input style="background-color:#202020; border: none;" type="text"
      placeholder="Search"
      v-model="textSearch"
      @keyup="searchCoin()"
      autofocus />
    </div>
    <div class="cryptolist">
      <table style="background-color:	#202020" v-if="posts && posts.length">
        <tr class="tab-index">
          <th style="width:3%; padding-left: 1%">#</th>
          <th style="width:25%">Coin</th>
          <th style="width:8%">Price</th>
          <th style="width:8%">Price change</th>
          <th style="width:8%">24h volume</th>
          <th style="width:8%">Mkt Cap</th>
          <th style="width:5%; text-align: center" v-if="currentUser.id">Favorites</th>
          <th style="width:5%" v-if="currentUser.role == 'admin'"></th>
        </tr>
        <tr class="coin-list" v-for="(post, index ) in filteredCoins" :key="post.name">
          <router-link :to="{ name: 'CryptoView', params: {id : post.id}  }" custom v-slot="{ navigate }">
            <td role="link" class="list-id" @click="navigate">
              {{ index + 1 }}
            </td>
          <td class="coin" role="link" @click="navigate">
            <div class="coin-image">
              <img :src="`${post.image}`">
            </div>
            <div class="coin-name">
              {{ post.name }}
            </div>
            <div class="coin-symbol">
              {{ post.symbol }}
            </div>
          </td>
          </router-link>
          <td class="coin_price">{{ post.current_price.toLocaleString("en-US", {style: "currency", currency: "USD"}) }}</td>
          <td :class="`${post.price_color}`">${{ post.rounded_price_change_24h }}</td>
          <td class="coin_volume">{{ post.total_volume.toLocaleString("en-US", {style: "currency", currency: "USD"}) }}</td>
          <td class="mkt_cap">{{ post.market_cap.toLocaleString("en-US", {style: "currency", currency: "USD"}) }}</td>
          <td class="favorites" v-if="currentUser.id">
            <button style="background-color:transparent; border:none; cursor: pointer" v-on:click="setFavorite(post.id, post.heart)">
              <img style="width:15px; float:left" :src="require(`@/img/${post.heart}`)" id="heart"/>
            </button>
          </td>
          <td v-if="currentUser.role == 'admin'"><a href="javascript:void(0)" v-on:click="cryptoDelete(post.id)" style="line-height: 0;display: block;"><img src="@/img/Trash.svg" style="width:27px" /></a></td>
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
      posts: [],
      // cryptoarrays: [],
      errors: [],
      currentUser: this.$store.state.user,
      textSearch: "",
      filteredCoins: [],
      subs: [],
      errorMessage: "",
    }
  },


  // Fetches posts when the component is created.
  methods: {

    //Function to get all cryptocoins in table
    getCrypto: function () {
      //convert tab of crypto to url part
      // this.cryptoarrays.join('%2C')
      // console.log(this.cryptoarrays)
      //get api with tab value
      axios
          .get("http://localhost:4000/cryptos")
          // .get("https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids=" + this.cryptoarrays + "&order=market_cap_desc&per_page=10&page=1&sparkline=false")
        .then(response => {
          var posts = response.data.data
          // console.log(posts)

          posts.forEach(post => {
            // add rounded value to the post array
            post.rounded_price_change_24h = (post.price_change_24h).toFixed(5)
            // give colors to prices
            post.price_color = post.price_change_24h >= 0 ? "green" : "red"

            if (this.currentUser.id) {
              // console.log(post.id)
              // console.log(this.subs.map(e => e.crypto))
              let indexOfValue = this.subs.map(e => e.crypto.id).indexOf(post.id);
              post.heart = indexOfValue > -1 ? "heart-full.png" : "heart-empty.png"
            }
          })

          this.posts = posts
          this.filteredCoins = posts
        });
    },

    // Function to delte a cryptocoin (admin)
    cryptoDelete: function (value) {
      axios
        .delete("http://localhost:4000/cryptos/" + value + '?admin=' + this.currentUser.id)
        .then(() => {
          // const index = this.posts.map(post => post.id).indexOf(value);
          // only splice array when item is found
          let index = this.posts.findIndex(posts => posts.id === value)
          // console.log(index)
          this.posts.splice(index, 1); // 2nd parameter means remove one item only
          // if (this.posts.length == 0) {
          //   this.getCryptoApi();
          //
          // }
          // console.log(this.posts.length)

        })
        .catch((errors) => {
          console.log(errors)
        })
    },

    // Function to serach a specific cryptocoin in table
    searchCoin() {
      this.filteredCoins = this.posts.filter(
          (post) =>
              post.name.toLowerCase().includes(this.textSearch.toLowerCase())
      );
      // console.log(this.filteredCoins)
    },

    // Function to get Favorite cryptocoin (user)
    getFavorite : function () {
      axios.get("http://localhost:4000/"+this.currentUser.id+"/subscriptions")
          .then(response=>{
            var subs = response.data.data
            // console.log(subs)
            // console.log(subs.filter(subs => subs.crypto !== null))
            this.subs = subs.filter(subs => subs.crypto !== null)
            // console.log(this.subs)
            this.getCrypto();
          })

    },

    // Function to set a favorite cryptocoin
    setFavorite : function (value, heart) {
      // console.log(value)
      let index = this.posts.findIndex(posts => posts.id === value)
      // console.log(index)
      // console.log(heart)

      if (heart === "heart-empty.png") {
        axios
            .post("http://localhost:4000/"+value+"/subscribe?id="+this.currentUser.id)
            .then((res) => {
              this.posts[index].heart = "heart-full.png"
              console.log(res)
            })
            .catch((errors) => {
              console.log(errors)
            })
      } else {
        axios
            .delete("http://localhost:4000/"+value+"/unsubscribe?id="+this.currentUser.id)
            .then((res) => {
              this.posts[index].heart = "heart-empty.png"
              console.log(res)
            })
            .catch((errors) => {
              console.log(errors)
            })
      }
    },

    // Function to add a cryptocoin (admin)
    addCoin: function () {
      axios
          .post('http://localhost:4000/cryptos?admin=' + this.currentUser.id,
              {
                "crypto":{
                  "name":this.coinname
                }
              })
          .then((res) => {
            //faire en sorte de se connecter
            // console.log(res.data.data);
            let newcrypto = res.data.data
            // console.log(newcrypto)
            if (newcrypto) {
              newcrypto.heart = "heart-empty.png"
              // console.log(newcrypto)
              this.posts.push(newcrypto)
              this.errorMessage = ""
              this.coinname = ""
            } else {
              this.errorMessage = "Crypto-currency not found"
            }

          })
          .catch((err) => {
            console.log(err)
            this.errorMessage = err.response.data.errors.unique_cryptos[0]
          })
      // alert(JSON.stringify(this.form))
    }

  },

  mounted: function () {
    if (this.currentUser.id) {
      this.getFavorite();
    } else {
      this.getCrypto();
    }

    // this.getCrypto();
    // console.log(this.posts)
    // }
  }
};

</script>

<style>
table {
  width: 100%;
  border-collapse: collapse;
}

div.searchBar {
  margin: auto;
}

div.searchBar input {
  width: calc(100% - 40px);
  margin-bottom: 20px;
  font-size: large;
}

.coin-image {
  display: flex;
  justify-content: center;
  align-content: center;
}

div.coin-image img {
  width: 30px;
  height: auto;
  margin-right: 10px;
  object-fit: contain;
}

div.coin-name {
  color: white;
  margin-right: 10px;
  font-weight: 700;
}

.coin-symbol {
  visibility: hidden;
}

.coin {
  float: left;
}

td.coin {
  display: flex;
  flex-direction: row;
  text-align: left;
  line-height: 35px;
  width: 100%;
}

td.coin_price, td.coin_volume, td.mkt_cap {
  color: white;
  text-align: left;
}

td.red {
  color: red;
  text-align: left;
}

td.green {
  color: green;
  text-align: left;
}

table tr.tab-index {
  height: 40px;
  padding-top: 20%;
  border-bottom: solid 2px lightgrey;
}

tr.tab-index th {
  color: white;
}

th {
  text-align: left;
}

td.list-id {
  color: white;
  text-align: left;
  padding-left: 1%;
}

td.coin {
  text-align: left;
}

tr.coin-list > td {
  margin-top: 10px;
  margin-bottom: 10px;
}

tr.coin-list:hover {
  background-color: rgb(24, 24, 24);
}

div.searchBar {
  margin-bottom: 10px;
}

input[type=text]:focus, input[type=password]:focus, input[type=email]:focus {
  outline: 2px solid var(--yellow);
  /* oranges! yey */
}

[role="link"]:hover {
  cursor: pointer;
}

.errorMessage {
  color: white;
}
</style>
