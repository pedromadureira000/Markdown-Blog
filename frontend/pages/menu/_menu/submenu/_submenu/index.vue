<template>
  <div class="ma-3">
    <div 
      v-for="item in allPagesItems"
      :key=item.id
    >
      <h1>{{item.title}}</h1>
      <p>{{item.description}}</p>
      <v-img
        contain
        width="115px"
        height="87px"
        :lazy-src="$store.state.CDNBaseUrl + '/media/images/page/defaultimage.jpeg'"
        :src="getImageUrl(item.image)"
      ></v-img>

      <v-btn text :to="item.to">Link</v-btn>
      <v-divider></v-divider>
    </div>

  </div>
</template>

<script>
 
export default {
  asyncData(context) {
    if (context.payload) {
      return {
        allPagesItems: context.payload.allPagesItems
      }
    }
    return context.store.dispatch("blog/fetchPagesToBuildBlog", {menu_slug: context.params.menu, submenu_slug: context.params.submenu})
  },

  data() {
    return {
    };
  },

  methods: {

    // Image
    onImageChange (event) {
      this.image = event
      if (event === null){
        this.img_url = ''
      } else{
        this.img_url = URL.createObjectURL(this.image)
      }
    },

    // The backend return item url with base url "http://..." after create an item
    getImageUrl(image){
      if (image) {
        let url = image
        if (url.startsWith('http')){
          let url_fixed = url.split('/media/images/')[1]
          return this.$store.state.CDNBaseUrl + '/media/images/' + url_fixed
        }
        else {
          return this.$store.state.CDNBaseUrl + url
        }
      }
      else {
        return this.$store.state.CDNBaseUrl + '/media/images/page/defaultimage.jpeg'
      }
    },
  },

};
</script>
<style scoped>
.v-application .mb-3 {
  margin-bottom: 0px !important;
}
</style>
