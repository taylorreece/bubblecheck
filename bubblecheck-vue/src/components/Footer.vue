<template>
    <footer>
        <p>&copy; 2014-{{ copywrite_year }} Bubblecheck
          | <i class="material-icons">android</i>Android App
          | <i class="material-icons">phone_iphone</i>iOS App
          | <router-link :to="'TechStack'">Tech Stack</router-link>
        </p>
    </footer>
</template>

<style>
footer {
    position: fixed;
    bottom: 0;
    width: 100%;
}
footer p {
   vertical-align: middle;
}
footer p i.material-icons {
  font-size: 1rem;
}
</style>

<script>
export default {
  data () {
    return {
      copywrite_year: null
    }
  },
  created () {
    var dt = new Date()
    this.copywrite_year = dt.getFullYear()
  }
}
</script>
