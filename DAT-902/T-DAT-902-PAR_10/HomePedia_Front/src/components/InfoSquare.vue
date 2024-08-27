<template>
      <div id="info_square">
        <h1>Commune name : {{ infoSquare.commune}}</h1>
        <p class="nom_dept">nom_dept: {{ lowerCaseFirst(infoSquare.nom_dept) }}</p>
        <p class="nom_region">nom_region: {{ formattedRegion }}</p>
        <p class="superficie">superficie: {{ formattedSuperficie }}</p>
        <p class="population">population: {{ formattedPopulation }}</p>
        <p class="superficie">Densité: {{ formattedDensity }}</p>
    </div>

</template>
<script>
  import { mapGetters } from 'vuex';
  export default {
    name:"InfoSquare",
    data(){
      return {
        current_post: ""
      }
    },
    mounted() {

  
    },
    computed: {
      ...mapGetters(["infoSquare"]),
    formattedSuperficie() {
      const formatted = this.infoSquare.superficie ? (this.infoSquare.superficie * 0.01).toFixed(2) + ' km²' : '... ...';
      return formatted
    },
    formattedPopulation() {
      const formatted = this.infoSquare.population ? this.infoSquare.population  + ' pers' : '... ...';
      return formatted
    },
    formattedDensity() {
      if (this.infoSquare.population && this.infoSquare.superficie) {
        return (this.infoSquare.population * 1000000 / this.infoSquare.superficie * 0.01).toFixed(2) + ' pers/km²';
      }
      return '... ...';
    },
    formattedRegion(){
      if (this.infoSquare.nom_region) {
        return this.infoSquare.nom_region[0]
      }
      return '... ...';
    } 
    },
    methods: {
      lowerCaseFirst(str) {
      return str ? str[0].toLowerCase() + str.slice(1) : '... ...';
    }
    },
  };
  </script>
    
  <style>
  #info_square {
  backdrop-filter: blur(10px) saturate(200%);
  -webkit-backdrop-filter: blur(10px) saturate(200%);
  background-color: rgba(255, 255, 255, 0.45);
  border-radius: 12px;
  border: 1px solid rgba(209, 213, 219, 0.3);
  padding: 20px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  max-width: 400px;
  margin: auto;
  font-family: 'Arial', sans-serif;
  color: #333;
  text-align: center;
  background-color: #EEEEEE;
  position: absolute;
  right: 5px;
  top: 10vh;
  text-align: left;
  height: 80vh;
  width: 15vw;
}

#info_square h1 {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 10px;
}

#info_square p {
  font-size: 18px;
  margin: 5px 0;
}

.nom_dept, .nom_region, .superficie, .population {
  font-weight: 500;
}

.nom_dept::before, .nom_region::before, .superficie::before, .population::before {
  content: '• ';
  color: #007BFF;
}

  </style>
