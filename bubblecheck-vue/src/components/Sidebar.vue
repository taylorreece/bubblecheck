<template>
    <!-- Drawer start -->
    <nav class="bubblecheck-sidebar">
        <router-link v-if="user==null" :to="'Login'"><i class="material-icons">computer</i>Log in</router-link>
        <ul v-if="user">
            <router-link
                v-for="course in courses"
                v-bind:key="course.id"
                :to="{ name: 'course', params: { courseid: course.id }}"
                class="mdl-list__item mdl-navigation__link"
            >
                <i class="material-icons">school</i>{{ course.name }}
            </router-link>
        </ul>
        <div></div>
        <hr v-if="user" />
            <span v-if="user"><i class="material-icons">person</i>{{ this.$parent.user.teachername }}</span>
            <span v-if="user"><i class="material-icons">email</i>{{ this.$parent.user.email }}</span>
        <hr v-if="user" />
        <a v-if="user" href="/user/logout"><i class="material-icons">exit_to_app</i>Log out</a>
        <a href="#"><i class="material-icons">help_outline</i><span> Help</span></a>
    </nav>
    <!-- Drawer End -->
</template>

<script>
export default {
  props: ['user', 'courses']
}
</script>

<style>
.bubblecheck-sidebar {
    margin-top: 0px;
    margin-left: 0px;
    border-top: 0px;
    border-left: 0px;
    height: 100%;
}
</style>
