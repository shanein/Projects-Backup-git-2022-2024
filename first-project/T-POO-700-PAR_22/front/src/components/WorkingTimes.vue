<template>
  <div>
    <!-- Modal -->
    <div class="modal fade" id="exampleModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h2 class="modal-title fs-5" id="exampleModalLabel" >Modifier le Worktime {{EditPost['id']}}</h2>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close">           </button>
          </div>
          <div class="modal-body">
            <form
                @submit.prevent="editWorkTime(EditPost['id'])"
            >
              <p>
                <input
                    id="editstart"
                    v-model="EditPost['start']"
                    type=datetime-local
                    name="editstart"
                    placeholder="Start"
                    required
                >
              </p>

              <p>
                <input
                    id="editend"
                    v-model="EditPost['end']"
                    type=datetime-local
                    name="editend"
                    placeholder="End"
                    required
                >
              </p>

              <p>
                <input
                    type="submit"
                    value="Modifier le Worktime"
                >
              </p>

            </form>
          </div>
<!--          <div class="modal-footer">-->
<!--            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>-->
<!--          </div>-->
        </div>
      </div>
    </div>

    <h1>Working Times</h1>
    <ul class="grid-liste">
      <li v-for="post in posts" :key="post.id">
          <h2>UserId {{this.currentUser.id}}</h2>
          <div>Start : {{ post.start.replace('T', ' ') }}</div>
          <div>End : {{ post.end.replace('T', ' ') }}</div>
          <div>Id : {{ post.id }}</div>
          <div v-on:click="deleteWorkingTimes( post.id )">-</div>
        <button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#exampleModal" v-on:click="EditPost = this.posts[this.posts.map(post => post.id).indexOf(post.id)]">
          Modifier
        </button>
      </li>
    </ul>
    <form
        @submit.prevent="addWorkTime"
    >
      <p>
        <input
            id="start"
            v-model="start"
            type=datetime-local
            name="start"
            placeholder="Start"
            required
        >
      </p>

      <p>
        <input
            id="end"
            v-model="end"
            type=datetime-local
            name="end"
            placeholder="End"
            required
        >
      </p>

      <p>
        <input
            type="submit"
            value="Ajouter un Worktime"
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
    getWorkingTimes: function() {
      axios
        .get("http://localhost:4000/api/workingtimes/" + this.currentUser.id)
        .then(response => {
          // console.log(response.data.data);
          // console.log(response.data.data.slice());
          this.posts = response.data.data.slice();
          console.log(this.$store.state.user)
          console.log(this.currentUser)

        });
    },

    //Delete Working
    deleteWorkingTimes: function(id) {
      axios
          .delete("http://localhost:4000/api/workingtimes/" + id)
          .then(() => {
            // console.log("http://localhost:4000/api/workingtimes/" + id);
            let i = this.posts.map(post => post.id).indexOf(id) // find index of your object
            this.posts.splice(i, 1) // remove it from array
          });
    },

    //Add Worktime
    addWorkTime() {
      console.log(this.start)
      console.log(this.end)
      axios
          .post("http://localhost:4000/api/workingtimes/" + this.currentUser.id ,  {
            "workingtime": {
              "start":this.start,
              "end":this.end,
              "user_id":this.currentUser.id.toString()
            }
          })
          .then(response => {
            // console.log(this.posts);
            // console.log(response.data.data);
            this.posts.push(response.data.data)
            // console.log(this.posts)
            console.log("test")
            console.log(this.test)
          });
    },


    //Edit Worktime
    editWorkTime(idEditWord) {
      console.log(this.start)
      console.log(this.end)
      axios
          .put("http://localhost:4000/api/workingtimes/" + idEditWord, {
            "workingtime": {
              "start":this.EditPost['start'],
              "end":this.EditPost['end'],
              "user_id":this.currentUser.id.toString()
            }
          })
          .then(response => {
            // console.log(this.posts);
            console.log(response.data.data);
            // this.posts.push(response.data.data)
            // console.log(this.posts)
            console.log(this.EditPost['start'])
            console.log(this.EditPost['end'])
            console.log(idEditWord)
            // this.EditPost = []
            // console.log(localStorage.globalCurrentUser)
            // console.log(localStorage.getItem("globalCurrentUser").username)

          })
          .catch((err) => {
            console.error(err)
            console.log(this.EditPost['start'])
            console.log(this.EditPost['end'])
            console.log(idEditWord)
          })
    }
  },
  mounted: function() {
      console.log(this.currentUser.id)
      this.getWorkingTimes();
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
