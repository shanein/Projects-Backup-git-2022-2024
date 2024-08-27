<template>
    <div ref="chartdiv" style="width: 100%; height: 500px;"></div>
  </template>
  
  <script>
  import * as am5 from "@amcharts/amcharts5";
  import * as am5xy from "@amcharts/amcharts5/xy";
  import am5themes_Animated from "@amcharts/amcharts5/themes/Animated";
  import {charAt} from "core-js/internals/string-multibyte";
  
  export default {
    name: 'DualChart',
    props: {
      cryptoData: Array,
      bitcoinData: Array
    },
    watch: {
    bitcoinData() {
        if (this.root) {
          this.root.dispose();
        }
        this.$nextTick(() => {
          this.initChart();
        });
      },
    },
    mounted() {
    },
    methods: {
      initChart() {
        console.log("cryptoData", this.cryptoData);
        console.log("bitcoinData", this.bitcoinData);
        const root = am5.Root.new(this.$refs.chartdiv);
  
        root.setThemes([am5themes_Animated.new(root)]);
  
        const chart = root.container.children.push(am5xy.XYChart.new(root, {
            focusable: true,
            panX: true,
          panY: true,
          wheelX: "panX",
          wheelY: "zoomX",
          pinchZoomX: true
        }));
  
        const xAxis = chart.xAxes.push(am5xy.DateAxis.new(root, {
          maxDeviation: 0.1,
          groupData: false,
          baseInterval: {
            timeUnit: "minute",
            count: 30
          },
          renderer: am5xy.AxisRendererX.new(root, {})
        }));
  
        // Série pour la première cryptomonnaie
        this.createAxisAndSeries(root, chart, xAxis, this.cryptoData, charAt(this.$route.params.id).toUpperCase() + this.$route.params.id.slice(1), "#FF0000");
  
        // Série pour Bitcoin
        this.createAxisAndSeries(root, chart, xAxis, this.bitcoinData, "Bitcoin", "#0000FF");

        const cursor = am5xy.XYCursor.new(root, {});
        cursor.lineY.set("stroke", am5.color("#FF0000")); // Ajuster si nécessaire
        cursor.lineX.set("stroke", am5.color("#0000FF")); // Ajuster si nécessaire
        chart.set("cursor", cursor);

        chart.set("scrollbarX", am5.Scrollbar.new(root, {}));

        this.root = root; // Stocker la référence à root pour la nettoyer plus tard
      },
      createAxisAndSeries(root, chart, xAxis, data, name, color) {
        console.log("data", data);
        const yAxis = chart.yAxes.push(am5xy.ValueAxis.new(root, {
          renderer: am5xy.AxisRendererY.new(root, { opposite: data === this.bitcoinData })
        }));

        // Modifier la couleur des axes et des étiquettes
        yAxis.get("renderer").labels.template.setAll({
          fill: am5.color(color)
        });

        const series = chart.series.push(am5xy.LineSeries.new(root, {
          name: name,
          xAxis: xAxis,
          yAxis: yAxis,
          valueYField: "value",
          valueXField: "date",
          stroke: am5.color(color),
          tooltip: am5.Tooltip.new(root, {
            labelText: "{name}: {valueY}"
          })
        }));

        let tooltip = am5.Tooltip.new(root, {
          getFillFromSprite: false,
          labelText: "[bold]{name}[/]\n$ {valueY}",
          autoTextColor: false,
        });

        tooltip.get("background").setAll({
          fill: am5.color(color),
        });

        tooltip.label.setAll({
          fill: am5.color(0xffffff)
        });

        series.set("tooltip", tooltip);

        series.data.setAll(data);
      }
    },
    beforeUnmount() {
      if (this.root) {
        this.root.dispose();
      }
    }
  }
  </script>
  
  <style scoped>
  #chartdiv {
    width: 100%;
    height: 500px;
  }
  </style>
