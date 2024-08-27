<template>
  <h1>Chart Manager</h1>
  <div class="container">
    <h2>Graphique des worktimes dans le temps</h2>
    <Bar :chart-data="chartData" class="chart-bar"/>
  <h2>Graphique des durées des worktimes</h2>
  <Pie :chart-data="chartDatabis" class="chart-pie"/>
    <h2>Graphique des clock</h2>
    <Line :chart-data="chartDataline" class="chartlLine"/>
<!--    <LineChart />-->

  </div>


</template>

<script>

import { Bar } from 'vue-chartjs'
import { Pie } from 'vue-chartjs'
// import { LineChart } from 'vue-chartjs'
import { Line } from 'vue-chartjs'

// import { defineComponent, h, PropType } from 'vue'


import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale, ArcElement, LineElement, PointElement,} from 'chart.js'
import axios from "axios";

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale, ArcElement,  LineElement, PointElement)


export default {
  name: 'ChartManager',
  components: { Bar, Pie, Line },
  data() {
    return {
      posts: [],
      clokingtimes: [],
      barData: [[],[]],
      pieData: [[],[],[]],
      lineData: [[],[]],
      currentUser: this.$store.state.user,
      chartData: {
        labels: [],
        datasets: [
          {
            label: 'Worktime de la journée',
            backgroundColor: '#f87979',
            data: []
          }
        ]
      },
      chartDatabis: {
        labels: [],
        datasets: [
          {
            backgroundColor: ['#41B883', '#E46651', '#00D8FF', '#DD1B16'],
            data: []
          }
        ]
      },
      chartDataline: {
        labels: [],
        datasets: [
          {
            label: 'Heure du Clocking time',
            backgroundColor: '#f87979',
            data: []
          }
        ]
      }
    }
  },
  methods: {
    getWorkingTimes: function () {
      axios
          .get("http://localhost:4000/api/workingtimes/" + this.currentUser.id)
          .then(response => {
            this.posts = response.data.data.slice();
            this.posts.sort(function(a,b){
              return new Date(a.start) - new Date(b.start);
            })
            this.posts.forEach(post => {
              // console.log(Math.ceil((new Date(post.end) - new Date(post.start)) / (1000 * 60 * 60)) )
              this.barData[0].push(new Date(post.start).toLocaleDateString())
              this.barData[1].push(Math.ceil((new Date(post.end) - new Date(post.start)) / (1000 * 60 * 60)) )

              this.pieData[0].push(" Id : " + post.id + " ")
              this.pieData[1].push(Math.ceil((new Date(post.end) - new Date(post.start)) / (1000 * 60 * 60)) )
              this.pieData[2].push("#" + ("00000" + Math.floor(Math.random() * Math.pow(16, 6)).toString(16)).slice(-6))

            })

            this.chartData.labels = this.barData[0]

            this.chartData.datasets[0].data = this.barData[1]


            this.chartDatabis.labels = this.pieData[0]

            this.chartDatabis.datasets[0].data = this.pieData[1]

            this.chartDatabis.datasets[0].backgroundColor = this.pieData[2]
          });
    },

    getClokingTimes: function () {
      axios
          .get("http://localhost:4000/api/clocks/" + this.currentUser.id)
          .then(response => {

            this.clokingtimes = response.data.data.slice();
            console.log(this.clokingtimes)
            this.clokingtimes.sort(function(a,b){

              return new Date(a.time) - new Date(b.time);
            })
            console.log(this.clokingtimes)
            this.clokingtimes.forEach(post => {
              this.lineData[0].push(new Date(post.time).toLocaleDateString())
              this.lineData[1].push(new Date(post.time).getHours())
            })

            this.chartDataline.labels = this.lineData[0]

            this.chartDataline.datasets[0].data = this.lineData[1]
          });
    }
  },
  mounted: function() {
    console.log(this.currentUser.id)
    this.getWorkingTimes();
    this.getClokingTimes();
  }
}
</script>

<style scoped>
.chart-bar, .chart-pie, .chartlLine {
  max-width: 500px;
  margin: auto;
  padding: 30px 0 ;
}
</style>
