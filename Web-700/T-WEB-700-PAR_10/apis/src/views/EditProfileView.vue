<template>
    <div class="edit-bloc">
      <form class="form-grid form-edit" @submit.prevent="editUser">
        <div class="edit-profile">
            <div class="icon-user-big">
              <img v-if="this.$store.state.user.profile_picture" v-bind:src="'data:image/jpeg;base64,'+ currentUser.profile_picture"  style="object-fit: contain" />
              <img v-else src="@/assets/user-icon.png"/>
            </div>
            <div style="padding: 5px 30px;display: flex;align-items: center">
                <!--<input type="file">

                <button @click="chooseFiles()"
                    style="background-color: var(--yellow); padding: 5px 25px; color:black; border-radius: 15px">Import
                    image</button>-->
<!--                <label for="file-upload" class="custom-file-upload"-->
<!--                    style="background-color: var(&#45;&#45;yellow); padding: 5px 25px; color:black; border-radius: 15px">-->
<!--                    Import image-->
<!--                </label>-->
                <vue-base64-file-upload
                class="v1"
                accept="image/png,image/jpeg"
                image-class="v1-image"
                placeholder="Import image"
                input-class="v1-input"
                disable-preview="true"
                :max-size="customImageMaxSize"
                @size-exceeded="onSizeExceeded"
                @file="onFile"
                @load="onLoad" />
<!--                <input v-on="chooseFiles" id="file-upload" type="file" hidden />-->
            </div>
            <div>
                <a href="javascript:void(0)" v-on:click="deleteImgUser()"><img src="@/img/Trash.svg" style="width:2vw;margin-top: 5px" /></a>
            </div>
        </div>
        <input v-model="EditUser.firstname" type="text" placeholder="First name" style="" required />
        <input v-model="EditUser.lastname" type="text" placeholder="Last name" style="" required />
        <input v-model="EditUser.email" type="email" placeholder="Email" required />
        <a href="/#/edit-password" class="link-yellow" style="text-align: right">Update Password</a>
<!--        <input v-model="password" type="password" placeholder="password" style="width:21%; margin-right: 30px" required />-->
<!--        <input type="text" placeholder="Confirm password" style="width:21%; margin-bottom: 40px" required /><br />-->
        <input class="create create-btn" type="submit" value="SAVE">
        <div v-if="errorMessage">{{ errorMessage }}</div>
      </form>
    </div>
</template>

<script>
import axios from "axios";
import VueBase64FileUpload from 'vue-base64-file-upload';

export default {
  components: {
    VueBase64FileUpload
  },

  data() {
      return {
        currentUser: this.$store.state.user,
        errorMessage: "",
        EditUser: this.$store.state.user,
        customImageMaxSize: 3,
        dataimage: ""
      }
  },
  methods: {
    onFile(file) {
      console.log(file); // file object
    },

    onLoad(dataUri) {
      console.log(dataUri.substring(dataUri.indexOf(',') + 1)); // data-uri string
      this.dataimage = dataUri.substring(dataUri.indexOf(',') + 1)
      this.currentUser.profile_picture = this.dataimage
      this.$store.commit('DEFINE_USER', this.currentUser)
    },

    onSizeExceeded(size) {
      alert(`Image ${size}Mb size exceeds limits of ${this.customImageMaxSize}Mb!`);
    },

    editUser() {
      axios
          .put('http://localhost:4000/' + this.currentUser.id + '/profile',
              {
                "user": {
                  "email": this.email,
                  "firstname": this.firstname,
                  "lastname": this.lastname,
                  "profile_picture": this.dataimage,
                }
              })
          .then(response => {
            // localStorage.setItem("globalCurrentUser", JSON.stringify(this.EditUser));
            this.currentUser = this.EditUser
            this.currentUser.profile_picture = this.dataimage
            this.$store.commit('DEFINE_USER', this.currentUser)

            localStorage.setItem("globalCurrentUser", JSON.stringify(this.currentUser));



            // console.log(this.posts);
            // console.log(response.data.data);
            // this.posts.push(response.data.data)
            // console.log(this.posts)
            // console.log(this.EditUser)
            // console.log(JSON.parse(localStorage.globalCurrentUser))
            if (response.status === 200) {
              this.$router.push({ path: '/account' });
            }
          })
          .catch((err) => {
            console.error(err)
            console.log(this.EditUser.username)
            console.log(this.EditUser.email)
            console.log(this.EditUser.id)
          })
    },

    deleteImgUser() {
      this.dataimage = ""
      this.currentUser.profile_picture = this.dataimage
      this.$store.commit('DEFINE_USER', this.currentUser)
    }
  },


  mounted() {
    // console.log(test)
    if (this.$store.state.user.id == null) {
      this.$router.push('/account/signIn');
    }
  }
}
</script>

<style>
/*img.v1-image {*/
/*  display: none;*/
/*}*/

input[type="file"] {
  background-color: var(--yellow);
  color:black;
  border-radius: 15px;
  margin: 0;
  display: flex;
  position: relative;
  height: inherit;
  padding: 5px 0px;
  cursor: default !important;
}

input.v1-input {
  background-color: var(--yellow);
  color: black !important;
  border-radius: 15px;
  text-align: center;
  height: inherit;
  padding: 5px 0px;
  margin: 0;
  cursor: default !important;
  font-weight: 400;
}

input.v1-input::placeholder {
  color: black;
  opacity: 1;
}

.link-yellow {
  color: var(--yellow);
}

.edit-profile {
  display: flex;
  align-items: center;
}

form.form-grid.form-edit {
  width: initial;
  margin: 0;
  grid-template-columns: 1fr 1fr;
}

form.form-grid.form-edit > * {
  grid-column: 1 / 3;
}

form.form-grid.form-edit > input[type="text"] {
  grid-column: initial;
}

.edit-bloc {
  padding-top: 50px;
}
</style>
