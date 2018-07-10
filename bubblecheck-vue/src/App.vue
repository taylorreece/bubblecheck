<template>
  <div>
    <div class="bubblecheck-layout mdl-layout mdl-js-layout mdl-layout--fixed-header">
      <bubblecheck-navbar />
      <bubblecheck-drawer />
      <!-- Main Content start -->
      <main class="mdl-layout__content">
        <router-view/>
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
      logged_in: false,
      user: null
    }
  },
  created () {
    axios.get('/api/user/current_user')
      .then(response => {
        this.user = response.data
        console.log(this.user)
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
</style>
