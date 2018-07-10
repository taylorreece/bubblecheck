<template>
    <!-- Header start -->
    <header class="bubblecheck-header mdl-layout__header">
        <div class="mdl-layout__header-row">
            <span class="mdl-layout-title">BubbleCheck</span>
            <div class="mdl-layout-spacer"></div>
            <button class="mdl-button mdl-js-button mdl-js-ripple-effect mdl-button--icon" id="hdrbtn">
                <i class="material-icons">person</i>
            </button>
            <ul v-if="this.$parent.user" class="mdl-menu mdl-js-menu mdl-js-ripple-effect mdl-menu--bottom-right" for="hdrbtn">
                <li class="mdl-menu__item" disabled>{{ this.$parent.user.teachername }}</li>
                <li class="mdl-menu__item mdl-menu__item--full-bleed-divider" disabled>{{ this.$parent.user.email }}</li>
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
