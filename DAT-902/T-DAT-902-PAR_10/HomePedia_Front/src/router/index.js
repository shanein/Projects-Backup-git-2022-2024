import { createRouter, createWebHashHistory } from 'vue-router'
import SignIn from "@/components/SignIn";
import SignUp from "@/components/SignUp";
import EditProfile from '@/views/EditProfileView'
import News from '@/views/NewsView'
import EditPassword from "@/views/EditPasswordView";
import DetailsMap from '@/views/DetailsMap.vue';
import MapsView from '@/views/MapsView.vue';
import store from '../store';
// import jwt_decode from "jwt-decode"; // Importer le store Vuex
import { decodeJwt } from '@/jwtUtils';
import EnergyView from '@/views/EnergyView.vue';
import PopulationAndMarketView from "@/views/PopulationAndMarketView";

console.log(decodeJwt);


const routes = [
  {
    path: '/population-and-market',
    name: 'populationAndMarket',
    component: PopulationAndMarketView
  },
  {
    path: '/energy',
    name: 'energy',
    component: EnergyView
  },
  {
    path: '/account',
    name: 'account',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '@/views/AccountView.vue'),
    children: [
      // c'est aussi un itinéraire
      { path: 'signIn', component: SignIn },
      { path: 'signUp', component: SignUp }
    ],
  },
  /*{
    path: '/signin',
    name: 'signin',
    component: SignIn
  },*/
  {
    path: '/edit',
    name: 'edit',
    component: EditProfile
  },
  {
    path: '/edit-password',
    name: 'edit-password',
    component: EditPassword
  },
  {
    path: '/news/:id',
    name: 'news',
    component: News
  },
  {
    path: '/',
    name: 'maps',
    component: MapsView
  },
  {
    path: '/details/:id',
    name: 'detailsMap',
    component: DetailsMap
  },
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})


router.beforeEach(async (to, from, next) => {
  const accessToken = localStorage.getItem('access_token');
  const refreshToken = localStorage.getItem('refresh_token');

  if (accessToken) {
    const decodedToken = decodeJwt(accessToken);
    console.log(decodedToken)
    const currentTime = Date.now() / 1000;

    if (decodedToken.exp < currentTime && refreshToken) {
      console.log("token expired")
      // Token expiré, tenter de rafraîchir le token
      try {
        await store.dispatch('refreshToken');
        console.log("token refresh")
        next();
      } catch {
        store.dispatch('logout');
        next({ path: '/account/signIn' });
      }
    } else {
      next();
    }
  } else {
    console.log("no token")
    next();
  }
});

export default router
