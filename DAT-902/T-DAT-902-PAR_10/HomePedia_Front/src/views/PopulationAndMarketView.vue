<template>
  <div class="searchBar">
    <div v-if="currentUser && currentUser.is_admin" class="addCoin">
      <form class="formAddCoin" @submit.prevent="addCoin">
        <input v-model="coinname" type="text" placeholder="Crypto name" required />
        <p>
          <input class="create create-btn" type="submit" value="CREATE CRYPTO">
        </p>
        <div v-if="errorMessage" class="errorMessage" style="margin-bottom: 20px">{{ errorMessage }}</div>
      </form>
    </div>
  </div>
  <div>
<!--    <crypto-market-cap-chart :chartData="cryptoData"></crypto-market-cap-chart>-->
  </div>
  <div class="list-graph">
    <PopulationHorizontalBarChart></PopulationHorizontalBarChart>
  </div>
</template>

<script>
import '../../globalVars.css';
import PopulationHorizontalBarChart from "@/components/PopulationHorizontalBarChart";
// import CryptoMarketCapChart from "@/components/CryptoMarketCapChart";

export default {
  components: {
    // CryptoMarketCapChart
    PopulationHorizontalBarChart
  },
  data() {
    return {
      errors: [],
      currentUser: this.$store.state.user,
      textSearch: "",
      subs: [],
      errorMessage: "",
    }
  },


  // Fetches posts when the component is created.
methods: {



    // setFavorite : function (value, heart) {
    //   console.log(value)
    //   let index = this.posts.findIndex(posts => posts.id=== value)
    //   console.log(index)
    //   console.log(heart)
    //
    //   if (heart === "heart-empty.png") {
    //     axios
    //         .post("http://127.0.0.1:8000/subscribe-crypto/",
    //             {
    //               name: value
    //             },
    //             {
    //               headers: {
    //                 Authorization: `Bearer ${this.currentUser.token}`,
    //               }
    //             })
    //         .then((res) => {
    //           this.posts[index].heart = "heart-full.png"
    //           console.log(res)
    //         })
    //         .catch((errors) => {
    //           console.log(errors)
    //         })
    //   } else {
    //     axios
    //         .delete("http://127.0.0.1:8000/unsubscribe-crypto/", {
    //               headers: {
    //                 Authorization: `Bearer ${this.currentUser.token}`,
    //               },
    //               data: {
    //                 name: value
    //               }
    //             },
    //         )
    //         .then((res) => {
    //           this.posts[index].heart = "heart-empty.png"
    //           console.log(res)
    //         })
    //         .catch((errors) => {
    //           console.log(errors)
    //         })
    //   }
    // },

    // Function to get Favorite cryptocoin (user)
    // getFavorite : function () {
    //   axios.get("http://127.0.0.1:8000/subscriptions-crypto/", {
    //     headers: {
    //       Authorization: `Bearer ${this.currentUser.token}`,
    //     }
    //   })
    //       .then(response=>{
    //         var subs = response.data
    //         console.log(subs)
    //         console.log(subs.filter(subs => subs.crypto !== null))
    //         this.subs = subs.filter(subs => subs.crypto !== null)
    //         console.log(this.subs)
    //         this.getCrypto();
    //       })
    //       .catch((errors) => {
    //         console.log(errors)
    //       })
    //
    // },

  },


mounted: function () {
    if (this.$store.state.user) {
      // this.getFavorite();
    } else {
      // this.getCrypto();
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
  color: var(--primary);
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
  color: var(--primary);
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
  color: var(--primary);
}

th {
  text-align: left;
}

td.list-id {
  color: var(--primary);
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
  background-color: var(--primarylight);
}

div.searchBar {
  margin-bottom: 10px;
}

input[type=text]:focus, input[type=password]:focus, input[type=email]:focus {
  outline: 2px solid var(--primary);
  /* oranges! yey */
}

[role="link"]:hover {
  cursor: pointer;
}

.errorMessage {
  color: var(--primary);
}

.list-graph {
  display: flex;
}
</style>
