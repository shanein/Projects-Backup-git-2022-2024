import { createRouter, createWebHistory } from 'vue-router'
// import HomeView from '../views/HomeView.vue'
import User from "@/components/User";
import WorkingTimes from "@/components/WorkingTimes";
import ClockManager from "@/components/ClockManager";
import chartManager from "@/components/ChartManager";

const routes = [
  {
    path: '/',
    name: 'Accueil',
    component: User
  },
  { path: '/workingTimes/:id', name:'worktimes', component: WorkingTimes },
  { path: '/clock/:name', name:'clockmanager', component: ClockManager },
  { path: '/chartManager/:id', name:'chartManager', component: chartManager },

  // {
  //   path: '/workingTimes/' + this.stor.state.user,
  //   name: 'workingtimes',
  //   component: WorkingTimes
  //   // route level code-splitting
  //   // this generates a separate chunk (about.[hash].js) for this route
  //   // which is lazy-loaded when the route is visited.
  //   // component: () => import(/* webpackChunkName: "about" */ '../views/about.vue')
  // }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
