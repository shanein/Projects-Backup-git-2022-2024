<template>
  <div class="about">
<!--    <h1>This is an account page</h1>-->
<!--    <SignIn  v-if="this.$store.state.user.id == null && this.$route.matched[1].components.default.name == 'SignIn'"/>-->
<!--    <SignUp  v-if="this.$store.state.user.id == null && this.$route.matched[1].components.default.name == 'SignUp'"/>-->
    <router-view v-if="this.$store.state.user.id == null"/>
      <div v-else class="about" style="">
        <table style="width: fit-content">
          <tr>
            <th class="icon-user-big" rowspan="2">
              <img v-if="this.$store.state.user.profile_picture" v-bind:src="'data:image/jpeg;base64,'+ $store.state.user.profile_picture" />
              <img v-else alt="userIcon" src="@/assets/user-icon.png">
            </th>
            <td style="text-align: left; color:white; font-size: 40px; padding: 2px 25px; text-transform: capitalize">
              {{currentUser.firstname}} {{ currentUser.lastname}}
            </td>
          </tr>
          <tr>
            <td style="text-align: left; padding: 10px 25px">
              <a href="/#/edit" style="background-color:var(--yellow); text-decoration: none; color: black; padding: 5px 30px;
                        margin-right:50px; font-size: 20px; font-weight: 500;">Edit
                profile</a>
              <a href="/" onclick="localStorage.clear();" style="color:white; text-decoration:none; font-size: 20px">Log out</a>
            </td>
          </tr>
        </table>

        <hr style="background-color:var(--yellow); height: 10px; border:none; width: 100%; margin: 0;margin-top: 40px;" />
        <div class="favorites">
          <p style="color: var(--yellow); font-size: 30px; text-align:left;font-family: 'Kelly Slab', sans-serif">My favorites <img
              src="../img/heart-full.png" style="width:20px" /></p>
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
              </tr>
              <tr class="coin-list" v-for="(post, index ) in posts" :key="post.name">
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
              </tr>
            </table>
            <p v-else style="color: white">You don't have favorite crypto currencies</p>
          </div>
        </div>
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
    getCrypto: function () {
      //convert tab of crypto to url part
      // this.cryptoarrays.join('%2C')
      // console.log(this.cryptoarrays)
      //get api with tab value
      axios
          .get("http://localhost:4000/cryptos")
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

            this.posts = posts.filter(post => post.heart == "heart-full.png");
            // console.log(this.posts)
          });
    },

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
      axios.get("http://localhost:4000/"+this.currentUser.id+"/subscriptions")
          .then(response=>{
            var subs = response.data.data
            // console.log(subs)
            // console.log(subs.filter(subs => subs.crypto !== null))
            this.subs = subs.filter(subs => subs.crypto !== null)
            // console.log(this.subs)
            this.getCrypto();
          })

    }
  },
  mounted() {
    // console.log(test)
    if (this.$store.state.user.id == null) {
      this.$router.push('/account/signIn');
    } else {
      this.getFavorite();
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
