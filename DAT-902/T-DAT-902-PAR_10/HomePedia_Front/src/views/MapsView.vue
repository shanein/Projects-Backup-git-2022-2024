<template>
  <div class="map">
    <svg ref="svg" class="external-wrapper extended"></svg>
    <p ref="info" class="utils"></p>
  </div>
</template>

<script>
/* eslint-disable */
import * as d3 from "d3"
import departments from '@/assets/departments.json'
import { mapState } from "vuex"



export default {
  data() {
    return {
      current_post: "",
      isCustomSyle: true
    }
  },
  async mounted() {
    this.$store.commit('MUTATE_CUSTOM_STYLE_STATUS', true)

    const paths = this.draw(departments.features)
    this.setupDragAndZoom(paths)
  },
  computed: {
    ...mapState(["regions"])
  },
  methods: {
    draw(geo_data) {
      let svg = d3.select(this.$refs["svg"]);
      svg.attr("height", window.innerHeight)
        .attr("viewBox", [0, 0, window.innerWidth, window.innerHeight])
        .attr("width", window.innerWidth)

      const projection = this.getProjection()
      const g = svg.append("g")
        .attr("transform", `translate(${window.innerWidth / 2}, ${window.innerHeight / 2})`);

      const paths = g.selectAll('path')
        .data(geo_data)
        .enter().append('path')
        .attr('fill', d => { const result = this.getColorAndRegion(d.properties["NOM_REGION"]);console.log(d, result); return result.color })
        .attr('stroke', "black")
        .attr('d', projection)
        .on("mouseover", this.handleMouseOver)
        .on("mouseleave", this.handleMouseLeave)
        .on("click", this.goToPage)

      return paths
    },
    goToPage(event, d) {
      this.$router.push({name: 'detailsMap', params: {id: d.properties["CODE_DEPT"]}})
    },
    setupDragAndZoom(paths) {
      let svg = d3.select(this.$refs["svg"]);
      const g = svg.select("g")
      const drag = d3.drag()
        .on("start", function (event) {
          const [x, y] = d3.pointer(event, svg.node());
          try {
            const transform = g.attr("transform").match(/-?\d+\.?\d*/g)?.map(Number);
            event.subject.offsetX = (x - transform[0])
            event.subject.offsetY = (y - transform[1])
          } catch (e) {
            console.error(e)
          }
        })
        .on("drag", function (event) {
          const [x, y] = d3.pointer(event, svg.node());
          g.attr("transform", `translate(${x - event.subject.offsetX}, ${y - event.subject.offsetY})`);
        });

      paths.call(drag);

      paths.call(d3.zoom()
        .extent([[0, 0], [window.innerWidth, window.innerHeight]])
        .scaleExtent([1, 8])
        .on("zoom", ({ transform }) => {
          paths.attr("transform", transform)
          paths.attr("stroke-width", 1 / transform.k);
          this.$store.commit('UPDATE_ZOOM_LEVEL', Math.floor(transform.k))
        }));

    },
    getProjection() {
      var projection = d3.geoConicConformal()
        .center([2.454071, 46.279229])
        .scale(5000)
        .translate([0, 0]);

      return d3.geoPath().projection(projection);
    },
    handleMouseOver(e) {
      d3.select(e.target)
        .transition()
        .duration(200)
        .attr('fill', 'orange')
        .each(d => {
          d3.select(this.$refs["info"])
            .style("top", `${e.pageY}px`)
            .style("left", `${e.pageX + 15}px`)
            .style('opacity', 0)
            .transition()
            .duration(500)
            .style("top", `${e.pageY}px`)
            .style("left", `${e.pageX}px`)
            .style('opacity', 1)
            .attr("display", "inline").text(d.properties["NOM_DEPT"])
        })

    },
    getColorAndRegion(name) {
      console.log(name)
      name = name.toLowerCase()
      let returnValue = {}
      for (const key in this.regions) {
        const oldRegions = this.regions[key].subpart.map(elt => elt.toLowerCase())
        if (oldRegions.includes(name)) {
          returnValue = { name: key, color: this.regions[key].color }
          break;
        }
      }
      return returnValue
    },
    handleMouseLeave(e) {
      d3.select(e.target)
        .transition()
        .duration(200)
        .attr('fill', (d) => { const result = this.getColorAndRegion(d.properties["NOM_REGION"]); return result.color });
      d3.select(this.$refs["info"]).style("opacity", 0)
    },
  },
  unmounted() {
    this.$store.commit('MUTATE_CUSTOM_STYLE_STATUS', false)
  }
}
</script>

<style>
.custom-main {
  margin: 0 !important;
  margin-top: 74px !important;;
  /*background-color: blueviolet !important;*/
  width: 100vw;
  height: 100vh;
  max-width: max-content;
  padding: 0;
  margin: 0;
}

.mybut {
  position: absolute;
  top: 500px;
  left: 0;
}

.utils {
  position: absolute;
  opacity: 0;
  padding: 5px;
  background-color: rgb(29, 184, 223);
}
</style>
