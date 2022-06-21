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
              <!-- Default Sub-menu -->
              <v-row align="center">
                <v-col
                  class="d-flex"
                  cols="12"
                  sm="6"
                >
                  <v-select
                    v-model="default_submenu"
                    :label="$t('Default Sub-menu')"
                    :items="submenus"
                    :item-text="(x) => x.slug ? x.title + ' (' + x.slug + ')' : $t('Empty')"
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
              <!-- Icon -->
              <v-text-field
                :label="$t('Icon')"
                v-model.trim="icon"
                :error-messages="iconErrors"
                required
                @blur="$v.icon.$touch()"
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
            @click="updateMenu()"
            :loading="loading"
            :disabled="loading"
          >{{$t('Save')}}</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Delete Confirmation Dialog -->
    <delete-confirmation-dialog 
      @delete-item="deleteMenu" 
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

let empty_default_submenu = {slug: null, id: null}

export default {
  mixins: [validationMixin],
  components: {
    "dots-menu": require("@/components/dots-menu.vue").default,
    "delete-confirmation-dialog": require("@/components/delete-confirmation-dialog.vue").default,
  },
  props: ['menu'],
  data() {
    return {
      show_edit_dialog: false,
      show_delete_confirmation_dialog: false,
      submenus: [empty_default_submenu],
      default_submenu: null,
      slug: null,
      title: null,
      icon: null,
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
    icon: {
      required,
      maxLength: maxLength(15),
    },
    menuInfoGroup: [
      "slug",
      "title",
      "icon",
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
    iconErrors() {
      const errors = [];
      if (!this.$v.icon.$dirty) return errors;
      !this.$v.icon.required && errors.push(this.$t("This_field_is_required"));
      !this.$v.icon.maxLength && errors.push(this.$formatStr(this.$t("This_field_must_have_up_to_X_characters"), 15));
      return errors;
    },
  },

  methods: {

    handleClick(index){
      //this.menu_items[id].click()  #will get errors because the function click will not access properties with its own 'this'
      this.menu_items[index].click.call(this) // will call the function but the function will use the vue instance 'this' context.
    },

    async updateMenu(){
      this.$v.menuInfoGroup.$touch();
      if (this.$v.menuInfoGroup.$invalid) {
        this.$store.dispatch("setAlert", { message: this.$t("Please_fill_the_form_correctly"), alertType: "error" }, { root: true })
      } else {
        this.loading = true;
        let data = await this.$store.dispatch("admin/updateMenu", {
          default_submenu: this.default_submenu.id,
          id: this.menu.id,
          slug: this.slug,
          title: this.title,
          icon: this.icon,
        })
        this.loading = false;
        if (data === 'ok'){
          // Reactivity for menu list inside menu.vue 
          this.menu.default_submenu = this.default_submenu,
          this.menu.slug = this.slug
          this.menu.title = this.title
          this.menu.icon = this.icon
            // Close dialog
          this.show_edit_dialog = false
        }
      }
    },

    async deleteMenu(){
      let data = await this.$store.dispatch('admin/deleteMenu', this.menu.id)
      if (data === "ok"){
        this.$emit('menu-deleted')
      }
    },

    async fetchSubmenus(){
      let submenus = await this.$store.dispatch("admin/fetchSubmenus", this.menu.id)
      if (submenus){
        this.submenus = [...submenus, empty_default_submenu]
      }
    }
  },

	watch: {
    show_edit_dialog(newValue){
      /** console.log(`old value = ${oldValue}. New value = ${newValue}`  ) */
    if (newValue === true && this.submenus.length == 1) { // TODO weird logic
      this.fetchSubmenus()
    }}
  },

  mounted() {
    this.slug = this.menu.slug
    this.default_submenu = this.menu.default_submenu ? this.menu.default_submenu : empty_default_submenu
    this.title = this.menu.title
    this.icon = this.menu.icon
  }
}
</script>
