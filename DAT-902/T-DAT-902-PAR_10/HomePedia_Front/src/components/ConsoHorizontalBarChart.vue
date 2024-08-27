<template>
  <div id="chart-container">
    <h2>Annual energy consumption by region</h2>
    <svg :width="width" :height="height"></svg>
    <p class="source">Source: <a href="https://odre.opendatasoft.com/">Open Data Soft</a></p>
  </div>
</template>

<script>
import * as d3 from 'd3';
import { defineComponent } from 'vue';
import axios from 'axios';

export default defineComponent({
  name: 'ConsommationAnnuelleBruteRegionaleChart',
  data() {
    return {
      width: 800,
      height: 500,
      margin: { top: 30, right: 30, bottom: 40, left: 200 },
      barColor1: '#66c2a5',
      barColor2: '#fc8d62',
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
      axios.get('https://odre.opendatasoft.com/api/explore/v2.1/catalog/datasets/consommation-annuelle-brute-regionale/records?limit=100')
        .then(response => {
          this.data = response.data.results.map(d => ({
            region: d.region,
            consommation_gaz: d.consommation_brute_gaz_totale || 0,
            consommation_electricite: d.consommation_brute_electricite_rte || 0
          }));
          this.data.sort((a, b) => b.consommation_gaz + b.consommation_electricite - (a.consommation_gaz + a.consommation_electricite));
          this.renderChart();
        })
        .catch(error => {
          console.error('Error fetching consumption data:', error);
        });
    },
    renderChart() {
      const svg = d3.select('svg')
        .attr('viewBox', `0 0 ${this.width} ${this.height}`)
        .append('g')
        .attr('transform', `translate(${this.margin.left},${this.margin.top})`);

      const x = d3.scaleLinear()
        .domain([0, d3.max(this.data, d => d.consommation_gaz + d.consommation_electricite)])
        .range([0, this.chartWidth]);

      const y = d3.scaleBand()
        .domain(this.data.map(d => d.region))
        .range([0, this.chartHeight])
        .padding(0.1);

      const tooltip = d3.select('body').append('div')
        .attr('class', 'tooltip')
        .style('position', 'absolute')
        .style('text-align', 'center')
        .style('width', 'auto')
        .style('height', 'auto')
        .style('padding', '5px')
        .style('font', '12px sans-serif')
        .style('background', 'lightsteelblue')
        .style('border', '0px')
        .style('border-radius', '8px')
        .style('pointer-events', 'none')
        .style('opacity', 0);

      svg.append('g')
        .selectAll('rect.gaz')
        .data(this.data)
        .join('rect')
        .attr('class', 'gaz')
        .attr('x', x(0))
        .attr('y', d => y(d.region))
        .attr('width', 0)
        .attr('height', y.bandwidth() / 2)
        .attr('fill', this.barColor1)
        .on('mouseover', function(event, d) {
          d3.select(this)
            .style('fill', d3.rgb('#66c2a5').darker(2));
          tooltip.transition()
            .duration(200)
            .style('opacity', .9);
          tooltip.html(`Region: ${d.region}<br>Gaz: ${d.consommation_gaz} kWh`)
            .style('left', (event.pageX + 5) + 'px')
            .style('top', (event.pageY - 28) + 'px');
        })
        .on('mouseout', function() {
          d3.select(this)
            .style('fill', '#66c2a5');
          tooltip.transition()
            .duration(500)
            .style('opacity', 0);
        })
        .transition()
        .duration(1000)
        .attr('width', d => x(d.consommation_gaz));

      svg.append('g')
        .selectAll('rect.electricite')
        .data(this.data)
        .join('rect')
        .attr('class', 'electricite')
        .attr('x', x(0))
        .attr('y', d => y(d.region) + y.bandwidth() / 2)
        .attr('width', 0)
        .attr('height', y.bandwidth() / 2)
        .attr('fill', this.barColor2)
        .on('mouseover', function(event, d) {
          d3.select(this)
            .style('fill', d3.rgb('#fc8d62').darker(2));
          tooltip.transition()
            .duration(200)
            .style('opacity', .9);
          tooltip.html(`Region: ${d.region}<br>electricity: ${d.consommation_electricite} kWh`)
            .style('left', (event.pageX + 5) + 'px')
            .style('top', (event.pageY - 28) + 'px');
        })
        .on('mouseout', function() {
          d3.select(this)
            .style('fill', '#fc8d62');
          tooltip.transition()
            .duration(500)
            .style('opacity', 0);
        })
        .transition()
        .duration(1000)
        .attr('width', d => x(d.consommation_electricite));

      svg.append('g')
        .call(d3.axisLeft(y));

      svg.append('g')
        .attr('transform', `translate(0, ${this.chartHeight})`)
        .call(d3.axisBottom(x).tickFormat(d => `${d / 1000} kWh`));
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
.tooltip {
  position: absolute;
  text-align: center;
  width: auto;
  height: auto;
  padding: 5px;
  font: 12px sans-serif;
  background: lightsteelblue;
  border: 0px;
  border-radius: 8px;
  pointer-events: none;
  opacity: 0;
}
</style>
