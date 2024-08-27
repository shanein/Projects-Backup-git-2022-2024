<template>
  <div id="chart-container">
    <h2>Population of the Regions</h2>
    <svg :width="width" :height="height"></svg>
    <p class="source">Source: <a href="https://public.opendatasoft.com/">Open Data Soft</a></p>
  </div>
</template>

<script>
import * as d3 from 'd3';
import { defineComponent } from 'vue';
import api from "@/api";

export default defineComponent({
  name: 'PopulationHorizontalBarChart',
  data() {
    return {
      width: 800,
      height: 500,
      margin: { top: 30, right: 30, bottom: 40, left: 150 },
      barColor: '#163DC850',
      data: []
    };
  },
  computed: {
    chartWidth() {
      return this.width - this.margin.left - this.margin.right;
    },
    chartHeight() {
      return this.height - this.margin.top - this.margin.bottom;
    }
  },
  mounted() {
    this.fetchData();
  },
  methods: {
    fetchData() {
      api.post('/population/')
          .then(response => {
            this.data = response.data;
            this.data.sort((a, b) => b.population - a.population);
            this.renderChart();
          })
          .catch(error => {
            console.error('Error fetching population data:', error);
          });
    },
    renderChart() {
      const localeFr = d3.formatLocale({
        decimal: ",",
        thousands: " ",
        grouping: [3],
        currency: ["€", ""]
      });

      const formatNumber = localeFr.format(",.0f");

      const svg = d3.select('svg')
          .attr('viewBox', `0 0 ${this.width} ${this.height}`)
          .append('g')
          .attr('transform', `translate(${this.margin.left},${this.margin.top})`);

      const x = d3.scaleLinear()
          .domain([0, d3.max(this.data, d => d.population)])
          .range([0, this.chartWidth]);

      const y = d3.scaleBand()
          .domain(this.data.map(d => d.region))
          .range([0, this.chartHeight])
          .padding(0.1);

      svg.append('g')
          .selectAll('rect')
          .data(this.data)
          .join('rect')
          .attr('x', x(0))
          .attr('y', d => y(d.region))
          .attr('width', 0)
          .attr('height', y.bandwidth())
          .attr('fill', this.barColor)
          .transition() // Add transition for the animation
          .duration(1000) // Duration of the animation in milliseconds
          .attr('width', d => x(d.population));

      // Adding the title element separately
      svg.selectAll('rect')
          .data(this.data)
          .append('title')
          .text(d => `${d.region}: ${d.population.toLocaleString()}`);

      svg.append('g')
          .call(d3.axisLeft(y));

      svg.append('g')
          .attr('transform', `translate(0, ${this.chartHeight})`)
          .call(d3.axisBottom(x).tickFormat(d => `${formatNumber(d / 1000000)} M`));
    }
  }

});
</script>

<style scoped>
#chart-container {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}
svg {
  background-color: #f9f9f9;
}
p.source {
  margin-top: 5px;
  margin-left: auto;
}
</style>
