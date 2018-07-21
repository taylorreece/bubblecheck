<template>
  <div class="bubblecheck-page">
    <bubblecheck-navbar v-bind:user="user" v-bind:courses="courses" />
    <div class="row">
      <input type="checkbox" id="drawer-control" class="drawer">
      <div class="col-md-3 col-lg-3 bubblecheck-drawer">
        <bubblecheck-sidebar v-bind:user="user" v-bind:courses="courses" />
      </div>
      <div class="col-md-9 col-lg-9 col-sm-12">
        <router-view/>
      </div>
    </div>
    <bubblecheck-footer />
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
.bubblecheck-drawer {
  border: 0px !important;
}
.responsive-label {
    align-items:center
}
.responsive-label div input {
    width: 100%;
}
@media (min-width: 768px) {
    .responsive-label .col-md-3{text-align:right}
}
</style>
