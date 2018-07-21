<template>
    <footer>
        <p>&copy; 2014-{{ copywrite_year }}</p>
    </footer>
</template>

<style>
footer {
    position: fixed;
    bottom: 0;
    width: 100%;
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
