<template>
    <!-- Drawer start -->
    <div class="bubblecheck-drawer mdl-layout__drawer">
        <nav class="title mdl-color--primary mdl-color-text--primary-contrast">
            BubbleCheck
        </nav>
        <nav class="bubblecheck-navigation">
            <a class="mdl-navigation__link" href=""><i class="material-icons" role="presentation">home</i>Home</a>
            <router-link v-if="this.$parent.user==null" class="mdl-navigation__link" :to="'Login'"><i class="material-icons">computer</i>Log in</router-link>
            <a v-if="this.$parent.user" class="mdl-navigation__link" href="#"><i class="material-icons">school</i>Courses</a>
            <div class="mdl-layout-spacer"></div>
            <a v-if="this.$parent.user" class="mdl-navigation__link" href="#"><i class="material-icons">person</i>{{ this.$parent.user.teachername }}</a>
            <a v-if="this.$parent.user" class="mdl-navigation__link" href="#"><i class="material-icons">email</i>{{ this.$parent.user.email }}</a>
            <a v-if="this.$parent.user" class="mdl-navigation__link" href="/user/logout"><i class="material-icons">exit_to_app</i>Log out</a>
            <a class="mdl-navigation__link" href="#"><i class="material-icons" role="presentation">help_outline</i><span class="visuallyhidden">Help</span></a>
        </nav>
    </div>
    <!-- Drawer End -->
</template>

<style>
.bubblecheck-drawer {
    border-right: 0;
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
  height: 100px;
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
.bubblecheck-layout .bubblecheck-navigation .mdl-navigation__link {
    display: -webkit-flex !important;
    display: -ms-flexbox !important;
    display: flex !important;
    -webkit-flex-direction: row;
    -ms-flex-direction: row;
    flex-direction: row;
    -webkit-align-items: center;
    -ms-flex-align: center;
    align-items: center;
    padding: 10px;
    font-weight: 500;
}

.bubblecheck-layout .bubblecheck-navigation .mdl-navigation__link:hover {
    background-color: #00BCD4;
    color: #37474F;
}

.bubblecheck-navigation .mdl-navigation__link .material-icons {
    font-size: 24px;
    margin-right: 32px;
}
</style>
