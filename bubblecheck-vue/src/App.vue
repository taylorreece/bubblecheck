<template>
  <div>
    <div class="bubblecheck-layout mdl-layout mdl-js-layout mdl-layout--fixed-header mdl-layout--fixed-drawer">
      <bubblecheck-navbar />
      <bubblecheck-drawer />
      <!-- Main Content start -->
      <main class="mdl-layout__content mdl-color--grey-100">
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
.bubblecheck-drawer {
    border: none;
}

/* iOS Safari specific workaround */
.bubblecheck-drawer .mdl-menu__container {
    z-index: -1;
}
.bubblecheck-drawer .bubblecheck-navigation {
    z-index: -2;
}
/* END iOS Safari specific workaround */

.bubblecheck-drawer .mdl-menu .mdl-menu__item {
    display: -webkit-flex;
    display: -ms-flexbox;
    display: flex;
    -webkit-align-items: center;
    -ms-flex-align: center;
    align-items: center;
}

.bubblecheck-navigation {
-webkit-flex-grow: 1;
    -ms-flex-positive: 1;
        flex-grow: 1;
}

.bubblecheck-layout .bubblecheck-navigation .mdl-navigation__link {
    display: -webkit-flex !important;
    display: -ms-flexbox !important;
    display: flex !important;
    -webkit-flex-direction: row;
    -ms-flex-direction: row;
    flex-direction: row;
    -webkit-align-items: center;
    -ms-flex-align: center;
    align-items: center;
    color: rgba(255, 255, 255, 0.56);
    font-weight: 500;
}

.bubblecheck-layout .bubblecheck-navigation .mdl-navigation__link:hover {
    background-color: #00BCD4;
    color: #37474F;
}

.bubblecheck-navigation .mdl-navigation__link .material-icons {
    font-size: 24px;
    color: rgba(255, 255, 255, 0.56);
    margin-right: 32px;
}
</style>
