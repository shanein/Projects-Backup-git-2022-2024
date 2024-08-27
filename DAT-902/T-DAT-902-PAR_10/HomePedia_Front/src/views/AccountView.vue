<template>
  <div class="about">
<!--    <h1>This is an account page</h1>-->
      <router-view v-if="!this.$store.state.user"/>
      <div v-else class="about" style="">
        {{ console.log(this.$store.state.user)}}

        <table style="width: fit-content">
          <tr>
            <th class="icon-user-big" rowspan="2">
              <img v-if="this.$store.state.user.profile_picture" v-bind:src="'data:image/jpeg;base64,'+ $store.state.user.profile_picture" />
              <img v-else alt="userIcon" src="@/assets/user-icon.png">
            </th>
            <td style="text-align: left; color:var(--primary); font-size: 40px; padding: 2px 25px; text-transform: capitalize">
              {{ this.$store.state.user.firstname }} {{ this.$store.state.user.lastname }}
            </td>
          </tr>
          <tr>
            <td style="text-align: left; padding: 10px 25px">
              <a href="/#/edit" style="background-color:var(--primary); text-decoration: none; color: var(--backgroundColor); padding: 5px 30px;
                        margin-right:50px; font-size: 20px; font-weight: 500;">Edit
                profile</a>
              <a href="/" onclick="localStorage.clear();" style="color:var(--primary); text-decoration:none; font-size: 20px">Log out</a>
            </td>
          </tr>
        </table>

        <hr style="background-color:var(--primary); height: 10px; border:none; width: 100%; margin: 0;margin-top: 40px;" />
<!--        <div class="favorites">-->
<!--          <p style="color: var(&#45;&#45;primary); font-size: 30px; text-align:left;font-family: 'Kelly Slab', sans-serif">My favorites <img-->
<!--              src="../img/heart-full.png" style="width:20px" /></p>-->
<!--          <div class="cryptolist">-->
<!--            <table style="background-color:	var(&#45;&#45;backgroundColor)" v-if="posts && posts.length">-->
<!--              <tr class="tab-index">-->
<!--                <th style="width:3%; padding-left: 1%">#</th>-->
<!--                <th style="width:25%">Coin</th>-->
<!--                <th style="width:8%">Price</th>-->
<!--                <th style="width:8%">Price change</th>-->
<!--                <th style="width:8%">24h volume</th>-->
<!--                <th style="width:8%">Mkt Cap</th>-->
<!--                <th style="width:5%; text-align: center" v-if="currentUser.token">Favorites</th>-->
<!--              </tr>-->
<!--              <tr class="coin-list" v-for="(post, index ) in posts" :key="post.name">-->
<!--                <router-link :to="{ name: 'CryptoView', params: {id : post.id}  }" custom v-slot="{ navigate }">-->
<!--                  <td role="link" class="list-id" @click="navigate">-->
<!--                    {{ index + 1 }}-->
<!--                  </td>-->
<!--                  <td class="coin" role="link" @click="navigate">-->
<!--                    <div class="coin-image">-->
<!--                      <img :src="`${post.image}`">-->
<!--                    </div>-->
<!--                    <div class="coin-name">-->
<!--                      {{ post.name }}-->
<!--                    </div>-->
<!--                    <div class="coin-symbol">-->
<!--                      {{ post.symbol }}-->
<!--                    </div>-->
<!--                  </td>-->
<!--                </router-link>-->
<!--                <td class="coin_price">{{ post.current_price.toLocaleString("en-US", {style: "currency", currency: "USD"}) }}</td>-->
<!--                <td :class="`${post.price_color}`">${{ post.rounded_price_change_24h }}</td>-->
<!--                <td class="coin_volume">{{ post.total_volume.toLocaleString("en-US", {style: "currency", currency: "USD"}) }}</td>-->
<!--                <td class="mkt_cap">{{ post.market_cap.toLocaleString("en-US", {style: "currency", currency: "USD"}) }}</td>-->
<!--                <td class="favorites" v-if="currentUser.token">-->
<!--                  <button style="background-color:transparent; border:none; cursor: pointer; padding-top: 5px;" v-on:click="setFavorite(post.id, post.heart)">-->
<!--                    <img style="width:20px; float:left" :src="require(`@/img/${post.heart}`)"/>-->
<!--                  </button>-->
<!--                </td>-->
<!--              </tr>-->
<!--            </table>-->
<!--            <p v-else style="color: white">You don't have favorite crypto currencies</p>-->
<!--          </div>-->
<!--        </div>-->
      </div>
    </div>
</template>
<script>

import axios from "axios";

export default {
  data() {
      return {
        currentUser: this.$store.state.user,
        posts: [],
        subs: []
      }
  },
  methods: {
    //Function to get all cryptocoins in table
    // getCrypto: function () {
    //   //convert tab of crypto to url part
    //   // this.cryptoarrays.join('%2C')
    //   // console.log(this.cryptoarrays)
    //   //get api with tab value
    //   axios
    //       .get("http://127.0.0.1:8000/cryptos/")
    //       // .get("https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids=" + this.cryptoarrays + "&order=market_cap_desc&per_page=10&page=1&sparkline=false&x_cg_demo_api_key=CG-2r8ib2dqpFsVk5UG5Hn38hZy")
    //       .then(response => {
    //         var posts = response.data
    //         // var posts = response.data.data
    //         console.log(posts)
    //
    //         posts.forEach(post => {
    //           // add rounded value to the post array
    //           post.rounded_price_change_24h = (post.price_change_24h).toFixed(5)
    //           // give colors to prices
    //           post.price_color = post.price_change_24h >= 0 ? "green" : "red"
    //
    //           if (this.currentUser.token) {
    //             console.log(post.id)
    //             console.log(this.subs.map(e => e.crypto))
    //             let indexOfValue = this.subs.map(e => e.crypto.id).indexOf(post.id);
    //             console.log(indexOfValue)
    //             post.heart = indexOfValue > -1 ? "heart-full.png" : "heart-empty.png"
    //           }
    //         })
    //
    //         this.posts = posts.filter(post => post.heart == "heart-full.png");
    //         // console.log(this.posts)
    //       });
    // },

    setFavorite : function (value, heart) {
      console.log(value)
      let index = this.posts.findIndex(posts => posts.id=== value)
      console.log(index)
      console.log(heart)

      if (heart === "heart-empty.png") {
        axios
            .post("http://127.0.0.1:8000/subscribe-crypto/",
                {
                  name: value
                },
                {
                  headers: {
                    Authorization: `Bearer ${this.currentUser.token}`,
                  }
                })
            .then((res) => {
              this.posts[index].heart = "heart-full.png"
              console.log(res)
            })
            .catch((errors) => {
              console.log(errors)
            })
      } else {
        axios
            .delete("http://127.0.0.1:8000/unsubscribe-crypto/", {
                  headers: {
                    Authorization: `Bearer ${this.currentUser.token}`,
                  },
                  data: {
                    name: value
                  }
                },
                )
            .then((res) => {
              this.posts.splice(index, 1);
              console.log(res)
            })
            .catch((errors) => {
              console.log(errors)
            })
      }
    },

    // Function to get Favorite cryptocoin (user)
    getFavorite : function () {
      // axios.get("http://127.0.0.1:8000/subscriptions-crypto/", {
      //       headers: {
      //         Authorization: `Bearer ${this.currentUser.token}`,
      //       }
      //     })
      //     .then(response=>{
      //       var subs = response.data
      //       console.log(subs)
      //       console.log(subs.filter(subs => subs.crypto !== null))
      //       this.subs = subs.filter(subs => subs.crypto !== null)
      //       console.log(this.subs)
      //       this.getCrypto();
      //     })
      //     .catch((errors) => {
      //       console.log(errors)
      //     })

    }
  },
  mounted() {
    console.log(this.$store.state)
    if (!this.$store.state.user) {
      console.log("redirect signin")
      this.$router.push('/account/signIn');
    } else {
      // this.getFavorite();
    }
    // console.log(this.$route.matched)
  }
}
</script>
<style>

.icon-user-big img {
  width: 110px;
  height: 110px;
  object-fit: contain;
}
</style>
