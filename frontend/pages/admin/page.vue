<template>
  <p v-if="$fetchState.pending">{{$t('Fetching_data')}}</p>
  <p v-else-if="$fetchState.error">{{$t('Error_fetching_data')}}</p>
  <div v-else>
    <div class="ma-3">
      <v-expansion-panels>
        <v-expansion-panel>
          <v-expansion-panel-header>
            <h3>{{$t('Create Page')}}</h3>
          </v-expansion-panel-header>
          <v-expansion-panel-content>
            <form @submit.prevent="createPage">
              <!-- Menu -->
              <v-row align="center">
                <v-col
                  class="d-flex"
                  cols="12"
                  sm="6"
                >
                  <v-select
                    v-model="menu"
                    label="Menu"
                    :items="menus"
                    :item-text="(x) =>  x.title + ' (' + x.slug + ')'"
                    return-object
                    @change="fetchSubmenus('create')"
                  ></v-select>
                </v-col>
              </v-row>
              <!-- submenu -->
              <v-row align="center">
                <v-col
                  class="d-flex"
                  cols="12"
                  sm="6"
                >
                  <v-select
                    v-model="submenu"
                    label="Sub-menu"
                    :items="submenus"
                    :item-text="(x) =>  x.title + ' (' + x.slug + ')'"
                    return-object
                  ></v-select>
                </v-col>
              </v-row>
              <!-- Slug -->
              <v-text-field
                label="Slug"
                v-model.trim="slug"
                :error-messages="slugErrors"
                required
                @blur="$v.slug.$touch()"
              />
              <!-- Title -->
              <v-text-field
                :label="$t('Title')"
                v-model.trim="title"
                :error-messages="titleErrors"
                required
                @blur="$v.title.$touch()"
              />
              <!-- Description -->
              <v-textarea
                outlined
                :label="$t('Description')"
                v-model.trim="description"
                :error-messages="descriptionErrors"
                @blur="$v.description.$touch()"
                class="mb-3"
              />
              <!-- Image -->
              <v-row>
                <v-col>
                  <v-file-input
                    show-size
                    accept="image/*"
                    :label="$t('Image')"
                    prepend-icon="mdi-camera"
                    @change="onImageChange"
                  ></v-file-input>
                </v-col>
                <v-col>
                  <v-img
                    v-if="img_url"
                    contain
                    width="115px"
                    height="87px"
                    :src="img_url"
                  ></v-img>
                </v-col>
              </v-row>
              <!-- Markdown Text -->
              <v-textarea
                outlined
                :label="$t('Markdown Text')"
                v-model.trim="markdown_text"
                :error-messages="markdownTextErrors"
                @blur="$v.markdown_text.$touch()"
                class="mb-3"
              />
              <v-btn
                color="primary"
                type="submit"
                :loading="loading"
                :disabled="loading"
                >{{$t('Submit')}}</v-btn>
            </form>
          </v-expansion-panel-content>
        </v-expansion-panel>
      </v-expansion-panels>

    <div>
      <h3 class="mt-6 mb-4">{{$t('Edit Page')}}</h3>
      <!-- Search filters -->
      <v-card class="mb-6">
        <!-- <v-card-title style="font-size: 1rem; font-weight: 400; line-height: 1rem">{{$t('Search filters')}}</v-card-title> -->
        <v-row class="ml-2">
          <v-col cols='3'>
              <v-select
                v-model="menu_filter"
                label="Menu"
                :items="menus_filter"
                :item-text="(x) =>  x.title + ' (' + x.slug + ')'"
                return-object
                @change="fetchSubmenus('edit')"
              ></v-select>
          </v-col>
          <v-col cols='3'>
              <v-select
                v-model="submenu_filter"
                label="Sub-menu"
                :items="submenus_filter"
                :item-text="(x) => x.title + ' (' + x.slug + ')'"
                return-object
                @change="fetchPages"
              ></v-select>
          </v-col>
        </v-row>
      </v-card>

      <v-data-table
        :headers="headers"
        :items="pages"
        :items-per-page="10"
        item-key="id"
        class="elevation-1 mt-3"
        :loading="loading_pages"
      >
        <template v-slot:item.actions="{ item }">
          <page-edit-menu :page="item" :submenus="submenus" @page-deleted="deletePage(item)" />
        </template>
        <template v-slot:item.image="{ item }">
          <v-img
            contain
            width="115px"
            height="87px"
            :lazy-src="$store.state.CDNBaseUrl + '/media/images/page/defaultimage.jpeg'"
            :src="getImageUrl(item.image)"
          ></v-img>
        </template>
          <template v-slot:item.description="{ item }">
            <p>{{$reduceBigText(item.description)}}</p>
          </template>
        </v-data-table>
      </div>
    </div>
  </div>
</template>

<script>
import {
  required,
  maxLength,
} from "vuelidate/lib/validators";
import { validationMixin } from "vuelidate";
import {slugFieldValidator} from "~/helpers/validators"
 
export default {
  middleware: ["authenticated"],
  components: {
    "page-edit-menu": require("@/components/admin/page-edit-menu.vue").default,
  },
  mixins: [validationMixin],

  data() {
    return {
      // Page POST fields
      menu: null,
      submenu: null,
      slug: null,
      title: null,
      description: "",
      image: null,
      markdown_text: "",
      img_url: "",
      //
      pages: [],
      submenus: [],
      menus: [],
      submenus_groups: [],
      page_groups: [],
      submenus_filter: [],
      submenu_filter: null,
      menus_filter: [],
      menu_filter: null,
      loading: false,
      loading_pages: false,
      headers: [
        { text: this.$t('Image'), value: 'image' },
        { text: 'Slug', value: 'slug' },
        { text: this.$t('Title'), value: 'title' },
        { text: this.$t('Description'), value: 'description' },
        { text: this.$t('Actions'), value: 'actions' },
      ]
    };
  },

  async fetch() {
    let menus = await this.$store.dispatch("admin/fetchMenus")
    if (menus) {
      this.menus = menus
      this.menus_filter = menus
      if (menus.length >= 1){
        this.menu = this.menus[0]
        this.menu_filter = this.menus[0]
        await this.fetchSubmenus("create")
        if (this.submenus.length >= 1){
          this.submenus_filter = this.submenus // #< this.fetchSubmenus("edit")
          this.submenu_filter = this.submenus[0]
          await this.fetchPages()
        }
      }
    }
  },
  methods: {
    async fetchSubmenus(caller) {
      this.pages = [] // <<< RESET pages list
      let menu_id = null
      if (caller === "edit"){menu_id = this.menu_filter.id}
      else if (caller === "create"){menu_id = this.menu.id}

      let group_found = this.submenus_groups.find(el=>el.id === menu_id)
      if (group_found){
        if (caller === "create"){
          this.submenus = group_found.items
          if (group_found.items.length >= 1){
            this.submenu = group_found.items[0]
          }else{this.submenu = null}
        }
        else if (caller === "edit"){
          this.submenus_filter = group_found.items
          if (group_found.items.length >= 1){
            this.submenu_filter = group_found.items[0]
          }else {this.submenu_filter = null}
        }
      }
      else {
        this.loading_pages = true;
        let submenus = await this.$store.dispatch("admin/fetchSubmenus", menu_id)
        if (submenus){
          this.submenus_groups.push({id: menu_id, items: submenus})
          if (caller === "create"){
            this.submenus = submenus
            if (submenus.length >= 1){
              this.submenu = submenus[0]
            }else{this.submenu = null}
          }
          else if (caller === "edit"){
            this.submenus_filter = submenus
            if (submenus.length >= 1){
              this.submenu_filter = submenus[0]
            }
            else {
              this.submenu_filter = null
            }
          }
        }
        this.loading_pages = false
      }
    },

    async fetchPages() {
      if (this.submenu_filter === null){
        return;
      }
      let group_found = this.page_groups.find(el=>el.id === this.submenu_filter.id)
      if (group_found){
        this.pages = group_found.items
      }
      else{
        this.loading_pages = true;
        let pages = await this.$store.dispatch("admin/fetchPages", this.submenu_filter.id)
        if (pages){
          this.page_groups.push({id: this.submenu_filter.id, items: pages})
          this.pages = pages
          this.loading_pages = false
        }
      }
    },

    async createPage() {
      this.$v.subMenuInfoGroup.$touch();
      if (this.$v.subMenuInfoGroup.$invalid) {
        this.$store.dispatch("setAlert", { message: this.$t("Please_fill_the_form_correctly"), alertType: "error" }, { root: true })
      } else {
        this.loading = true;
        const formData = new FormData()
        formData.append('submenu', this.submenu.id)
        formData.append('slug', this.slug)
        formData.append('title', this.title)
        formData.append('description', this.description)
        formData.append('markdown_text', this.markdown_text)
        if (this.image){
          formData.append('image', this.image, this.image.name)
        }
        let data = await this.$store.dispatch("admin/createPage", formData)
        if (data) {
          let page_group = this.page_groups.find(el=> el.id===this.submenu.id)
          if (page_group){page_group.items.push(data)}
          // Clearing fields
          this.$v.$reset()
          this.slug = ""
          this.title = ""
          this.description = ""
          this.markdown_text = ""
        }
        this.loading = false
      }
    },

    deletePage(pageToDelete) {
      let group_found = this.page_groups.find(el=>el.id === pageToDelete.submenu)
      if (group_found){
        group_found.items = group_found.items.filter(el=>el.id != pageToDelete.id)
        this.pages = group_found.items
      }
    },

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

  validations: {
    slug: { 
      required, 
      slugFieldValidator, 
      maxLength: maxLength(25)
    },
    title: {
      required,
      maxLength: maxLength(30),
    },
    description: {
      required,
      maxLength: maxLength(200),
    },
    markdown_text: {
      required,
    },
    subMenuInfoGroup: [
      "slug",
      "title",
      "description",
      "markdown_text",
    ],
  },

  computed: {
    slugErrors() {
      const errors = [];
      if (!this.$v.slug.$dirty) return errors;
      !this.$v.slug.required && errors.push(this.$t("This_field_is_required"));
      !this.$v.slug.slugFieldValidator && errors.push(this.$t('SlugFieldErrorMessage'));
      !this.$v.slug.maxLength && errors.push(this.$formatStr(this.$t("This_field_must_have_up_to_X_characters"), 25));
      return errors;
    },
    titleErrors() {
      const errors = [];
      if (!this.$v.title.$dirty) return errors;
      !this.$v.title.required && errors.push(this.$t("This_field_is_required"));
      !this.$v.title.maxLength && errors.push(this.$formatStr(this.$t("This_field_must_have_up_to_X_characters"), 30));
      return errors;
    },
    descriptionErrors() {
      const errors = [];
      if (!this.$v.description.$dirty) return errors;
      !this.$v.description.required && errors.push(this.$t("This_field_is_required"));
      !this.$v.description.maxLength && errors.push(this.$formatStr(this.$t("This_field_must_have_up_to_X_characters"), 200));
      return errors;
    },
    markdownTextErrors() {
      const errors = [];
      if (!this.$v.markdown_text.$dirty) return errors;
      !this.$v.markdown_text.required && errors.push(this.$t("This_field_is_required"));
      return errors;
    },
  },
};
</script>
<style scoped>
.v-application .mb-3 {
  margin-bottom: 0px !important;
}
</style>
