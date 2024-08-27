// store/index.js
// import axios from 'axios';
import api from "@/api";
import { createStore } from 'vuex'

// const zoomLevel = {
//   1: "ZONE",
//   2: "REGION",
//   4: "DEPARTEMENTS",
//   8: "COMMUNES"
// }

const store = createStore({
  state: {
    user: JSON.parse(localStorage.getItem('globalCurrentUser')) || null,
    accessToken: localStorage.getItem('access_token') || '',
    refreshToken: localStorage.getItem('refresh_token') || '',
    news: [],
    articles: [],
    isCustom: false,
    zoomLevel: "",
    infoSquare: {
      "commune": null,
      "nom_dept": null,
      "nom_region": null,
      "superficie": null,
      "population": null,
    },
    regions : {
      "ile-de-france": { subpart: ["ile-de-France"], color: "#03AED2"},
      "bourgogne-franche-comté": { subpart: ["bourgogne", "franche-comte"], color:"#7776B3"},
      "bretagne": { subpart: ["bretagne"], color: "#FDDE55"},
      "centre-val de loire": { subpart: ["centre"], color: "#615EFC"},
      "corse": { subpart: ["corse"], color: "#F3CA52", code_postal: [20]},
      "grand est": { subpart: ["alsace", "lorraine", "champagne-ardenne"], color: "#F6E9B2" },
      "hauts-de-france": { subpart: ["Nord-Pas-De-Calais", "Picardie"], color: "#0A6847" },
      "auvergne-rhone-alpes": { subpart: ["rhone-alpes", "auvergne"], color: "#7aBa78" },
      "normandie": { subpart: ["haute-normandie", "basse-normandie"], color: "#028391" },
      "nouvelle-aquitaine": { subpart: ["aquitaine", "poitou-charentes", "limousin"], color: "#C39898" },
      "occitanie": { subpart: ["midi-pyrenees", "languedoc-roussillon"], color: "#808836" },
      "pays de la loire": { subpart: ["paysdelaLoire"], color: "#FFA27F" },
      "provence-Alpes-Côte d'azur": { subpart: ["provence-alpes-coted'azur"], color: "#254336" }
    }
  },
  getters: {
    isAuthenticated: state => !!state.accessToken,
    custom: state => state.isCustom,
    region: state => state.regions,
    infoSquare: state => state.infoSquare

  },
  mutations: {
    DEFINE_USER(state, payload) {
      state.user = payload;
      state.accessToken = payload.access;
      state.refreshToken = payload.refresh;
      localStorage.setItem('access_token', payload.access);
      localStorage.setItem('refresh_token', payload.refresh);
      localStorage.setItem('globalCurrentUser', JSON.stringify(state.user));
    },
    CLEAR_AUTH(state) {
      state.user = null;
      state.accessToken = '';
      state.refreshToken = '';
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      localStorage.removeItem('globalCurrentUser');
    },
    MUTATE_CUSTOM_STYLE_STATUS(state, payload){
      state.isCustom = payload
    },
    UPDATE_ZOOM_LEVEL(state, payload){
      state.zoomLevel = payload
    },
    UPDATE_INFOSQUARE(state, payload){
      console.log(payload)
      state.infoSquare["commune"] = payload.properties["commune"]
      state.infoSquare["nom_dept"] = payload.properties["nom_dept"]
      state.infoSquare["nom_region"] = payload.properties["nom_region"]
      state.infoSquare["superficie"] = payload.properties["superficie"]
      state.infoSquare["population"] = payload.properties["population"]
    },
    RESET_INFOSQUARE(state){
      state.infoSquare["commune"] = null
      state.infoSquare["nom_dept"] = null
      state.infoSquare["nom_region"] = null
      state.infoSquare["superficie"] = null
      state.infoSquare["population"] = null
    }
  },
  actions: {
    async getData(context, likePostalCode){
      let arrayOfResults = null
      try{
        const url = `https://127.0.0.1:8000/get_communes_by_department/?department_code=${likePostalCode}`
        console.log(url)
        let response = await fetch(url)

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const result = await response.json();
        console.log("result", result)

        arrayOfResults = result || []
        console.log(arrayOfResults)
      }catch(e){
        console.error("An Error occur while fetching data:", e)
      }
      return arrayOfResults

    },

    async refreshToken({ state, commit }) {
      try {
        const response = await api.post('/api/token/refresh/', {
          refresh: state.refreshToken,
        });
        commit('DEFINE_USER', {
          ...state.user,
          access: response.data.access,
        });
      } catch (error) {
        commit('CLEAR_AUTH');
        throw error;
      }
    },
    logout({ commit }) {
      commit('CLEAR_AUTH');
    },
  },
});

export default store;
