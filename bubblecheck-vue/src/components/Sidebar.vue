<template>
    <!-- Drawer start -->
    <nav class="bubblecheck-sidebar">
        <router-link :to="{ name: 'home' }">
            BubbleCheck
        </router-link>
        <router-link v-if="user==null" :to="'Login'"><i>computer</i>Log in</router-link>
        <ul v-if="user">
            <router-link
                v-for="course in courses"
                v-bind:key="course.id"
                :to="{ name: 'course', params: { courseid: course.id }}"
                class="mdl-list__item mdl-navigation__link"
            >
                <i>school</i>{{ course.name }}
            </router-link>
        </ul>
        <div></div>
        <hr v-if="user" />
            <span v-if="user"><i>person</i>{{ this.$parent.user.teachername }}</span>
            <span v-if="user"><i>email</i>{{ this.$parent.user.email }}</span>
        <hr v-if="user" />
        <a v-if="user" href="/user/logout"><i>exit_to_app</i>Log out</a>
        <a href="#"><i role="presentation">help_outline</i><span> Help</span></a>
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
}
</style>
