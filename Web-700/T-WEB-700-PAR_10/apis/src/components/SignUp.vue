<template>
  <div class="main signup-bloc">
    <h1 class="font">Sign Up</h1>
    <p class="text">Already have an account ? <a href="/#/account/signIn">Sign In</a></p>
    <form class="form-grid" id="signup" @submit.prevent="addUser">
      <input v-model="firstname" type="text" placeholder="First name" required />
      <input v-model="lastname" type="text" placeholder="Last name" required />
      <input v-model="email"  type="email" placeholder="Email" required />
      <div class="password-input">
        <input v-model="password" id="password" :type="showOldPassword ? 'text' : 'password'" placeholder="Password" style="" required />
        <img v-if="!showOldPassword" src="@/img/show.png" @click="toggleShowOldPassword" class="img-password"/>
        <img v-if="showOldPassword" src="@/img/hide.png" @click="toggleShowOldPassword" class="img-password"/>
      </div>
      <div class="password-input">
        <input id="password-confirm" :type="showNewPassword ? 'text' : 'password'" placeholder="Confirm password" style="" required />
        <img v-if="!showNewPassword" src="@/img/show.png" @click="toggleShowNewPassword" class="img-password"/>
        <img v-if="showNewPassword" src="@/img/hide.png" @click="toggleShowNewPassword" class="img-password"/>
      </div>
      <input class="create create-btn" type="submit" v-on:click="confirmPassword()" value="CREATE ACCOUNT">
      <div class="error" v-if="errorMessage">{{ errorMessage }}</div>
    </form>
  </div>
</template>

<script>
import axios from 'axios';
import '../../globalVars.css'
export default {
  name: 'SignUp',
  data() {
    return {
      errorMessage: "",
      currentUser: [],
      showOldPassword: false,
      showNewPassword: false,
    }
  },
  methods: {
    toggleShowOldPassword() {
      this.showOldPassword = !this.showOldPassword;
    },
    toggleShowNewPassword() {
      this.showNewPassword = !this.showNewPassword;
    },

    confirmPassword: function () {
      var pw1 = document.getElementById("password").value;
      var pw2 = document.getElementById("password-confirm").value;
      // console.log("PASSWORD ENTRE : " + pw1);
      // console.log("PASSWORD CONFIRME : " + pw2);

      if (pw1 != pw2) {
        this.errorMessage = "Password did not match"
        console.log("Variable d'erreur : " + this.errorMessage);
      }
      else {
        this.errorMessage = "";
        console.log("Variable d'erreur : " + this.errorMessage);
      }
    },

    addUser: function () {
      if (this.errorMessage === "Password did not match") {
        return;
      } else {
        axios
            .post('http://localhost:4000/register',
                {
                  "user": {
                    "email": this.email,
                    "password": this.password,
                    "firstname": this.firstname,
                    "lastname": this.lastname,
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
      }
      // alert(JSON.stringify(this.form))
    },

    connectUser: function () {
      // console.log(this.currentUser)

      axios
        .get('http://localhost:4000/login?email=' + this.email + '&password=' + this.password)
        .then((res) => {
          this.errorMessage = ""
          //faire en sorte de se connecter
          // console.log(res);
          this.currentUser = res.data.data

          // var test = [
          //   {name: "Maximillian", score: 1000},
          //   {name: "The second guy", score: 700},
          //   {name: "The newbie", score: 50},
          // ];
          //
          // localStorage.setItem("highscores", JSON.stringify(test));
          localStorage.globalCurrentUser = this.currentUser
          localStorage.setItem("globalCurrentUser", JSON.stringify(this.currentUser));
          // console.log(this.currentUser)
          // console.log(JSON.parse(localStorage.globalCurrentUser))
          this.$store.commit('DEFINE_USER', this.currentUser)
          if (res.status === 200) {
            this.$router.push({ path: '/' });
          }
        })
        .catch((err) => {
          // console.log("test")
          console.error(err)
          this.errorMessage = "Email or password is wrong"
        })
    }
  }
}
</script>

<style>

.password-confirm {
  width: 21%;
  margin-bottom: 40px;
}

.error {
  color: red;
  grid-column: 1 / 3;
}

.font {
  color: var(--yellow);
  font-weight: bold;
  font-family: "Kelly Slab";
  font-size: 30px;
}

.text {
  color: white;
}

.forgot a {
  color: white;
}

.login-btn .v-btn {
  border-radius: 10px;
}

.remember {
  width: 48vw;
  height: 30px;
  line-height: 30px;
  margin-left: 26vw;
  margin-bottom: 30px;
}

.remember a {
  margin-left: 15vw;
}

a.forgot {
  color: white;
}

.main.signup-bloc {
  min-height: calc(100vh - 252px);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding-bottom: 126px;
}

form.form-grid#signup input[type="email"], form.form-grid#signup input[type="submit"] {
  grid-column: 1 /3;
}

</style>
