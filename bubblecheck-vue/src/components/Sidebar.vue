<template>
    <!-- Drawer start -->
    <nav>
        <span v-if="user"><i class="material-icons">person</i>{{ this.$parent.user.teachername }}</span>
        <router-link v-if="user" to="/dashboard"><i class="material-icons">dashboard</i>Dashbard</router-link>
        <label for="drawer-control" class="drawer-close"></label>
        <router-link v-if="user==null" to="/login"><i class="material-icons">computer</i>Log in</router-link>
        <router-link v-if="user==null" to="/register"><i class="material-icons">ballot</i>Register</router-link>
        <span v-if="user">Courses</span>
        <router-link
            v-for="course in courses"
            v-bind:key="course.id"
            class="sublink-1"
            :to="{ name: 'course', params: { courseid: course.id }}">
            <i class="material-icons">school</i>{{ course.name }}
        </router-link>
        <router-link v-if="user" class="sublink-1" to="/course/add"><i class="material-icons">add</i>Add</router-link>
        <a v-if="user" href="/api/user/logout"><i class="material-icons">exit_to_app</i>Log out</a>
    </nav>
    <!-- Drawer End -->
</template>

<script>
export default {
  props: ['user', 'courses']
}
</script>

<style>
nav * {
    vertical-align: middle;
}
</style>
