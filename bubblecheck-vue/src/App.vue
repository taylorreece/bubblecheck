<template>
  <div>
    <bubblecheck-navbar v-bind:user="user" v-bind:courses="courses" />
    <div class="row">
      <div class="col-md-4 col-lg-3">
        <bubblecheck-drawer v-bind:user="user" v-bind:courses="courses" />
      </div>
      <div class="col-md-8 col-lg-9">
        <router-view/>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'App',
  data () {
    return {
      user: null,
      courses: null,
      flash_messages: null
    }
  },
  created () {
    axios.get('/api/user/flash_messages')
      .then(response => {
        this.flash_messages = response.data
      })
      .catch(error => {
        console.log(error)
      })
    axios.get('/api/user/current_user')
      .then(response => {
        this.user = response.data
        axios.get('/api/course/list')
          .then(courseResponse => {
            this.courses = courseResponse.data.courses
          })
      })
      .catch(error => {
        console.log(error)
      })
  }
}
</script>

<style>
</style>
