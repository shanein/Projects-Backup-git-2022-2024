<template>
  <svg ref="svg" class="external-wrapper extended" style=" width: 100vw"></svg>
  <p ref="info" class="utils"></p>
  <InfoSquare/>
</template>

<script>
/* eslint-disable */
import * as d3 from "d3"
import { mapState, mapActions } from "vuex"
import InfoSquare from "@/components/InfoSquare.vue"

export default {
  name: "Details Map",
  data() {
    return {
      current_post: "",
      isCustomSyle: true
    }
  },
  components:{
    InfoSquare
  },
  computed: {
    ...mapState(["regions"]),
  },
  async mounted() {
    this.$store.commit('MUTATE_CUSTOM_STYLE_STATUS', true)

    // let likePostalCode = this.$route.params.id + "*"
    let likePostalCode = this.$route.params.id
    this.processAndDraw(likePostalCode)
  },
  methods: {
    ...mapActions(['getData']),
    async processAndDraw(likePostalCode) {
      try {
        const geo_data = await this.getData(likePostalCode)
        const formattedData = geo_data.map(elt => {
          console.log(elt)
          console.log(elt.geoshape.coordinates)
          try {
            return {
              type: "Feature",
              properties: {
                CODE_DEPT: elt["code_dept"],
                NOM_DEPT: elt["nom_dept"],
                NOM_REGION: elt.nom_region,
                commune: elt["name"],
                nom_dept: elt["nom_dept"],
                nom_region: elt["nom_region"],
                superficie: elt["superficie"],
                population: elt["population"],
                CENTER: elt.geo_point_2d,
              },
              geometry: {
                type: "Polygon",
                coordinates: elt.geoshape.coordinates
              }
            }
          } catch (e) {
            console.error("here my error", e)
          }
        });

        const paths = await this.draw(formattedData)
        this.setupDragAndZoom(paths)
      } catch (e) {
        console.error(e)
      }
    },
    setupDragAndZoom(paths) {
      let svg = d3.select(this.$refs["svg"]);
      const g = svg.select("g")
      console.log("paths - g", paths, g)
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
    async draw(geo_data) {

      let svg = d3.select(this.$refs["svg"]);
      svg.attr("height", window.innerHeight)
        .attr("viewBox", [0, 0, window.innerWidth, window.innerHeight])
        .attr("width", window.innerWidth)

      const projection = this.getProjection(geo_data[0].properties.CENTER)
      const g = svg.append("g")

      const paths = g.selectAll('path')
        .data(geo_data, d => d.properties.ID_GEOFLA)
        .enter().append('path')
        .attr('fill', d => { const result = this.getColorAndRegion(d.properties["NOM_REGION"][0].toLowerCase()); return result.color })
        .attr('stroke', "black")
        .attr('d', projection)
        .on("mouseover", this.handleMouseOver)
        .on("mouseleave", this.handleMouseLeave)


      const height = g.node().getBBox().height
      const width = g.node().getBBox().width

      let rh = height / window.innerHeight
      let rw = width / window.innerWidth

      console.log(rh, rw)
      let ratio = Math.max(rh, rw)

      g.attr("transform", `translate(${window.innerWidth / 3}, ${window.innerHeight / 2})`)

      if (ratio > 0.5) {


        const [x, y] = [g.node().getBBox().x, g.node().getBBox().y]

        let twiker = 2
        if (y - window.innerHeight / 2 < 150) {
          twiker = 1.5
        } else if (y - window.innerHeight / 2 < 200) {
          twiker = 2
        } else if (y - (window.innerHeight / 2) > 150) {
          twiker = 3
        }
        g.attr("transform", `scale(${ratio, ratio}) translate(${window.innerWidth / 3}, ${window.innerHeight / twiker} )`)
      }
      return paths
    },
    getProjection({ lat, lon }) {
      var projection = d3.geoConicConformal()
        // .center([1.740805587691228, 48.95237177178076])
        .center([lon, lat])
        .scale(50000)
        .translate([0, 0]);

      return d3.geoPath().projection(projection);
    },
    handleMouseOver(e) {
      d3.select(e.target)
        .transition()
        .duration(200)
        .attr('fill', 'orange')
        .each(d => {
          console.log("Hello sa",d)
          d3.select(this.$refs["info"])
            .style("top", `${e.pageY}px`)
            .style("left", `${e.pageX}px`)
            .style('opacity', 1)
            .attr("display", "inline").text(d.properties["NOM_DEPT"])
            this.$store.commit('UPDATE_INFOSQUARE',d)
        })

    },
    getColorAndRegion(name) {
      let returnValue = {}
      for (const key in this.regions) {
        const oldRegions = this.regions[key].subpart.map(elt => elt.toLowerCase())
        if (oldRegions.includes(name.toLowerCase())) {
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
        .attr('fill', (d) => { const result = this.getColorAndRegion(d.properties["NOM_REGION"][0].toLowerCase()); return result.color });
      d3.select(this.$refs["info"]).style("opacity", 0)
      this.$store.commit('RESET_INFOSQUARE')
    },
  },
  unmounted() {
    this.$store.commit('MUTATE_CUSTOM_STYLE_STATUS', false)
  }
}
</script>

<style>

</style>
