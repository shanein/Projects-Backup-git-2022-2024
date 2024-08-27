<template>
  <div class="main signin-bloc">
    <h1 class="font" style="margin-bottom: 20px">Update Password</h1>
    <form class="form-grid" @submit.prevent="updatePassword()" id="editpassword">
      <div class="password-input">
        <input v-model="oldpassword" :type="showOldPassword ? 'text' : 'password'" placeholder="Old Password" style="" required />
        <img v-if="!showOldPassword" src="@/img/show.png" @click="toggleShowOldPassword" class="img-password"/>
        <img v-if="showOldPassword" src="@/img/hide.png" @click="toggleShowOldPassword" class="img-password"/>
      </div>
      <div class="password-input">
        <input v-model="newpassword" :type="showNewPassword ? 'text' : 'password'" placeholder="New Password" style="" required />
        <img v-if="!showNewPassword" src="@/img/show.png" @click="toggleShowNewPassword" class="img-password"/>
        <img v-if="showNewPassword" src="@/img/hide.png" @click="toggleShowNewPassword" class="img-password"/>
      </div>
      <input class="create create-btn" type="submit" value="Update Password">
      <div v-if="errorMessage" class="error">{{ errorMessage }}</div>
      <div v-if="successMessage" class="success">{{ successMessage }}</div>
    </form>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      currentUser: this.$store.state.user,
      errorMessage: "",
      successMessage: "",
      showOldPassword: false,
      showNewPassword: false,
    }
  },
  methods: {
    updatePassword() {
      axios
          .put('http://localhost:4000/' + this.currentUser.id + '/password',
              {
                "user":{
                  "old_password":this.oldpassword,
                  "password":this.newpassword
                }
              })
          .then(res => {
            // localStorage.setItem("globalCurrentUser", JSON.stringify(this.EditUser));
            if (res.status === 200 && res.data.data) {
              // console.log(res.data.data);
              this.successMessage = "Password updated"
              this.oldpassword = ""
              this.newpassword = ""
              // this.$router.push({ path: '/account' });
            } else if (res.data.errors[0].code === 400){
              console.log(res.data)
              this.errorMessage="Old Password Incorrect"
            } else {
              console.log(res.data.errors[0].message)
              this.errorMessage=res.data.errors[0].message
            }
          })
          .catch((err) => {
            this.errorMessage="Incorrect old Password"
            console.log(this.errorMessage)
            console.error(err)
          })
    },
    toggleShowOldPassword() {
      this.showOldPassword = !this.showOldPassword;
    },
    toggleShowNewPassword() {
      this.showNewPassword = !this.showNewPassword;
    },
    mounted() {
      // console.log(test)
      if (this.$store.state.user.id == null) {
        this.$router.push('/account/signIn');
      }
    }
  },

}
</script>

<style>

.img-password {
  cursor: pointer;
}

#editpassword .error, #editpassword .success {
  grid-column: 1 / 2;
}

</style>
