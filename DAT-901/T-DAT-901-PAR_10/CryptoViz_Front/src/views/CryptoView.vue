<template>
  <div class="page">

    <div class="coininfo">
      <div class="coin" v-if="coindata.market_data">
        <div class="coinrank">
          Rank #{{coindata.market_cap_rank}}
        </div>
        <div class="coinname" v-if="coindata.image.small">
          <div class="coinimage"><img :src="`${coindata.image.small}`" ></div>
          <h1>{{coindata.id}} <span>{{coindata.symbol}}</span></h1>
        </div>
        <div  class="coinprice">
          {{coindata.market_data.current_price.usd.toLocaleString("en-US", {style: "currency", currency: "USD"})}}
        </div>
      </div>
    </div>
    <div class="graph-bloc">
      <div class="dataButton">
        <button v-bind:class="getBtnClass(365)" v-on:click="updateData(365)">1y</button>
        <button v-bind:class="getBtnClass(7)" v-on:click="updateData(7)">7d</button>
        <button v-bind:class="getBtnClass(1)" v-on:click="updateData(1)">24h</button>
      </div>

      <div class="graph"></div>
      <div class="tab1"><div class="graph-sub" ref="chartdiv365" id="chartdiv365"></div></div>
      <div class="tab2"><div class="graph-sub" ref="chartdiv7" id="chartdiv7"></div></div>
      <div class="tab3"><div class="graph-sub" ref="chartdiv1" id="chartdiv1"></div></div>
    </div>

    <table class="cointable" v-if="coindata.market_data">
      <tr>
        <th>1h</th>
        <th>24h</th>
        <th>7d</th>
        <th>14d</th>
        <th>30d</th>
        <th>1y</th>
      </tr>
      <tr>
        <td :class="{ positive: coindata.market_data.price_change_percentage_1h_in_currency.usd > 0, negative: coindata.market_data.price_change_percentage_1h_in_currency.usd < 0 }">{{coindata.market_data.price_change_percentage_1h_in_currency.usd}} %</td>
        <td :class="{ positive: coindata.market_data.price_change_percentage_1y_in_currency.usd > 0, negative: coindata.market_data.price_change_percentage_24h_in_currency.usd < 0 }">{{coindata.market_data.price_change_24h_in_currency.usd}} %</td>
        <td :class="{ positive: coindata.market_data.price_change_percentage_7d_in_currency.usd > 0, negative: coindata.market_data.price_change_percentage_7d_in_currency.usd < 0 }">{{coindata.market_data.price_change_percentage_7d_in_currency.usd}} %</td>
        <td :class="{ positive: coindata.market_data.price_change_percentage_14d_in_currency.usd > 0, negative: coindata.market_data.price_change_percentage_14d_in_currency.usd < 0 }">{{coindata.market_data.price_change_percentage_14d_in_currency.usd}} %</td>
        <td :class="{ positive: coindata.market_data.price_change_percentage_30d_in_currency.usd > 0, negative: coindata.market_data.price_change_percentage_30d_in_currency.usd < 0 }">{{coindata.market_data.price_change_percentage_30d_in_currency.usd}} %</td>
        <td :class="{ positive: coindata.market_data.price_change_percentage_1y_in_currency.usd > 0, negative: coindata.market_data.price_change_percentage_1y_in_currency.usd < 0 }">{{coindata.market_data.price_change_percentage_1y_in_currency.usd}} %</td>
      </tr>
    </table>
  </div>
  <h2 v-if="this.$route.params.id != 'bitcoin'" :style="{ marginTop: '50px' }" >Comparison with bitcoin</h2>
  <chart-component :cryptoData="coinData" :bitcoinData="bitcoinData" v-if="this.$route.params.id != 'bitcoin'" class="bitcoincomparison"></chart-component>
</template>

<script>
import * as am5 from "@amcharts/amcharts5";
import * as am5xy from "@amcharts/amcharts5/xy";
import * as am5stock from "@amcharts/amcharts5/stock";
import ChartComponent from "@/components/dualchart.vue";

// import am5themes_Dark from '@amcharts/amcharts5/themes/Dark';
import axios from 'axios';
// import { isProxy, toRaw } from 'vue';

export default {
  name: 'CryptoView',
  components: {
    ChartComponent
  },
  data(){
    return{
      coindata :[],
      coinData: [],
      bitcoinData: [],
      selectedDuration: 365
    }
  },
  methods:{
    getCryptoApi: function() {
      const coin = this.$route.params.id
      console.log(coin)
      axios
      // .get("http://localhost:4000/cryptos/detail/"+coin)
      // .get("https://api.coingecko.com/api/v3/coins/"+coin)
      .get('http://127.0.0.1:8000/detail/?name=' + coin)
      .then(response => {
          console.log(response.data)
          this.coindata = response.data
      })
      .catch((err) => {
        console.error(err)
      })
    },
    getCryptoDataApi: function(length,idTemplate,timeunit,counted,showing,classcss) {
      // console.log(idTemplate)
    const coin = this.$route.params.id
      console.log(coin)
      var objdata = []
      axios
      .get("http://127.0.0.1:8000/variation/?name=" + coin + "&length=" + length)
      .then(response => {
          console.log(response.data)
          var coindata = response.data
          if (length === 1) {
            this.coinData = this.transformData(response.data);
          }
          for (let index = 0; index < coindata.length; index++) {
            var obj ={};
            obj["Date"] = coindata[index][0];
            obj["Close"] = coindata[index][4];
            obj["Open"] = coindata[index][1];
            obj["High"] = coindata[index][2];
            obj["Low"] = coindata[index][3];
            objdata.push(obj)
          }
          // console.log(objdata)
          if(showing == "hidden"){
            var chart = document.querySelector(classcss);
            chart.style.visibility = "hidden";
          }
          this.getCryptoGraph(objdata,idTemplate,timeunit,counted)
          if(showing == "hidden"){
            var chart2 = document.querySelector(classcss);
            chart2.style.display = "none";
          }
          if (coin !== 'bitcoin' && length === 1) {
            axios
                .get("http://127.0.0.1:8000/variation/?name=bitcoin&length=" + length)
                .then(response => {
                  console.log("bitcoin-first", response.data)
                  this.bitcoinData = this.transformData(response.data);
                })
                .catch((err) => {
                  console.error(err)
                })
            console.log("bitcoin", this.bitcoinData)
          }
      })
      .catch((err) => {
        console.error(err)
      })
      // console.log(objdata.length)
    },
    getCryptoGraph: function(data,idTemplate,timeunit,counted) {
      // console.log(idTemplate)
      //let data = toRaw(this.objdata)

      // let data = data2
      // console.log(data)
      // console.log(this.objdata)
      // Create root element
      // https://www.amcharts.com/docs/v5/getting-started/#Root_element
      var root = am5.Root.new(idTemplate);

      // Set themes
      // https://www.amcharts.com/docs/v5/concepts/themes/
      // root.setThemes([
      //   am5themes_Dark.new(root)
      // ]);

      // Create a stock chart
      // https://www.amcharts.com/docs/v5/charts/stock-chart/#Instantiating_the_chart
      var stockChart = root.container.children.push(am5stock.StockChart.new(root, {
      }));

      // Set global number format
      // https://www.amcharts.com/docs/v5/concepts/formatters/formatting-numbers/
      root.numberFormatter.set("numberFormat", "#,###.00");

      //
      // Main (value) panel
      //

      // Create a main stock panel (chart)
      // https://www.amcharts.com/docs/v5/charts/stock-chart/#Adding_panels
      var mainPanel = stockChart.panels.push(am5stock.StockPanel.new(root, {
        wheelY: "zoomX",
        panX: true,
        panY: true,
        height: am5.percent(70)
      }));

      // Create axes
      // https://www.amcharts.com/docs/v5/charts/xy-chart/axes/
      var valueAxis = mainPanel.yAxes.push(am5xy.ValueAxis.new(root, {
        renderer: am5xy.AxisRendererY.new(root, {opposite: true

        }),
        tooltip: am5.Tooltip.new(root, {}),
        numberFormat: "#,###.00",
        extraTooltipPrecision: 2
      }));

      var dateAxis = mainPanel.xAxes.push(am5xy.GaplessDateAxis.new(root, {
        baseInterval: {
          timeUnit: timeunit,
          count: counted
        },
        groupData: true,
        renderer: am5xy.AxisRendererX.new(root, {}),
        tooltip: am5.Tooltip.new(root, {})
      }));

      // Add series
      // https://www.amcharts.com/docs/v5/charts/xy-chart/series/
      var valueSeries = mainPanel.series.push(am5xy.CandlestickSeries.new(root, {
        name: "$",
        valueXField: "Date",
        valueYField: "Close",
        highValueYField: "High",
        lowValueYField: "Low",
        openValueYField: "Open",
        calculateAggregates: true,
        xAxis: dateAxis,
        yAxis: valueAxis,
        legendValueText: "{valueY}",
      }));
      valueSeries.data.setAll(data);

      // Set main value series
      // https://www.amcharts.com/docs/v5/charts/stock-chart/#Setting_main_series
      stockChart.set("stockSeries", valueSeries);

      // Add a stock legend
      // https://www.amcharts.com/docs/v5/charts/stock-chart/stock-legend/
      var valueLegend = mainPanel.plotContainer.children.push(am5stock.StockLegend.new(root, {
        stockChart: stockChart
      }));
      valueLegend.data.setAll([valueSeries]);
      valueLegend.settingsButtons.template.set("visible", false);


      // Add cursor(s)
      // https://www.amcharts.com/docs/v5/charts/xy-chart/cursor/
      mainPanel.set("cursor", am5xy.XYCursor.new(root, {
        yAxis: valueAxis,
        xAxis: dateAxis,
        snapToSeries: [valueSeries],
        snapToSeriesBy: "y!"
      }));


      // Add scrollbar
      // https://www.amcharts.com/docs/v5/charts/xy-chart/scrollbars/


    },
    updateData: function(days) {
      this.selectedDuration = days;

      var chart365 = document.querySelector(".tab1");
      var chart7 = document.querySelector(".tab2");
      var chart1 = document.querySelector(".tab3");

      if (days === 365) {
        chart365.style.display = "block";
        chart7.style.display = "none";
        chart1.style.display = "none";
      } else if (days === 7) {
        chart365.style.display = "none";
        chart7.style.display = "block";
        chart1.style.display = "none";
        chart7.style.visibility = "visible";
      } else if (days === 1) {
        chart365.style.display = "none";
        chart7.style.display = "none";
        chart1.style.display = "block";
        chart1.style.visibility = "visible";
      }
    },
    transformData: function(data) {
      return data.map((item) => {
        return {
          date: item[0],
          value: item[4]
        }
      });
    },
    getBtnClass: function(duration) {
      return {
        active: this.selectedDuration === duration
      }
    }


  },
  mounted() {
    this.getCryptoApi()
    this.getCryptoDataApi(7,"chartdiv7","hour",1,"hidden",".tab2")
    this.getCryptoDataApi(1,"chartdiv1","hour",0.1,"hidden",".tab3")
    this.getCryptoDataApi(365,"chartdiv365","day",2,"show",".tab1")
    // this.getCryptoGraph()
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  .graph-sub {
    height: 500px;
    margin: auto;
    background-color: transparent;
  }

  .coininfo{
    display: flex;
  }

  .coinname{
    color:var(--primary);
    display: flex;
    align-items: center;
    flex-direction: row;
    font-size: 40px;
    text-transform: capitalize;
  }

  .coinname h1 {
    font-size: 40px;
  }

  .coinname h1 span{
    font-size: 20px;
    font-weight: 400;
    text-transform: uppercase;
  }

  .coinprice {
    font-weight: 400;
    font-size: 30px;
    text-align: left;
    margin-top: 10px;
    color: var(--primary);
  }

  .coinimage img {
    width: 40px;
  }

  .coinsymbol{
    color: var(--backgroundColor);
  }

  .coinrank{
    color: var(--backgroundColor);
    font-weight: 700;
    padding: 5px 10px;
    font-size: 12px;
    text-align: left;
    background-color: var(--primary);
    position: relative;
    display: flex;
    width: max-content;
    border-radius: 28px;
    margin-bottom: 10px;
  }

  .coin{
    width: 100%;
  }

  .coinimage{
    margin-right: 10px;
    display: flex;
    align-items: center;
  }

  .page p{
    font-size: 25px;
    color: var(--primary);
  }

  div.tools{
    display: flex;
    flex-direction: row;
    width: 80%;
    margin: auto;
  }

  div.tools input.active{
    font-weight: bold;
  }

  .graph-bloc {
    position: relative;
  }

  .dataButton {
    display: flex;
    margin-left: auto;
    margin-bottom: 10px;
    width: max-content;
    z-index: 1;
    margin-right: 24px;
  }

  .dataButton button{
    background-color: transparent;
    border-radius: 25px;
    width: max-content;
    color: var(--primary);
    font-weight: bold;
    font-style: normal;
    padding: 5px 15px;
    font-size: 16px;
    height: max-content;
    border: 2px solid var(--primary);
    cursor: pointer;
    margin-right: 10px;
  }

  .dataButton > button:nth-child(3){
    margin-right: 0;
  }

  .dataButton button.active {
    background-color: var(--primary);
    color: var(--backgroundColor);
  }


  .positive {
    color: green;
  }

  .negative {
    color: red;
  }

  table.cointable {
    background-color: var(--primarylight);
    margin: 0;
    table-layout: fixed;
    margin-bottom: 10px;
    margin-top: 40px;
  }

  table.cointable td, table.cointable th {
    padding: 20px;
  }

  table.cointable th {
    font-weight: 700;
    text-align: center;
    background-color: var(--primarylight);
  }

  .bitcoincomparison {
    margin-bottom: 50px;
    margin-top: 20px;
  }
</style>
