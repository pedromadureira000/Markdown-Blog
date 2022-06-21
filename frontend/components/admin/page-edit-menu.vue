<template>
  <div>
    <dots-menu :menu_items="menu_items" :handleClick="handleClick"/>
     <!-- Edit Dialog -->
    <v-dialog :retain-focus="false" v-model="show_edit_dialog" max-width="50%">
      <v-card>
        <!-- Close Butto -->
        <div style="text-align: right;"> 
          <v-icon @click="show_edit_dialog = false" large class="pt-2 mr-2">mdi-window-close</v-icon >
        </div>
        <v-card-title style="padding-top: 0px;">{{$t('Edit')}}</v-card-title>
        <v-card-text>
          <v-container fluid>
              <!-- Menu -->
              <v-row align="center">
                <v-col
                  class="d-flex"
                  cols="12"
                  sm="6"
                >
                  <v-select
                    disabled
                    :value="submenu"
                    label="Sub-menu"
                    :items="[submenu]"
                    :item-text="(x) => x.title + ' (' + x.slug + ')'"
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
          </v-container>
        </v-card-text>
        <v-divider></v-divider>
        <!-- Submit Button -->
        <v-card-actions class="d-flex justify-space-around" style="width:100%;">
          <v-btn class="blue--text darken-1" text @click="show_edit_dialog = false">{{$t('Cancel')}}</v-btn>
          <v-btn 
            class="blue--text darken-1" 
            text 
            @click="updatePage()"
            :loading="loading"
            :disabled="loading"
          >{{$t('Save')}}</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Delete Confirmation Dialog -->
    <delete-confirmation-dialog 
      @delete-item="deletePage" 
      @cancel="show_delete_confirmation_dialog = false" 
      :show_delete_confirmation_dialog="show_delete_confirmation_dialog"
    />

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
  mixins: [validationMixin],
  components: {
    "dots-menu": require("@/components/dots-menu.vue").default,
    "delete-confirmation-dialog": require("@/components/delete-confirmation-dialog.vue").default,
  },
  props: ['page', 'submenus'],
  data() {
    return {
      show_edit_dialog: false,
      show_delete_confirmation_dialog: false,
      // Fields
      submenu: null,
      slug: null,
      title: null,
      description: null,
      image: null,
      markdown_text: "",
      img_url: "",
      //
      loading: false,
      menu_items: [
        { 
          title: this.$t('Edit'),
          icon: 'mdi-pencil',
          async click(){
            this.show_edit_dialog = true
          }
        },
        { 
          title: this.$t('Delete'),
          icon: 'mdi-delete',
          async click(){
            this.show_delete_confirmation_dialog = true
          }
        },
      ]
    }
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
    pageInfoGroup: [
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
      !this.$v.slug.slugFieldValidator && errors.push(this.$t('SlugFieldErrorMessage'));
      !this.$v.slug.maxLength && errors.push(this.$formatStr(this.$t("This_field_must_have_up_to_X_characters"), 25));
      !this.$v.slug.required && errors.push(this.$t("This_field_is_required"));
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

  methods: {

    handleClick(index){
      //this.menu_items[id].click()  #will get errors because the function click will not access properties with its own 'this'
      this.menu_items[index].click.call(this) // will call the function but the function will use the vue instance 'this' context.
    },

    async updatePage(){
      this.$v.pageInfoGroup.$touch();
      if (this.$v.pageInfoGroup.$invalid) {
        this.$store.dispatch("setAlert", { message: this.$t("Please_fill_the_form_correctly"), alertType: "error" }, { root: true })
      } else {
        this.loading = true;
        const formData = new FormData()
        formData.append('id', this.page.id)
        formData.append('slug', this.slug)
        formData.append('title', this.title)
        formData.append('description', this.description)
        formData.append('markdown_text', this.markdown_text)
        if (this.image){
          formData.append('image', this.image, this.image.name)
        }
        let data = await this.$store.dispatch("admin/updatePage", formData)
        this.loading = false;
        if (data){
          // Reactivity for page list inside page.vue 
          this.page.slug = this.slug
          this.page.title = this.title
          this.page.description = this.description
          this.page.markdown_text = this.markdown_text
          this.page.image = this.getImageUrl(data.image) 
            // Close dialog
          this.show_edit_dialog = false
        }
      }
    },

    async deletePage(){
      let data = await this.$store.dispatch('admin/deletePage', this.page.id)
      if (data === "ok"){
        this.$emit('page-deleted')
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

  mounted() {
    this.submenu = this.submenus.find(el=> el.id === this.page.submenu) 
    this.slug = this.page.slug
    this.title = this.page.title
    this.description = this.page.description
    this.markdown_text = this.page.markdown_text
    this.img_url = this.getImageUrl(this.page.image)
  }
}
</script>
