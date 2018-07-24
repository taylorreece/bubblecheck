<template>
    <div>
        <fieldset>
            <legend class="doc">Register</legend>
            <div class="row responsive-label">
                <div class="col-sm-12 col-md-3">
                    <label for="email">Email</label>
                </div>
                <div class="col-sm-12 col-md-7">
                    <input type="email" placeholder="Email Address" v-model="email" />
                </div>
            </div>
            <div class="row responsive-label">
                <div class="col-sm-12 col-md-3">
                    <label for="teachername">Teacher Name</label>
                </div>
                <div class="col-sm-12 col-md-7">
                    <input type="text" placeholder="e.g. Mrs. Smith" v-model="teachername" />
                </div>
            </div>
            <div class="row responsive-label">
                <div class="col-sm-12 col-md-3">
                    <label for="password">Password</label>
                </div>
                <div class="col-sm-12 col-md-7">
                    <input type="password" placeholder="Password" v-model="password"/>
                </div>
            </div>
            <div class="row responsive-label">
                <div class="col-sm-12 col-md-3">
                    <label for="repeatpassword">Repeat Password</label>
                </div>
                <div class="col-sm-12 col-md-7">
                    <input type="password" placeholder="Password again" v-model="repeatpassword"/>
                </div>
            </div>
            <div class="row">
                <div class="col-sm-12 col-md-7 col-md-offset-3">
                    <div class="spinner primary" v-if="loading"></div>
                    <button v-else v-on:click="submitRegistration" class="primary">Register</button>
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
      repeatpassword: null,
      teachername: null,
      error_text: ''
    }
  },
  methods: {
    submitRegistration: function () {
      this.loading = true
      var registrationFormData = {
        'email': this.email,
        'teachername': this.teachername,
        'password': this.password,
        'repeatpassword': this.repeatpassword
      }
      axios.post('/api/user/register', registrationFormData)
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
