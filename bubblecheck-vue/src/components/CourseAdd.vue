<template>
    <div>
        <fieldset>
            <legend class="doc">Add Course</legend>
            <div class="row responsive-label">
                <div class="col-sm-12 col-md-3">
                    <label for="name">Course Name</label>
                </div>
                <div class="col-sm-12 col-md-7">
                    <input type="text" placeholder="e.g. World History" v-model="name"/>
                </div>
            </div>
            <div class="row responsive-label">
                <div class="col-sm-12 col-md-3">
                    <label for="numSections"># of Sections</label>
                </div>
                <div class="col-sm-12 col-md-7">
                    <select name="numSections" v-model.number="numSections">
                        <option v-for="n in maxSections" :key="n">{{ n }}</option>
                    </select>
                </div>
            </div>
            <div class="row" v-for="m in (1, numSections)" :key="m">
                <div class="col-sm-12 col-md-7 col-md-offset-3">
                    <input
                        type="text"
                        @keyup.enter="submitCourseAdd"
                        v-model="sections[m-1]"
                        :placeholder="'Section '+m + ' name'" />
                </div>
            </div>
            <div class="row">
                <div class="col-sm-12 col-md-7 col-md-offset-3">
                    <div class="spinner primary" v-if="loading"></div>
                    <button v-else v-on:click="submitCourseAdd" class="primary">Add Course</button>
                </div>
            </div>
            <div class="row" v-if="error_text">
                <div class="col-sm-12 col-md-7 col-md-offset-3">
                    <mark class="secondary">{{ error_text }}</mark>
                </div>
            </div>
        </fieldset>
        {{ sections.slice(0, numSections) }}
    </div>
</template>

<script>
import axios from 'axios'

export default {
  data () {
    return {
      loading: false,
      name: null,
      numSections: 3,
      maxSections: 15,
      sections: [ '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '' ],
      error_text: ''
    }
  },
  methods: {
    submitCourseAdd: function () {
      if (this.loading) {
        console.log('Already submitting.')
        return
      }
      this.loading = true
      var submitData = {
        'name': this.name,
        'sections': this.sections.slice(0, this.numSections)
      }
      axios.post('/api/course/add', submitData)
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
