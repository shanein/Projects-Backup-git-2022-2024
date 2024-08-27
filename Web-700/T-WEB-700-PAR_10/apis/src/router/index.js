import { createRouter, createWebHashHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import SignIn from "@/components/SignIn";
import SignUp from "@/components/SignUp";
import EditProfile from '@/views/EditProfileView'
import News from '@/views/NewsView'
import EditPassword from "@/views/EditPasswordView";
import NewsAdministration from '@/views/NewsAdministrationView'




const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  // {
  //   path: '/:id',
  //   name: 'CryptoView',
  //   // route level code-splitting
  //   // this generates a separate chunk (about.[hash].js) for this route
  //   // which is lazy-loaded when the route is visited.
  //   component: () => import(/* webpackChunkName: "about" */ '../views/CryptoView.vue')
  // },
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
    path: '/one_news/:currency/:id',
    name: 'one_news',
    component: () => import(/* webpackChunkName: "about" */ '@/views/OneNewsView.vue')
  },
  {
    path: '/news-administration',
    name: 'news-administration',
    component: NewsAdministration
  },
  {
    path: '/:id',
    name: 'CryptoView',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '@/views/CryptoView.vue')
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router
