<template>
  <p v-if="$fetchState.pending">Fetching mountains...</p>
  <p v-else-if="$fetchState.error">An error occurred :(</p>
  <div v-else>
    <div class="ma-3">
      <h3>Create User</h3>
      <form @submit.prevent="createUser">
        <div class="mb-3">
          <v-text-field
            label="Username"
            v-model="username"
            :error-messages="usernameErrors"
            required
            @blur="$v.username.$touch()"
          />
        </div>
        <div class="mb-3">
          <v-text-field
            label="Email"
            type="email"
            v-model="email"
            :error-messages="emailErrors"
            required
            @blur="$v.email.$touch()"
          />
        </div>
        <div class="mb-3">
          <v-text-field
            type="password"
            label="Password"
            v-model="password"
            :error-messages="passwordErrors"
            required
            @blur="$v.password.$touch()"
          />
        </div>
        <div class="mb-3">
          <v-text-field
            type="password"
            label="Password Confirm"
            v-model="password_confirm"
            :error-messages="passConfirmErrors"
            required
            @blur="$v.password_confirm.$touch()"
          />
        </div>
        <h4>User role</h4>
        <v-container
          class="px-0"
          style="display: flex;"
          fluid
        >
          <v-radio-group v-model="userRole" style="width: 25%;">
            <v-radio
              label="Guest"
              value="guest"
            ></v-radio>
            <v-radio
              label="Member"
              value="member"
            ></v-radio>
          </v-radio-group>
          <!-- <v-container -->
            <!-- class="px-0" -->
            <!-- fluid -->
            <!-- v-if="userRole === 'agent'"  -->
            <!-- style="width: 85%; display: flex; justify-content: space-between;" -->
          <!-- > -->
            <!-- <v-row > -->
              <!-- <v-checkbox  -->
                <!-- v-for="(value, perm) in agentPermissions" -->
                <!-- :key="perm" -->
                <!-- v-model="agentPermissions[perm]" -->
                <!-- :label="perm" -->
                <!-- style="margin-right: 27px;" -->
              <!-- ></v-checkbox> -->
            <!-- </v-row> -->
          <!-- </v-container> -->
        </v-container>
        <v-btn
          color="primary"
          type="submit"
          :loading="loading"
          :disabled="loading"
          >Submit</v-btn
        >
      </form>

      <h3 class="mt-6">Edit User</h3>
      <v-data-table
        :headers="headers"
        :items="users"
        :items-per-page="10"
        class="elevation-1"
      >
        <template v-slot:top>
        </template>
        <template v-slot:item.actions="{ item }">
          <user-edit-menu :user="item" @user-deleted="deleteUser(item)" />
        </template>
      </v-data-table>
    </div>
  </div>
</template>

<script>
import {
  required,
  sameAs,
  minLength,
  maxLength,
  email,
  alphaNum,
  integer
} from "vuelidate/lib/validators";
import { validationMixin } from "vuelidate";
 
export default {
  middleware: ["authenticated", "admin"],
  components: {
    "user-edit-menu": require("@/components/admin/user-edit-menu.vue").default,
  },
  mixins: [validationMixin],

  data() {
    return {
      username: null,
      email: null,
      password: null,
      password_confirm: null,
      loading: false,
      userRole: "guest",
      /** agentPermissions: { */
          /** create_client: false, */
          /** get_clients: false, */
          /** update_client: false, */
          /** delete_client: false, */
          /** create_item: false, */
          /** get_items: false, */
          /** update_item: false, */
          /** delete_item: false, */
          /** create_item_category: false, */
          /** get_item_category: false, */
          /** update_item_category: false, */
          /** delete_item_category: false, */
          /** create_price_table: false, */
          /** get_price_tables: false, */
          /** update_price_table: false, */
          /** delete_price_table: false */
      /** }, */
      users: [],
      headers: [
        { text: 'Username', value: 'username' },
        { text: 'Email', value: 'email' },
        { text: 'Role', value: 'role' },
        { text: 'Actions', value: 'actions' },
      ]
    };
  },

  async fetch() {
    let users = await this.$store.dispatch("auth/fetchUsersByAdmin");
    for (const user_index in users){
      let user = users[user_index]
      this.users.push({username: user.username, email: user.email, role: user.roles[0]})
    }
  },

  validations: {
    username: { 
      required, 
      alphaNum, 
      maxLength: maxLength(12)
    },
    email: {
      required,
      email,
    },
    password: {
      required,
      minLength: minLength(6),
      maxLength: maxLength(20),
    },
    password_confirm: {
      password_confirm: sameAs("password"),
    },
    userInfoGroup: [
      "username",
      "email",
      "password",
      "password_confirm",
    ],
  },

  methods: {
    async createUser() {
      this.$v.userInfoGroup.$touch();
      if (this.$v.userInfoGroup.$invalid) {
        this.$store.dispatch("setAlert", { message: "Please fill the form correctly.", alertType: "error" }, { root: true })
      } else {
        this.loading = true;
        let data = await this.$store.dispatch("auth/createUser", {
          username: this.username, 
          email: this.email,
          password: this.password,
          role: this.userRole,
          /** agentPermissions: this.agentPermissions */
        });
        if (data) {
          this.users.push({username: data.username, email: data.email, role: data.roles[0]})
        }
        this.loading = false;
      }
    },
    deleteUser(userToDelete) {
      this.users = this.users.filter((user) => user.username != userToDelete.username);
    },
  },

  computed: {
    usernameErrors() {
      const errors = [];
      if (!this.$v.username.$dirty) return errors;
      !this.$v.username.alphaNum && errors.push("Must have only alphanumeric characters.");
      !this.$v.username.required && errors.push("Username is required");
      !this.$v.username.maxLength && errors.push("This field must have up to 12 characters.");
      return errors;
    },
    emailErrors() {
      const errors = [];
      if (!this.$v.email.$dirty) return errors;
      !this.$v.email.email && errors.push("Must be valid e-mail");
      !this.$v.email.required && errors.push("E-mail is required");
      return errors;
    },
    passwordErrors() {
      const errors = [];
      if (!this.$v.password.$dirty) return errors;
      !this.$v.password.required && errors.push("Password is required.");
      !this.$v.password.maxLength &&
        errors.push("This field must have up to 20 characters.");
      !this.$v.password.minLength &&
        errors.push("This field must have at least 6 characters.");
      this.password === this.current_password &&
        errors.push(
          "The password should not be equal to the current password."
        );
      return errors;
    },
    passConfirmErrors() {
      const errors = [];
      if (!this.$v.password_confirm.$dirty) return errors;
      !this.$v.password_confirm.password_confirm &&
        errors.push("Password must be iqual.");
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
