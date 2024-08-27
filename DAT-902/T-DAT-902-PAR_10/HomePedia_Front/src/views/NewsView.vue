<template>
  <div>
    <div class="news-wrap">
      <div class="news">
        <div v-for="item in articles" :key="item.guid" class="article">
          <div class="article-text">
            <h2 class="title" @click="goToNews(item.link)">{{ item.title }}</h2>
            <div class="description" v-html="item.description"></div>
          </div>
          <div class="meta-data">
            <div class="author">{{ item.creator }}</div><div>&nbsp;-&nbsp;</div>
            <div class="date">{{ formatDate(item.pubDate) }}</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import xml2js from 'xml2js';

export default {
  data() {
    return {
      articles: [],
      articleGuids: new Set(), // Track unique GUIDs
    };
  },
  mounted() {
    this.fetchRSSFeed();
  },
  methods: {
    fetchRSSFeed() {
      const url = 'https://www.notaires.fr/fr/rss/thematique?id_thematique=4101';
      axios.get(url)
          .then(response => {
            this.parseXML(response.data)
                .then(parsedData => {
                  this.articles = parsedData.filter((_, index) => index % 2 === 0); // Take every second article
                });
          })
          .catch(error => {
            console.error('Error fetching RSS feed:', error);
          });
    },
    parseXML(data) {
      return new Promise((resolve, reject) => {
        const parser = new xml2js.Parser({ trim: true, explicitArray: false });
        parser.parseString(data, (err, result) => {
          if (err) {
            reject(err);
          } else {
            const items = result.rss.channel.item;
            const uniqueArticles = [];

            items.forEach(item => {
              if (!this.articleGuids.has(item.guid)) {
                this.articleGuids.add(item.guid);
                uniqueArticles.push({
                  title: item.title,
                  description: item.description,
                  link: item.link,
                  pubDate: item.pubDate,
                  creator: item['dc:creator'],
                  guid: item.guid,
                });
              }
            });

            resolve(uniqueArticles);
          }
        });
      });
    },
    goToNews(link) {
      window.open(link, '_blank');
    },
    formatDate(dateString) {
      const options = { year: 'numeric', month: 'long', day: 'numeric', weekday: 'long' };
      const date = new Date(dateString);
      return date.toLocaleDateString('fr-FR', options);
    },
  },
};
</script>

<style scoped>
.article {
  background-color: rgba(255, 255, 255, 0.9);
  border-radius: 20px;
  padding: 20px;
  margin-bottom: 20px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.article-text {
  text-align: left;
}

.title {
  font-size: 1.2rem;
  color: var(--primary);
  cursor: pointer;
}

.description {
  margin-top: 10px;
  color: #333;
}

.meta-data {
  margin-top: 10px;
  font-size: 0.9rem;
  color: #777;
  display: flex;
}

.meta-data .date {
  margin-bottom: 5px;
}

.meta-data .author {
  font-weight: bold;
}
</style>
