<template>
    <div>
        <fieldset>
            <legend class="doc">Log In</legend>
            <div class="row responsive-label">
                <div class="col-sm-12 col-md-3">
                    <label for="email">Email</label>
                </div>
                <div class="col-sm-12 col-md-7">
                    <input type="email" placeholder="Email" v-model="email"/>
                </div>
            </div>
            <div class="row responsive-label">
                <div class="col-sm-12 col-md-3">
                    <label for="password">Password</label>
                </div>
                <div class="col-sm-12 col-md-7">
                    <input type="password" placeholder="Password" v-model="password" @keyup.enter="submitLogin" />
                </div>
            </div>
            <div class="row">
                <div class="col-sm-12 col-md-7 col-md-offset-3">
                    <div class="spinner primary" v-if="loading"></div>
                    <button v-else v-on:click="submitLogin" class="primary">Sign In</button>
                </div>
            </div>
            <div class="row" v-if="error_text">
                <div class="col-sm-12 col-md-7 col-md-offset-3">
                    <mark class="secondary">{{ error_text }}</mark>
                </div>
            </div>
        </fieldset>
    </div>
</template>

<style>
</style>

<script>
import axios from 'axios'

export default {
  data () {
    return {
      loading: false,
      email: null,
      password: null,
      error_text: ''
    }
  },
  methods: {
    submitLogin: function () {
      this.loading = true
      var loginFormData = {
        'email': this.email,
        'password': this.password
      }
      axios.post('/api/user/login', loginFormData)
        .then(response => {
          location.reload()
        })
        .catch(error => {
          console.log(error)
          this.error_text = error.response.data
          this.loading = false
        })
    }
  }
}
</script>
