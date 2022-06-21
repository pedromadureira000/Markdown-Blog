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
                    :value="menu"
                    label="Menu"
                    :items="[menu]"
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
            @click="updateSubmenu()"
            :loading="loading"
            :disabled="loading"
          >{{$t('Save')}}</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Delete Confirmation Dialog -->
    <delete-confirmation-dialog 
      @delete-item="deleteSubmenu" 
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
  props: ['submenu', 'menus'],
  data() {
    return {
      show_edit_dialog: false,
      show_delete_confirmation_dialog: false,
      menu: null,
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
      maxLength: maxLength(50),
    },
    subMenuInfoGroup: [
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
      !this.$v.icon.maxLength && errors.push(this.$formatStr(this.$t("This_field_must_have_up_to_X_characters"), 50));
      return errors;
    },
  },

  methods: {

    handleClick(index){
      //this.menu_items[id].click()  #will get errors because the function click will not access properties with its own 'this'
      this.menu_items[index].click.call(this) // will call the function but the function will use the vue instance 'this' context.
    },

    async updateSubmenu(){
      this.$v.subMenuInfoGroup.$touch();
      if (this.$v.subMenuInfoGroup.$invalid) {
        this.$store.dispatch("setAlert", { message: this.$t("Please_fill_the_form_correctly"), alertType: "error" }, { root: true })
      } else {
        this.loading = true;
        let data = await this.$store.dispatch("admin/updateSubmenu", {
          id: this.submenu.id,
          slug: this.slug,
          title: this.title,
          icon: this.icon,
        })
        this.loading = false;
        if (data === 'ok'){
          // Reactivity for submenu list inside submenu.vue 
          this.submenu.slug = this.slug
          this.submenu.title = this.title
          this.submenu.icon = this.icon
            // Close dialog
          this.show_edit_dialog = false
        }
      }
    },

    async deleteSubmenu(){
      let data = await this.$store.dispatch('admin/deleteSubmenu', this.submenu.id)
      if (data === "ok"){
        this.$emit('submenu-deleted')
      }
    },
    
  },

  mounted() {
    this.menu = this.menus.find(el=> el.id === this.submenu.menu) 
    this.slug = this.submenu.slug
    this.title = this.submenu.title
    this.icon = this.submenu.icon
  }
}
</script>
