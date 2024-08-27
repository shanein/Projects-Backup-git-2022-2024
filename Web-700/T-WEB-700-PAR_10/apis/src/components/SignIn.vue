<template>
  <div class="main signin-bloc">
    <h1 class="font">Sign In</h1>
    <p class="text">Don't have an account ? <a href="/#/account/signUp">Create your account</a></p>
    <form class="form-grid" id="signin" @submit.prevent="connectUser">
      <input class="email" v-model="email" type="email" placeholder="Email" required />
      <div class="password-input">
        <input class="password" v-model="password" :type="showPassword ? 'text' : 'password'" placeholder="Password" required />
        <img v-if="!showPassword" src="@/img/show.png" @click="toggleShowPassword" class="img-password"/>
        <img v-if="showPassword" src="@/img/hide.png" @click="toggleShowPassword" class="img-password"/>
      </div>
      <input class="login login-btn" type="submit" value="LOGIN">
      <div v-if="errorMessage" class="error">{{ errorMessage }}</div>
    </form>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'SignIn',
  data() {
    return {
      errorMessage: "",
      currentUser: [],
      showPassword: false,
    }
  },
  methods: {
    connectUser: function () {
      // console.log(this.currentUser)

      axios
        .get('http://localhost:4000/login?email=' + this.email + '&password=' + this.password)
        .then((res) => {
          if (res.data.data) {
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
          } else {
            this.errorMessage = "Email or password is wrong"
          }

        })
        .catch((err) => {
          // console.log("test")
          console.error(err)
          this.errorMessage = "Email or password is wrong"
        })
    },
    toggleShowPassword() {
      this.showPassword = !this.showPassword;
    },
  }
}
</script>

<style>
.font {
  color: #FFD600;
  font-weight: bold;
  font-size: 30px;
}

.text {
  color: white;
  font-size: 18px;
}

.forgot a {
  color: white;
}

label {
  color: white;
  margin-top: -20px;
  height: auto;
}

.remember label {
  color: white;
  font-size: 18px;
}

::placeholder {
  color: #FFD600;
  margin-left: 10px;
}

.remember {
  width: 40vw !important;
  font-size: 18px;
  margin-left: 25vw !important;
}

.remember a {
  margin-left: 15vw;
}

a.forgot {
  color: white;
}

.password-input input {
  width: calc(100% - 30px);
}

img.img-password {
  position: absolute;
  right: 20px;
}

.password-input {
  display: flex;
  align-items: center;
  position: relative;
}

.main.signin-bloc {
  min-height: calc(100vh - 252px);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding-bottom: 126px;
}

#signin .error {
  grid-column: 1 / 2;
}
</style>
