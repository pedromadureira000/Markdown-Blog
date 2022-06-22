<template>
  <div>
    <v-bottom-navigation v-model="value">
      <!-- <NuxtLink v-for="item in allSubmenuItems" :key="item.slug" :to="item.to">Home page</NuxtLink> -->
      <v-btn v-for="item in allSubmenuItems" :key="item.slug" :value="item.title" :to="item.to" nuxt>
        <span>{{item.title}}</span>
        <v-icon>{{item.icon}}</v-icon>
      </v-btn>
    </v-bottom-navigation>
    <!-- I'm not sure what 'key' is for -->
		<nuxt-child :key="$route.params.menu"/>
  </div>
</template>

<script>
  export default {
    data(){ 
      return {
        value: '',
        /** allSubmenuItems: [ */
          /** {title: "Menu", icon: "mdi-menu", to: "admin-menu"}, */
          /** {title: "Sub-Menu", icon: "mdi-dots-vertical-circle-outline", to: "admin-submenu"}, */
          /** {title: "Page", icon: "mdi-book-open-page-variant", to: "admin-page"}, */
        /** ], */
      }
    },

    asyncData(context) {
      if (context.payload) {
        return {
          allSubmenuItems: context.payload.allSubmenuItems
        }
      }
      return context.store.dispatch("blog/fetchSubmenusToBuildBlog", context.params.menu)
    },

  }
</script>
<style scoped>
</style>
