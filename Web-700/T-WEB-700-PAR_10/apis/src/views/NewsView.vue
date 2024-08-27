<template>
    <div>
        <div class="news-wrap">
            <div class="news">
                <div v-if=" current_currency == 'all'">
                    <div v-for="(articles, key) in xmlItems" :key="key">
                        <div v-for="item in articles" :key="item.id" class="article">
                            <div class="description-image" v-html="item.description"></div>
                            <div class="article-text">
                                <h2 class="title" v-on:click="gotonews(item, current_currency)">{{ item.title }}</h2>
                                <div class="description" v-html="item.description"></div>
                            </div>
                            <div class="meta-data">
                                <div class="currency">{{ key }}</div>
                                <div class="date">{{ item.date }}</div>
                            </div>
                        </div>
                    </div>
                </div>
                <div v-else-if=" current_currency == 'favorite'">
                    <div v-for="(articles, key) in favs" :key="key">
                        <div v-for="item in articles" :key="item.id" class="article">
                            <div class="description-image" v-html="item.description"></div>
                            <div class="article-text">
                                <h2 class="title" v-on:click="gotonews(item, current_currency)">{{ item.title }}</h2>
                                <div class="description" v-html="item.description"></div>
                            </div>
                            <div class="meta-data">
                                <div class="currency">{{ key }}</div>
                                <div class="date">{{ item.date }}</div>
                            </div>
                        </div>
                    </div>
                </div>
                <div v-else>
                    <div v-for="item in xmlItems[this.current_currency.toLowerCase()]" :key="item.id" class="article">
                        <div class="description-image" v-html="item.description"></div>
                        <div class="article-text">
                            <h2 class="title" v-on:click="gotonews(item, current_currency)">{{ item.title }}</h2>
                            <div class="description" v-html="item.description"></div>
                        </div>
                        <div class="meta-data">
                            <div class="currency">{{ current_currency }}</div>
                            <div class="date">{{ item.date }}</div>
                        </div>
                    </div>
                </div>
                
            </div>
            <div class="menu">
                <div>
                    <ul>
                        <li>
                            <router-link to="/news/all">
                                <a v-on:click="changeNews('all')" this.current_currency="all">Toutes les actus</a>
                            </router-link>
                        </li>
                        <li v-if="currentUser.id">
                            <router-link to="/news/favorite">
                                <a id="favorites" v-on:click="printFavorite(); this.current_currency = 'favorite' ">Actus
                                    des
                                    favoris</a>
                            </router-link>
                        </li>
                        <li v-for="coin in coins" :key="coin.crypto.id">
                            <router-link v-bind:to="'/news/' + coin.crypto.id">
                                <a v-on:click="changeNews(coin.crypto.id); this.current_currency = coin.crypto.id ">{{
                                    coin.crypto.name
                                }}</a>
                            </router-link>

                        </li>
                    </ul>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
import store from '@/store';
import axios from 'axios';
import xml2js from 'xml2js';
//import $ from 'jquery';
export default {
    data: function () {
        return {
            xmlItems: new Object(),
            current_currency: "",
            coins: new Object(),
            currentUser: this.$store.state.user,
            subs: [],
            favs: []
        }
    },
    mounted() {
        //xml file calling
        const coin = this.$route.params.id;
        console.log(coin);
        this.getCoinsList();
        if(coin == "favorite")
        {
            this.printFavorite();
        }
        else{
            this.changeNews(coin);
        }
    },
    methods: {
        printFavorite() {
            this.getFavorite();
            this.subs.forEach(sub => {
                axios.get("https://cointext.com/fr/actualites/tag/"+ sub.crypto.id +"/feed/")
                    .then(response => {
                        this.parseXML(response.data)
                            .then((data) => {
                                //console.log(data);
                                this.favs.push(data);
                            });
                    });
            })
        },
        getCoinsList() {
            axios
                .get("http://localhost:4000/articles")
                .then(response => {
                    var coinsList = response.data.data;
                    this.coins = coinsList;
                })
        },
        getFavorite() {
            axios.get("http://localhost:4000/" + this.currentUser.id + "/subscriptions")
                .then(response => {
                    var subs = response.data.data
                    //console.log(subs)
                    // console.log(subs.filter(subs => subs.crypto !== null))
                    this.subs = subs.filter(subs => subs.crypto !== null)
                    //console.log(this.subs)
                    //this.getCrypto();
                })
                this.current_currency = "favorite";
        },
        changeNews(crypto) {
            if (crypto != "all") {
                axios
                    .get("http://localhost:4000/cryptos/" + crypto + "/articles")
                    .then(response => {
                        var news_source = response.data.data[0];
                        //console.log(news_source.src);
                        axios.get(news_source.src)
                            .then(response => {
                                this.parseXML(response.data)
                                    .then((data) => {
                                        this.xmlItems[news_source.crypto.id] = data;
                                    });
                            });
                    });
            }
            else {
                axios
                    .get("http://localhost:4000/articles")
                    .then(response => {
                        var news_sources = response.data.data;
                        news_sources.forEach(news_source => {
                            axios.get(news_source.src)
                                .then(response => {
                                    this.parseXML(response.data)
                                        .then((data) => {
                                            this.xmlItems[news_source.crypto.id] = data;

                                        });
                                });
                        })
                        //console.log(this.xmlItems)
                    })
            }
            this.current_currency = crypto;
            //console.log(this.current_currency);
        },
        gotonews(item, currency) {
            store.state.news = item;
            this.$router.push({ path: '/one_news/' + currency + '/' + item.title.replace(/[^a-zA-Z 1234567890 ]/g, '').replace(/\s/g, '_') });
        },
        //xml file data parsing
        parseXML(data) {
            return new Promise(resolve => {
                var k = "";
                var arr = [],
                    parser = new xml2js.Parser(
                        {
                            trim: true,
                            explicitArray: true
                        });
                parser.parseString(data, function (err, result) {
                    var obj = result.rss.channel[0];
                    //console.log(obj);
                    for (k in obj.item) {
                        var item = obj.item[k];
                        arr.push({
                            title: item.title[0],
                            description: item.description[0],
                            link: item.link[0],
                            crypto: item.category[2],
                            date: item.pubDate[0].substr(0, 16),
                            content: item["content:encoded"][0]
                        });
                    }
                    resolve(arr);
                });
            });
        },
        changeColor(id) {
            document.getElementById(id).style.color = "#ff0000"; // forecolor
            document.getElementById(id).style.backgroundColor = "#ff0000"; // backcolor
        }
    }
}
</script>

<style>
.description p:nth-child(3) {
    display: none;
}

.article {
  background-color: rgba(255, 255, 255, 0.9);
  border-radius: 20px;
  position: relative;
  display: flex;
  height: 200px;
  color: black;
  justify-content: space-between;
  padding-right: 40px;
  margin-bottom: 40px;
}

.news > div {
  display: grid;
  margin-right: 50px;
}

.description-image {
    width: 34%;
    height: 100%;
}

.description-image img {
    width: 100%;
    height: 100%;
    border-radius: 20px;
    object-fit: cover;
}

.description-image p,
.description img {
    display: none;
}

h2.title a {
    color: black;
    text-decoration: none;
}

h2.title {
    font-size: 1rem;
}

.article-text {
    width: 48%;
    text-align: left;
    padding: 20px 0;
}

ul li {
    margin-bottom: 20px;
}

.vl {
    border-left: 6px solid green;
    height: 500px;
}

.currency {
  font-family: 'Kelly Slab', cursive;
  text-transform: capitalize;
  color: #F7DA52;
  background-color: #070500;
  border-radius: 20px;
  padding: 3px 10px;
}

.news-wrap .menu {
    border-left: solid 1px var(--yellow);
    font-family: 'Kelly Slab', cursive;
}


.news-wrap .menu ul {
    text-align: left;
    color: white;
}

.news {
    width: 75%;
}

.news-wrap {
    margin: 20px auto;
    display: flex;
}

.news-wrap .menu {
  width: 25%;
}

.news-wrap .menu div {
    position: sticky;
    top: 7rem;
}

.news-wrap .menu a {
  text-decoration: none;
  color: white;
  font-size: 18px;
}

.news-wrap .menu a.router-link-active a{
  color: var(--yellow);
}

.meta-data {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    align-items: flex-end;
    margin: 20px 0;
}

/*#favorites {*/
/*    color: #F7DA52;*/
/*}*/

.title,
.news-wrap .menu li {
    cursor: pointer;
}

.news-wrap h2.title {
  margin: 0;
}

.news-wrap .date {
  font-style: normal;
  font-weight: 700;
  font-size: 12px;
  line-height: 14px;
  text-align: right;
  color: #000000;
}
</style>