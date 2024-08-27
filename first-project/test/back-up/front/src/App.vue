<template>
  <img alt="Vue logo" src="./assets/logo.png">
<!--  <HelloWorld msg="Welcome to Your Vue.js App"/>-->
  <User />
  <WorkingTimes />
  <WorkingTime />
  <ClocKManager />
  <ChartManager />
</template>

<script>
// import HelloWorld from './components/HelloWorld.vue'
import User from "@/components/User";
import WorkingTimes from "@/components/WorkingTimes";
import WorkingTime from "@/components/WorkingTime";
import ClocKManager from "@/components/ClocKManager";
import ChartManager from "@/components/ChartManager";

export default {
  name: 'App',
  components: {
    ChartManager,
    ClocKManager,
    WorkingTime,
    HelloWorld,
    User,
    WorkingTimes,
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
