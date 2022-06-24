<template>
  <div class="ma-3">
    <p>{{page.markdown_text}}</p>
  </div>
</template>

<script>
 
export default {
  asyncData(context) {
    if (context.payload) {
      return {
        page: context.payload.page
      }
    }
    return context.store.dispatch("blog/fetchPageToBuildBlog", {menu_slug: context.params.menu, submenu_slug: context.params.submenu,
      page_slug: context.params.page})
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
