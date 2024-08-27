<template>
    <div class="article-wrap">
        <h1>{{ title }}</h1>
        <div class="article-content">
            <div class="content" v-html="content"></div>
        </div>
    </div>
</template>

<script>
import store from '@/store';
import axios from 'axios';
import xml2js from 'xml2js';
export default {
    mounted() {
        const coin = this.$route.params.currency;
        axios
            .get("http://localhost:4000/cryptos/" + coin + "/articles")
            .then(response => {
                this.title_id = this.$route.params.id;
        
                var news_source = response.data.data[0];
                console.log(response);
                axios.get(news_source.src)
                    .then(response => {
                        this.parseXML(response.data)
                            .then((data) => {
                                this.xmlItems[news_source.crypto.id] = data;
                            });
                    });
            });
    },
    methods: {
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
                        console.log(this.title_id);
                        if(item.title[0].replace(/[^a-zA-Z 1234567890 ]/g, '').replace(/\s/g, '_') == this.title_id)
                        {
                            arr.push({
                                title: item.title[0],
                                description: item.description[0],
                                link: item.link[0],
                                crypto: item.category[2],
                                date: item.pubDate[0].substr(0, 16),
                                content: item["content:encoded"][0]
                            });
                        }
                    }
                    resolve(arr);
                });
            });
        },
    },
    data: function () {
        return {
            title: store.state.news.title,
            description: store.state.news.description,
            link: store.state.news.link,
            date: store.state.news.date,
            content: store.state.news.content,
            xmlItems: new Object(),
            title_id: ""
        }
    }
}
</script>
<style>
.article-wrap{
  color: white;
  text-align: left;
}

.article-wrap h1{
  margin-bottom: 20px;
}

.article-wrap img {
  max-width: 50%;
  object-fit: contain;
  height: auto;
  margin: auto;
  display: block;
}
</style>