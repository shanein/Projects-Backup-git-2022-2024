<template>
  <header>
    <nav>
      <div class="logo">
        <router-link to="/">
          <img alt="Apis logo" src="@/assets/logo.png">
        </router-link>
      </div>
      <div class="leftnav">
        <div class="menu">
          <router-link class="menu_option" active-class="active" to="/">Cryptocoins</router-link>
          <router-link class="menu_option" active-class="active" to="/news/all">News</router-link>
          <router-link class="menu_option" active-class="active" to="/news-administration" v-if="this.$store.state.user.role == 'admin'">News-administration</router-link>
        </div>
        <div class="account user-icon">
          <router-link v-if="this.$store.state.user.id == null" to="/account/signIn"><img alt="userIcon"
              src="@/assets/user-icon.png"></router-link>
          <router-link v-else to="/account">
            <img v-if="this.$store.state.user.profile_picture" v-bind:src="'data:image/jpeg;base64,'+ $store.state.user.profile_picture"  style="width:50px;height:50px;object-fit: contain" />
            <img v-else alt="userIcon" src="@/assets/user-icon.png">
          </router-link>
          <!--      <router-link to="/account" v-if="this.$store.state.user.id == null"><img alt="userIcon" src="@/assets/user-icon.png"></router-link>-->
        </div>
      </div>
    </nav>
  </header>
  <main>
    <router-view />
  </main>
</template>
<script>
export default {
  name: 'App',
  data() {
    return {

    }
  },
  methods: {

  },
  mounted() {
    if (localStorage.globalCurrentUser) {
      this.$store.commit('DEFINE_USER', JSON.parse(localStorage.globalCurrentUser))
    }
    // console.log(this.$store.state.user)
  }
}


</script>

<style>
@import url('https://fonts.cdnfonts.com/css/kelly-slab');
@import url('https://fonts.googleapis.com/css?family=Montserrat:400,500,700');

#app {
  font-family: Montserrat, Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  /*color: #2c3e50;*/
}

body {
  background-color: black;
  padding: 0;
  margin: 0;
  color: white;
}

h1 {
  margin: 0;
}

div.logo {
  float: left;
  margin: 0;
  padding: 10px;
}



div.menu {
  margin: 0;
  margin-right: 10px;
}

div.account {
  margin: 0;
  display: flex;
  margin-right: 10px;
}

a.active {
  color: var(--yellow) !important;
}

a.menu_option {
  color: white;
  text-decoration: none;
  margin: 10px;
  font-size: large;
  font-family: 'Kelly Slab', sans-serif;
}

nav {
  display: flex;
}

div.leftnav {
  margin-left: auto;
  display: flex;
  justify-content: center;
  align-items: center;
  margin-left: auto;
  padding: 10px;
}

main {
  width: 90%;
  max-width: 1440px;
  margin: auto;
  padding-top: 126px;
}

header {
  position: fixed;
  width: 100%;
  background-color: black;
  border-bottom: 1px solid hsla(0,0%,100%,0.16);
  z-index: 999;
}

input {
  background-color: black;
  border: solid 1px var(--yellow);
  color: var(--yellow);
  font-style: italic;
  padding: 15px 20px;
  font-size: 16px;
  font-family: Montserrat, Avenir, Helvetica, Arial, sans-serif;
}

input::placeholder {
  opacity: 60%;
  color: var(--yellow);
}

input[type="checkbox"] {
  -webkit-appearance: checkbox;
  -moz-appearance: checkbox;
  appearance: checkbox;
  display: inline-block;
  width: 20px;
  height: 20px;
  accent-color: var(--yellow);
}

label {
  color: white;
  font-size: .875rem;
  margin-top: -20px;
  height: auto;
}

a {
  font-weight: bold;
  color: var(--yellow);
  text-decoration: none;
}

form.form-grid {
  display: grid;
  width: 50%;
  margin-top: 10px;
  grid-gap: 30px;
}

.email {
  background-color: black;
  border: solid 1px #FFD600;
  color: #FFD600;
  font-style: italic;
  font-size: 15px;
}

/*input[type="submit"] {*/
/*  background: linear-gradient(to right, var(--yellow), var(--yellowDark));*/
/*  border-radius: 25px;*/
/*  color: black;*/
/*  font-weight: bold;*/
/*  font-style: normal;*/
/*  padding: 10px 40px;*/
/*  font-size: 22px;*/
/*  height: inherit;*/
/*  margin: auto;*/
/*  cursor: pointer;*/
/*}*/

input[type="submit"] {
  background: var(--yellow);
  border-radius: 25px;
  color: black;
  font-weight: bold;
  font-style: normal;
  padding: 10px 30px;
  font-size: 22px;
  height: inherit;
  background: linear-gradient(to left, var(--yellowDark) 10%, var(--yellow) 50%);
  background-size: 200% 100%;
  background-position: left bottom;
  transition: all .3s ease-out;
  margin: auto;
  cursor: pointer;
}

input[type="submit"]:hover {
  background-position: right bottom;
}

.user-icon img{
  max-width: 50px;
}
</style>




