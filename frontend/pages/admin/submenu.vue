<template>
  <p v-if="$fetchState.pending">{{$t('Fetching_data')}}</p>
  <p v-else-if="$fetchState.error">{{$t('Error_fetching_data')}}</p>
  <div v-else>
    <div class="ma-3">
      <v-expansion-panels>
        <v-expansion-panel>
          <v-expansion-panel-header>
            <h3>{{$t('Create Sub-menu')}}</h3>
          </v-expansion-panel-header>
          <v-expansion-panel-content>
            <form @submit.prevent="createSubmenu">
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
                    :item-text="(x) => x.title + ' (' + x.slug + ')'"
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
      <h3 class="mt-6 mb-4">{{$t('Edit Sub-menu')}}</h3>
      <!-- Search filters -->
      <v-card class="mb-6">
        <!-- <v-card-title style="font-size: 1rem; font-weight: 400; line-height: 1rem">{{$t('Search filters')}}</v-card-title> -->
        <v-row class="ml-2">
          <v-col cols='3'>
              <v-select
                v-model="menu_filter"
                label="Menu"
                :items="menus"
                :item-text="(x) => x.title + ' (' + x.slug + ')'"
                return-object
                @change="fetchSubmenus"
              ></v-select>
          </v-col>
        </v-row>
      </v-card>

      <v-data-table
        :headers="headers"
        :items="submenus"
        :items-per-page="10"
        item-key="id"
        class="elevation-1 mt-3"
        loading="loading_submenus"
      >
        <template v-slot:item.actions="{ item }">
          <submenu-edit-menu :submenu="item" :menus="menus" @submenu-deleted="deleteSubmenu(item)" />
        </template>
        <template v-slot:item.icon="{ item }">
          <v-icon>{{item.icon}}</v-icon>
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
    "submenu-edit-menu": require("@/components/admin/submenu-edit-menu.vue").default,
  },
  mixins: [validationMixin],

  data() {
    return {
      menu: null,
      slug: null,
      title: null,
      icon: null,
      submenus_groups: [],
      submenus: [],
      menus: [],
      menu_filter: null,
      loading: false,
      loading_submenus: false,
      headers: [
        { text: 'Slug', value: 'slug' },
        { text: this.$t('Title'), value: 'title' },
        { text: this.$t('Icon'), value: 'icon' },
        { text: this.$t('Actions'), value: 'actions' },
      ]
    };
  },

  async fetch() {
    let menus = await this.$store.dispatch("admin/fetchMenus")
    if (menus) {
      this.menus = menus
    }
    if (this.menus.length >= 1){
      this.menu = this.menus[0]
      this.menu_filter = this.menus[0]
      await this.fetchSubmenus()
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

  methods: {

    async fetchSubmenus() {
      let group_found = this.submenus_groups.find(el=>el.id === this.menu_filter.id)
      if (group_found){
        this.submenus = group_found.items
      }
      else{
        this.loading_submenus = true;
        let submenus = await this.$store.dispatch("admin/fetchSubmenus", this.menu_filter.id)
        this.submenus_groups.push({id: this.menu_filter.id, items: submenus})
        this.submenus = submenus
        this.loading_submenus = false
      }
    },

    async createSubmenu() {
      this.$v.subMenuInfoGroup.$touch();
      if (this.$v.subMenuInfoGroup.$invalid) {
        this.$store.dispatch("setAlert", { message: this.$t("Please_fill_the_form_correctly"), alertType: "error" }, { root: true })
      } else {
        this.loading = true;
        let data = await this.$store.dispatch("admin/createSubmenu", {
          menu: this.menu.id, 
          slug: this.slug, 
          title: this.title,
          icon: this.icon,
        })
        if (data) {
          let submenu_group = this.submenus_groups.find(el=> el.id===this.menu.id)
          if (submenu_group){submenu_group.items.push(data)}
          // Clearing fields
          this.$v.$reset()
          // this avoid "This field is required" errors by vuelidate
          this.slug = ""
          this.title = ""
          this.icon = ""
        }
        this.loading = false
      }
    },
    deleteSubmenu(submenuToDelete) {
      this.submenus = this.submenus.filter((menu) => menu.id != 
        submenuToDelete.id);

      let group_found = this.submenus_groups.find(el=>el.id === submenuToDelete.menu)
      if (group_found){
        group_found.items = group_found.items.filter(el=>el.id != submenuToDelete.id)
      }
    },
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
    iconErrors() {
      const errors = [];
      if (!this.$v.icon.$dirty) return errors;
      !this.$v.icon.required && errors.push(this.$t("This_field_is_required"));
      !this.$v.icon.maxLength && errors.push(this.$formatStr(this.$t("This_field_must_have_up_to_X_characters"), 50));
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
