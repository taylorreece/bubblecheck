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
            <div class="row">
                <div class="col-sm-12 col-md-3">
                    <label for="numSections"># of Sections</label>
                </div>
                <div class="col-sm-12 col-md-7">
                    <select name="numSections">
                        <option v-for="n in 15">{{ n }}</option>
                    </select>
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
    </div>
</template>

<script>
// import axios from 'axios'
export default {
  data () {
    return {
      loading: false,
      name: null,
      numSections: 5,
      error_text: ''
    }
  },
  methods: {
    submitCourseAdd: function () {
      console.log(this.name)
    }
  }
}
</script>
