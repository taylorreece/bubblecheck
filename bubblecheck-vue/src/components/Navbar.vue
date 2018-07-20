<template>
    <!-- Header start -->
    <header class="sticky">
        <label for="drawer-control" class="drawer-toggle"></label>
        <router-link :to="'/'" class="logo">Bubblecheck</router-link>
    </header>
    <!-- Header end -->
</template>

<script>
export default {
  props: ['user', 'courses']
}
</script>
