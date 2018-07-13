<template>
    <!-- Drawer start -->
    <div class="bubblecheck-drawer mdl-layout__drawer">
        <nav class="title mdl-color--primary mdl-color-text--primary-contrast">
            BubbleCheck
        </nav>
        <nav class="bubblecheck-navigation mdl-navigation">
            <router-link v-if="user==null" class="mdl-navigation__link" :to="'Login'"><i class="material-icons">computer</i>Log in</router-link>
            <ul v-if="user" class="mdl-list">
                <router-link
                    v-for="course in courses"
                    v-bind:key="course.id"
                    :to="{ name: 'course', params: { courseid: course.id }}"
                    class="mdl-list__item mdl-navigation__link"
                    >
                    <i class="material-icons">school</i>{{ course.name }}
                </router-link>
            </ul>
            <div class="mdl-layout-spacer"></div>
            <span v-if="user" class="drawer-info-text"><i class="material-icons">person</i>{{ this.$parent.user.teachername }}</span>
            <span v-if="user" class="drawer-info-text"><i class="material-icons">email</i>{{ this.$parent.user.email }}</span>
            <a v-if="user" class="mdl-navigation__link" href="/user/logout"><i class="material-icons">exit_to_app</i>Log out</a>
            <a class="mdl-navigation__link" href="#"><i class="material-icons" role="presentation">help_outline</i><span class="visuallyhidden">Help</span></a>
        </nav>
    </div>
    <!-- Drawer End -->
</template>

<script>
export default {
  props: ['user', 'courses']
}
</script>

<style>
.bubblecheck-drawer {
    border-right: 0;
    box-shadow: unset;
}

.bubblecheck-drawer .title {
  box-sizing: border-box;
  display: -webkit-flex;
  display: -ms-flexbox;
  display: flex;
  -webkit-flex-direction: column;
      -ms-flex-direction: column;
          flex-direction: column;
  -webkit-justify-content: flex-end;
      -ms-flex-pack: end;
          justify-content: flex-end;
  padding: 16px;
  font-size: 130%;
  min-height: 64px;
}

.bubblecheck-drawer .title span {
  display: flex;
  -webkit-flex-direction: row;
      -ms-flex-direction: row;
          flex-direction: row;
  align-items: center;
}

/* iOS Safari specific workaround */
.bubblecheck-drawer .mdl-menu__container {
    z-index: -1;
}

.bubblecheck-drawer .bubblecheck-navigation {
    z-index: -2;
    padding-top: 0px;
}
/* END iOS Safari specific workaround */

.bubblecheck-drawer .mdl-menu .mdl-menu__item {
    display: -webkit-flex;
    display: -ms-flexbox;
    display: flex;
    -webkit-align-items: center;
    -ms-flex-align: center;
    align-items: center;
}

.bubblecheck-layout .bubblecheck-navigation .mdl-navigation__link,
.bubblecheck-layout .bubblecheck-navigation .drawer-info-text {
    display: -webkit-flex !important;
    display: -ms-flexbox !important;
    display: flex !important;
    -webkit-flex-direction: row;
    -ms-flex-direction: row;
    flex-direction: row;
    -webkit-align-items: center;
    -ms-flex-align: center;
    align-items: center;
    font-weight: 500;
}

.bubblecheck-layout .bubblecheck-navigation .drawer-info-text {
    padding: 0px 16px;
}

.bubblecheck-navigation .mdl-navigation__link .material-icons,
.bubblecheck-navigation .drawer-info-text .material-icons {
    font-size: 24px;
    margin-right: 32px;
}
</style>
