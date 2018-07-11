<template>
    <!-- Header start -->
    <header class="bubblecheck-header mdl-layout__header">
        <div class="mdl-layout__header-row">
            <span class="mdl-layout-title">BubbleCheck</span>
            <div class="mdl-layout-spacer"></div>
            <button v-if="user" class="mdl-button mdl-js-button mdl-js-ripple-effect mdl-button--icon" id="courses_button">
                <i class="material-icons">school</i>
            </button>
            <ul v-if="user" class="mdl-menu mdl-js-menu mdl-js-ripple-effect mdl-menu--bottom-right" for="courses_button">
                <a v-for="course in courses" v-bind:key="course.id" class="mdl-menu__item">{{ course.name }}</a>
                <hr>
                <a class="mdl-menu__item">New</a>
            </ul>
            <button class="mdl-button mdl-js-button mdl-js-ripple-effect mdl-button--icon" id="user_button">
                <i class="material-icons">person</i>
            </button>
            <ul v-if="user" class="mdl-menu mdl-js-menu mdl-js-ripple-effect mdl-menu--bottom-right" for="user_button">
                <li class="mdl-menu__item" disabled>{{ user.teachername }}</li>
                <li class="mdl-menu__item mdl-menu__item--full-bleed-divider" disabled>{{ user.email }}</li>
                <a class="mdl-menu__item" href="#">Settings</a>
                <a class="mdl-menu__item" href="/user/logout">Log Out</a>
            </ul>
            <ul v-else class="mdl-menu mdl-js-menu mdl-js-ripple-effect mdl-menu--bottom-right" for="hdrbtn">
                <router-link class="mdl-menu__item" :to="'Login'">Log in</router-link>
                <a class="mdl-menu__item" href="#">Register</a>
            </ul>
        </div>
    </header>
    <!-- Header end -->
</template>

<script>
export default {
  props: ['user', 'courses']
}
</script>
