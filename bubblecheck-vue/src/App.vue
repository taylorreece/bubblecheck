<template>
  <div>
    <div class="bubblecheck-layout mdl-layout mdl-js-layout mdl-layout--fixed-header mdl-layout--fixed-drawer">
      <bubblecheck-navbar v-bind:user="user" v-bind:courses="courses" />
      <bubblecheck-drawer v-bind:user="user" v-bind:courses="courses" />
      <!-- Main Content start -->
      <main class="mdl-layout__content">
        <router-view/>
        {{ flash_messages }} <!-- TODO: make these messages better -->
      </main>
      <!-- Main Content End -->
    </div> <!-- End bubblecheck-layout -->
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
        console.log(error.response.data)
        console.log(error.response.status)
        console.log(error.response.headers)
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
        console.log(error.response.data)
        console.log(error.response.status)
        console.log(error.response.headers)
      })
  }
}
</script>

<style>
.bubblecheck-navigation {
-webkit-flex-grow: 1;
    -ms-flex-positive: 1;
        flex-grow: 1;
}
.mdl-layout__content {
  padding: 16px;
}
</style>
