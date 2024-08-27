<template>
  <h1>User</h1>
  <div>

    <!-- Modal -->
    <div class="modal fade" id="ModalUser" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h2 class="modal-title fs-5" id="exampleModalLabel">Modifier le user {{EditUser.id}}</h2>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close">           </button>
          </div>
          <div class="modal-body">
            <form
                @submit.prevent="editUser()"
            >
              <div>
                <input v-model="EditUser.username" type="text" placeholder="username" required/>
              </div>
              <div>
                <input v-model="EditUser.email" type="email" placeholder="email" required/>
              </div>
              <div>
                <input v-model="EditUser.password" type="password" placeholder="password" required/>
              </div>
              <p>
                <input
                    type="submit"
                    value="Modifier le User"
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

    <div v-if="currentUser.id == null">
      <h2>Inscription</h2>
      <form
          id="inscription"
          @submit.prevent="addUser">
        <div>
          <input v-model="username" type="text" placeholder="username" required/>
        </div>
        <div>
          <input v-model="email" type="email" placeholder="email" required/>
        </div>
        <div>
          <input v-model="password" type="password" placeholder="password" required/>
        </div>
        <p>
          <input
              type="submit"
              value="Creer un Utilisateur"
          >
        </p>
      </form>
    </div>

    <div v-if="currentUser.id == null">
      <h2>Connexion</h2>
      <form
          id="connexion"
          @submit.prevent="connectUser">
        <div>
          <input v-model="identifier" type="text" placeholder="identifier" required/>
        </div>
        <div>
          <input v-model="password" type="password" placeholder="password" required/>
        </div>
        <p>
          <input
              type="submit"
              value="Se connecter"
          >
        </p>
      </form>
    </div>

    <div>
      <h2>Suppression d'un User</h2>
      <form
          id="connexion"
          @submit.prevent="deleteUser">
        <div>
          <input v-model="id" type="number" placeholder="User id" required/>
        </div>
        <p>
          <input
              type="submit"
              value="Supprimer l'utilisateur"
          >
        </p>
      </form>
    </div>
    <div v-if="currentUser.id">
      <div >Connecté en tant que {{ currentUser.username }} id : {{ currentUser.id}} email :  {{ currentUser.email}} </div>
      <a href="/" onclick="localStorage.clear();" >Déconnexion</a>
      <button v-if="currentUser.id" type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#ModalUser" >
        Modifier
      </button>
    </div>
    <div v-if="errorMessage">Erreur : {{ errorMessage }}</div>
  </div>

</template>

<script>

import axios from 'axios';

// export let data =  {
//   user: {
//     username:"",
//     email:""
//   }
// }

export default {
  data() {
    if (localStorage.globalCurrentUser) {
      return {
        currentUser: JSON.parse(localStorage.globalCurrentUser),
        errorMessage: "",
        EditUser: JSON.parse(localStorage.globalCurrentUser),
        value: localStorage.globalCurrentUser
      }
    } else {
      return {
        currentUser: [],
        errorMessage: "",
        EditUser: [],
        value: localStorage.globalCurrentUser
      }
    }
  },
  methods: {

    connectUser: function () {
      console.log(this.currentUser)
      if (!this.identifier) {
        this.identifier = this.email ? this.email : this.username
      }

      axios
          .post('http://localhost:4000/api/users/login',
              {
                "user": {
                  "identifier": this.identifier,
                  "password": this.password
                }
              })
          .then((res) => {
            this.errorMessage = ""
            //faire en sorte de se connecter
            console.log(res);
            this.currentUser = res.data.data[0]

            // var test = [
            //   {name: "Maximillian", score: 1000},
            //   {name: "The second guy", score: 700},
            //   {name: "The newbie", score: 50},
            // ];
            //
            // localStorage.setItem("highscores", JSON.stringify(test));
            // localStorage.globalCurrentUser = this.currentUser
            localStorage.setItem("globalCurrentUser", JSON.stringify(this.currentUser));
            console.log(this.currentUser)
            console.log(JSON.parse(localStorage.globalCurrentUser))
            this.EditUser = this.currentUser
            this.$store.commit('DEFINE_USER', this.currentUser)
          })
          .catch((err) => {
            console.error(err)
            this.errorMessage = err.message
          })
    },

    addUser: function () {

      axios
          .post('http://localhost:4000/api/users/',
              {
                "user": {
                  "username": this.username,
                  "email": this.email,
                  "password": this.password
                }
              })
          .then((res) => {
            //faire en sorte de se connecter
            console.log(res);
            this.errorMessage = ""
            this.connectUser()
          })
          .catch((err) => {
            console.error(err)
            this.errorMessage = err.message
          })
      // alert(JSON.stringify(this.form))
    },

    deleteUser: function () {

      axios
          .delete('http://localhost:4000/api/users/' + this.id)
          .then((res) => {
            //faire en sorte de se connecter
            console.log(res);
            this.errorMessage = ""
            if (this.id == this.currentUser.id) {
              console.log("id pareil")
              localStorage.clear();
              location.reload()
            }
          })
          .catch((err) => {
            console.error(err)
            this.errorMessage = err.message
          })
    },

    editUser() {
      axios
          .put('http://localhost:4000/api/users/' + this.currentUser.id,
              {
                "user": {
                  "username": this.EditUser.username,
                  "email": this.EditUser.email,
                  "password": this.EditUser.password
                }
              })
          .then(response => {
            localStorage.setItem("globalCurrentUser", JSON.stringify(this.EditUser));
            this.currentUser = this.EditUser
            this.$store.commit('DEFINE_USER', this.currentUser)

            // console.log(this.posts);
            console.log(response.data.data);
            // this.posts.push(response.data.data)
            // console.log(this.posts)
            console.log(this.EditUser.username)
            console.log(this.EditUser.email)
            console.log(this.EditUser.id)
          })
          .catch((err) => {
            console.error(err)
            console.log(this.EditUser.username)
            console.log(this.EditUser.email)
            console.log(this.EditUser.id)
          })
    }

    // createUser : {
    //   mounted() {
    //     axios
    //         .post('http://localhost:4000/api/users')
    //         .then((res) => {
    //           console.log(res);
    //         })
    //   }
    // },
    // getUser : {
    //   mounted() {
    //     axios
    //         .get('http://localhost:4000/api/users/{id}')
    //         .then((res) => {
    //           console.log(res);
    //         })
    //   }
    // },
    // updateUser : {
    //   mounted() {
    //     axios
    //         .put('http://localhost:4000/api/users/{id}')
    //         .then((res) => {
    //           console.log(res);
    //         })
    //   }
    // },
    // deleteUser : {
    //   mounted() {
    //     axios
    //         .delete('http://localhost:4000/api/users/{id}')
    //         .then((res) => {
    //           console.log(res);
    //         })
    //   }
    // }
  }
}


</script>
<!-- filename: User.vue -->
<style scoped>

</style>
