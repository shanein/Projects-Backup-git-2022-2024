<template>
  <div>
    <h1>Clock Manager</h1>
    <ul class="grid-liste">
      <li v-for="post in posts" :key="post.id">
        <div>Time : {{ post.time.replace('T', ' ') }}</div>
        <div>Status: {{ post.status }}</div>
        <div>Id : {{ post.id }}</div>
      </li>
    </ul>
    <form
        @submit.prevent="addClocking"
    >
      <p>
        <input
            id="time"
            v-model="time"
            type=datetime-local
            name="time"
            placeholder="Time"
            required
        >
      </p>

      <p>
        <input
            type="submit"
            value="Ajouter un Clocking time"
        >
      </p>

    </form>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      posts: [],
      EditPost: [],
      currentUser: this.$store.state.user,
    }
  },
  methods: {
    //get Workings
    getClocking: function() {
      axios
          .get("http://localhost:4000/api/clocks/" + this.currentUser.id)
          .then(response => {
            // console.log(response.data.data);
            // console.log(response.data.data.slice());
            this.posts = response.data.data.slice();
            console.log(this.$store.state.user)
            console.log(this.currentUser)

          });
    },

    //Add Worktime
    addClocking() {
      axios
          .post("http://localhost:4000/api/clocks/" + this.currentUser.id ,  {
            "clock":{
              "time":this.time + ":00",
              "user_id":this.currentUser.id.toString()
            }
          })
          .then(response => {
            // console.log(this.posts);
            // console.log(response.data.data);
            this.posts.push(response.data.data)
            // console.log(this.posts)
            console.log("test")
            console.log(this.time)
            console.log('2022-11-11 15:29')
            console.log('2022-11-11 15:29'.toString().replace(/.*(\d{2}:\d{2}:\d{2}).*/, "$1"))
          })
          .catch((err) => {
            console.log("testtt")
            console.error(err)

            console.log(this.currentUser.id.toString())
          })
    },
  },
  mounted: function() {
    console.log(this.currentUser.id)
    this.getClocking();
  }
};
</script>

<style scoped>
.grid-liste {
  display: grid;
  grid-gap: 10px;
  padding: 0;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
}
li {
  list-style-type: none;
  background-color: lightgrey;
}
</style>
