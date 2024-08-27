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
import apiAuth from "@/auth";

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
    async updatePassword() {
      try {
        const response = await apiAuth.post('/password/',
              {
                  "token": this.currentUser.token,
                  "email": this.currentUser.email,
                  "old_password":this.oldpassword,
                  "new_password":this.newpassword
              })
            if (response.data) {
              if (response.status === 200 && response.data) {
                // console.log(res.data.data);
                this.successMessage = "Password updated"
                this.oldpassword = ""
                this.newpassword = ""
                // this.$router.push({ path: '/account' });
              } else if (response.data.errors[0].code === 400){
                console.log(response.data)
                this.errorMessage="Old Password Incorrect"
              } else {
                console.log(response.data.errors[0].message)
                this.errorMessage=response.data.errors[0].message
              }
            }
      } catch (err) {
          this.errorMessage=err.response.data.error
          console.log(this.errorMessage)
          console.error(err)
      }
    },
    toggleShowOldPassword() {
      this.showOldPassword = !this.showOldPassword;
    },
    toggleShowNewPassword() {
      this.showNewPassword = !this.showNewPassword;
    },
  },
  mounted() {
    if (!this.$store.state.user) {
      this.$router.push('/account/signIn');
    }
  }

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
