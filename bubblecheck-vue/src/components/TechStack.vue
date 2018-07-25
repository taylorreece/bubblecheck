<template>
    <table class="hoverable softwareattributions">
        <caption>Software that powers BubbleCheck</caption>
        <thead>
            <tr>
            <th>Name</th>
            <th>Purpose</th>
            <th>WebSite</th>
            </tr>
        </thead>
        <tbody>
            <tr
                v-for="technology in technologies"
                v-bind:key="technology.name">
                <td data-label="Name">{{ technology.name }}</td>
                <td data-label="Purpose">{{ technology.purpose }}</td>
                <td data-label="Website"><a :href="technology.website">{{ technology.website }}</a></td>
            </tr>
        </tbody>
    </table>
</template>

<style>
table.softwareattributions {
    max-height: unset;
}
</style>

<script>
export default {
  data () {
    return {
      technologies: [
        {
          'name': 'Flask',
          'purpose': 'Website Backend API',
          'website': 'http://flask.pocoo.org/'
        },
        {
          'name': 'Flutter',
          'purpose': 'Cross-platform mobile app framework',
          'website': 'https://flutter.io/'
        },
        {
          'name': 'mini.css',
          'purpose': 'CSS Framework',
          'website': 'https://minicss.org/'
        },
        {
          'name': 'OpenCV',
          'purpose': 'Exam image processing',
          'website': 'https://opencv.org/'
        },
        {
          'name': 'SQLAlchemy',
          'purpose': 'Database ORM',
          'website': 'http://www.sqlalchemy.org/'
        },
        {
          'name': 'Vue JS',
          'purpose': 'Front-end HTML and JavaScript',
          'website': 'https://vuejs.org/'
        }
      ]
    }
  }
}
</script>
