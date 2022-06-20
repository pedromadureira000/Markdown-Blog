<template>
  <p v-if="$fetchState.pending">{{$t('Fetching_data')}}</p>
  <p v-else-if="$fetchState.error">{{$t('Error_fetching_data')}}</p>
  <div v-else>
    <div class="ma-3">
      <v-expansion-panels>
        <v-expansion-panel>
          <v-expansion-panel-header>
            <h3>{{$t('Create Menu')}}</h3>
          </v-expansion-panel-header>
          <v-expansion-panel-content>
            <form @submit.prevent="createMenu">
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
      <h3 class="mt-6">{{$t('Edit Menu')}}</h3>
      <v-data-table
        :headers="headers"
        :items="menus"
        :items-per-page="10"
        item-key="id"
        class="elevation-1 mt-3"
      >
        <template v-slot:item.actions="{ item }">
          <menu-edit-menu :menu="item" @menu-deleted="deleteMenu(item)" />
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
    "menu-edit-menu": require("@/components/admin/menu-edit-menu.vue").default,
  },
  mixins: [validationMixin],

  data() {
    return {
      slug: null,
      title: null,
      icon: null,
      menus: [],
      loading: false,
      headers: [
        { text: 'Slug', value: 'slug' },
        { text: this.$t('Default Sub-menu'), value: 'default_submenu' },
        { text: this.$t('Title'), value: 'title' },
        { text: this.$t('Icon'), value: 'icon' },
        { text: this.$t('Actions'), value: 'actions' },
      ]
    };
  },

  async fetch() {
    // Fetch Submenus
    let menus = await this.$store.dispatch("admin/fetchMenus");
    if (menus) {
      this.menus = menus
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

  methods: {
    async createMenu() {
      this.$v.menuInfoGroup.$touch();
      if (this.$v.menuInfoGroup.$invalid) {
        this.$store.dispatch("setAlert", { message: this.$t("Please_fill_the_form_correctly"), alertType: "error" }, { root: true })
      } else {
        this.loading = true;
        let data = await this.$store.dispatch("admin/createMenu", {
          slug: this.slug, 
          title: this.title,
          icon: this.icon,
        })
        if (data) {
          this.menus.push(data)
          // Clearing fields
          this.$v.$reset()
          // this avoid "This field is required" errors by vuelidate
          this.slug = ""
          this.title = ""
          this.icon = ""
        }
        this.loading = false;
      }
    },
    deleteMenu(menuToDelete) {
      this.menus = this.menus.filter((menu) => menu.slug != 
        menuToDelete.slug);
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
      !this.$v.icon.maxLength && errors.push(this.$formatStr(this.$t("This_field_must_have_up_to_X_characters"), 15));
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
