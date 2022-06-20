<template>
  <div>
    <v-bottom-navigation v-model="value">
      <v-btn v-for="item in allMenuItems" :key="item.title" :value="item.title" :to="localePath(item.to)" nuxt>
        <span>{{$t(item.title)}}</span>
        <v-icon>{{item.icon}}</v-icon>
      </v-btn>
    </v-bottom-navigation>
		<nuxt-child/>
  </div>
</template>

<script>
  export default {
    middleware: ["authenticated"],
    data(){ 
      return {
        value: '',
        allMenuItems: [
          {title: "Menu", icon: "mdi-menu", to: "admin-menu"},
          {title: "Sub-Menu", icon: "mdi-dots-vertical-circle-outline", to: "admin-submenu"},
          {title: "Page", icon: "mdi-book-open-page-variant", to: "admin-page"},
        ],
      }
    },

    /** computed: { */
    /** }, */
  }
</script>
<style scoped>
</style>
