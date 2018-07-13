<template>
    <div>
        <span v-if="loading">Loading...</span>
        <div v-else>
            Course id {{ $route.params.courseid }}
            {{ course }}
        </div>
    </div>
</template>

<script>
import axios from 'axios'

export default {
  data () {
    return {
      loading: true,
      course: null
    }
  },
  created () {
    this.fetchCourseData()
  },
  watch: { // call again the method if the route changes
    '$route': 'fetchCourseData'
  },
  methods: {
    fetchCourseData () {
      this.loading = true
      axios.get('/api/course/' + this.$route.params.courseid)
        .then(response => {
          this.course = response.data
          this.loading = false
        })
        .catch(error => {
          console.log(error.response.data)
          console.log(error.response.status)
          console.log(error.response.headers)
        })
    }
  }
}
</script>
