<template>
  <nav>
    <router-link to="/">Home</router-link>
    <router-link v-if="this.$store.state.user.id" :to="{ name: 'worktimes', params: {id : this.$store.state.user.id}  }">Workingtimes</router-link>
    <router-link v-if="this.$store.state.user.id" :to="{ name: 'clockmanager', params: {name : this.$store.state.user.username}  }">ClockManager</router-link>
    <router-link v-if="this.$store.state.user.id" :to="{ name: 'chartManager', params: {id : this.$store.state.user.id}  }">ChartManager</router-link>

    <!--    {{this.currentUser.id}}-->
  </nav>
  <router-view/>
</template>





<!--<template>-->
<!--  <img alt="Epitech logo" src="./assets/logo.png" height="100">-->
<!--  <User/>-->
<!--  <WorkingTimes v-if="this.$store.state.user.id"/>-->
<!--  <WorkingTime v-if="this.$store.state.user.id"/>-->
<!--  <ClocKManager  v-if="this.$store.state.user.id"/>-->
<!--  <ChartManager  v-if="this.$store.state.user.id"/>-->
<!--</template>-->

<script>
// import User from "@/components/User";
// import WorkingTimes from "@/components/WorkingTimes";
// import WorkingTime from "@/components/WorkingTime";
// import ClocKManager from "@/components/ClockManager";
// import ChartManager from "@/components/ChartManager";


export default {
  name: 'App',
  // components: {
  //   ChartManager,
  //   ClocKManager,
  //   WorkingTime,
  //   User,
  //   WorkingTimes,
  // },
  data() {
      return {
        // currentUser: this.$store.state.user,
        // id: this.currentUser.toString()
      }
  },
  methods: {
    // increment() {
    //   // this.$store.commit('increment')
    //   this.$store.state = 2
    //   console.log(this.$store.state.count)
    // },
    // defineUser() {
    //   this.$store.state = ["test"]
    //   console.log(this.$store.state.user)
    // }
  },
  mounted() {
    if (localStorage.globalCurrentUser) {
      this.$store.commit('DEFINE_USER', JSON.parse(localStorage.globalCurrentUser))
      // this.currentUser = this.$store.state.user
    }
    // console.log(this.currentUser.id)


  }
}
//
// var vm = new Vue({
//   data: {
//     a: 1
//   }
// })




</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

nav {
  padding: 30px;
}

nav a {
  font-weight: bold;
  color: #2c3e50;
}

nav a.router-link-exact-active {
  color: #42b983;
}
</style>


