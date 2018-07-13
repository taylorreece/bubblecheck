<template>
    <div>
        Course id {{ $route.params.courseid }}
        {{ course }}
    </div>
</template>

<script>
import axios from 'axios'

export default {
  data () {
    return {
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
      axios.get('/api/course/' + this.$route.params.courseid)
        .then(response => {
          this.course = response.data
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
