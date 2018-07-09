<template>
    <!-- Drawer start -->
    <div class="bubblecheck-drawer mdl-layout__drawer mdl-color--blue-grey-900 mdl-color-text--blue-grey-50">
        <nav class="bubblecheck-drawer-header" v-if="this.$parent.user">
            <span class="bubblecheck-drawer-header-text"><i class="mdl-color-text--blue-grey-400 material-icons">person</i>{{ this.$parent.user.teachername }}</span>
            <span class="bubblecheck-drawer-header-text"><i class="mdl-color-text--blue-grey-400 material-icons">email</i>{{ this.$parent.user.email }}</span>
        </nav>
        <nav class="bubblecheck-navigation mdl-navigation mdl-color--blue-grey-800 mdl-color-text--blue-grey-400">
            <a class="mdl-navigation__link" href=""><i class="material-icons" role="presentation">home</i>Home</a>
            <a v-if="this.$parent.user" class="mdl-navigation__link" href="#"><i class="material-icons">school</i>Courses</a>
            <div class="mdl-layout-spacer"></div>
            <a v-if="this.$parent.user" class="mdl-navigation__link" href="/user/logout"><i class="material-icons">exit_to_app</i>Log out</a>
            <a class="mdl-navigation__link" href=""><i class="mdl-color-text--blue-grey-400 material-icons" role="presentation">help_outline</i><span class="visuallyhidden">Help</span></a>
        </nav>
    </div>
    <!-- Drawer End -->
</template>

<style>
.bubblecheck-drawer-header {
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
}
.bubblecheck-drawer-header-text {
  display: flex;
  -webkit-flex-direction: row;
      -ms-flex-direction: row;
          flex-direction: row;
  align-items: center;
  color: rgba(255,255,255,0.56);
}
.bubblecheck-drawer-header-text .material-icons {
    margin-right: 20px;
}
</style>
