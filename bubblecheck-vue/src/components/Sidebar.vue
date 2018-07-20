<template>
    <!-- Drawer start -->
    <nav>
        <label for="drawer-control" class="drawer-close"></label>
        <router-link v-if="user==null" :to="'Login'"><i class="material-icons">computer</i>Log in</router-link>
        <router-link v-if="user==null" :to="'Register'"><i class="material-icons">ballot</i>Register</router-link>
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
        <span v-if="user"><i class="material-icons">person</i>{{ this.$parent.user.teachername }}</span>
        <span v-if="user"><i class="material-icons">email</i>{{ this.$parent.user.email }}</span>
        <a v-if="user" href="/user/logout"><i class="material-icons">exit_to_app</i>Log out</a>
    </nav>
    <!-- Drawer End -->
</template>

<script>
export default {
  props: ['user', 'courses']
}
</script>

<style>

</style>
