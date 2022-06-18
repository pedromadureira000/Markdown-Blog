<template>
  <div>
    <div class="ma-3">
      <h3>{{$t('Update_profile')}}</h3>
      <form @submit.prevent="updateCurrentUserProfile">
        <div class="mb-3">
          <v-text-field
            disabled
            label="Username"
            :value="username"
          />
        </div>
        <div class="mb-3">
          <v-text-field
            disabled
            label="Email"
            :value="email"
          />
        </div>
        <v-btn 
          color="primary"
          type="submit"
          :loading="loading_profile"
          disabled
        >{{$t('Save')}}</v-btn>
      </form>

      <h3 class="mt-4">{{$t('Change_Password')}}</h3>
      <p class="caption">{{$t('After_change_your_password_you_will_be_logged_out')}}</p>

      <form @submit.prevent="passwordSubmit">
        <div class="mb-3">
          <v-text-field
            type="password"
            :label="$t('Current_password')"
            v-model.trim="current_password"
            :error-messages="currentPassErrors"
            required
            @blur="$v.current_password.$touch()"
          />
        </div>
        <div class="mb-3">
          <v-text-field
            type="password"
            label="Password"
            v-model.trim="password"
            :error-messages="passwordErrors"
            required
            @blur="$v.password.$touch()"
          />
        </div>
        <div class="mb-3">
          <v-text-field
            type="password"
            :label="$t('Password_Confirm')"
            v-model.trim="password_confirm"
            :error-messages="passConfirmErrors"
            required
            @blur="$v.password_confirm.$touch()"
          />
        </div>
        <v-btn 
          color="primary" 
          type="submit"
          :loading="loading_password"
          :disabled="loading_password"
        >{{$t('Save')}}</v-btn>
      </form>
    </div>
  </div>
</template>

<script>
import {
  required,
  sameAs,
  minLength,
  maxLength,
  email
} from "vuelidate/lib/validators";
import { validationMixin } from "vuelidate";

export default {
	middleware: ['authenticated'],
  mixins: [validationMixin],

  data() {
    return {
			username: this.$store.state.user.currentUser.username,
			email: this.$store.state.user.currentUser.email,
      current_password: "",
      password: "",
      password_confirm: "",
      loading_password: false,
      loading_profile: false,
    };
  },

  validations: {
    email: {
      required,
      email,
    },
    current_password: {
      required,
      minLength: minLength(6),
      maxLength: maxLength(20),
    },
    password: {
      required,
      minLength: minLength(6),
      maxLength: maxLength(20),
    },
    password_confirm: {
      password_confirm: sameAs("password"),
    },
    /** profileGroup: ["username", "email"], */
    passwordUpdateGroup: ["current_password","password", "password_confirm"],
  },

  methods: {
    /** async updateCurrentUserProfile() { */
      /** this.$v.profileGroup.$touch(); */
      /** if (this.$v.profileGroup.$invalid) { */
        /** this.$store.dispatch("setAlert", { message: this.$t("Please_fill_the_form_correctly"), alertType: "error" }, { root: true }) */
      /** } else { */
        /** if ( */
          /** this.username === this.$store.state.user.currentUser.username && */
          /** this.email === this.$store.state.user.currentUser.email */
        /** ){ this.$store.dispatch('setAlert', {message: this.$t('You_have_not_changed_any_fields'), alertType: 'warning'}, { root: true }) } */
        /** else { */
          /** this.loading_profile = true; */
          /** await this.$store.dispatch('user/updateCurrentUserProfile', { */
            /** username: this.username, */
            /** email: this.email, */
          /** }) */
          /** this.loading_profile = false; */
        /** }	 */
      /** } */
    /** }, */

    async passwordSubmit() {
      this.$v.passwordUpdateGroup.$touch();
      if (this.$v.passwordUpdateGroup.$invalid) {
        this.$store.dispatch("setAlert", { message: this.$t("Please_fill_the_form_correctly"), alertType: "error" }, { root: true })
      } else {
        this.loading_password = true;
        await this.$store.dispatch('user/updateOwnPassword', {password: this.password, current_password: this.current_password})
        this.loading_password = false;
      }
    },
  },
  computed: {
    /** emailErrors() { */
      /** const errors = []; */
      /** if (!this.$v.email.$dirty) return errors; */
      /** !this.$v.email.email && errors.push(this.$t("Must be valid e-mail")); */
      /** !this.$v.email.required && errors.push(this.$t("This_field_is_required"));       */
      /** return errors; */
    /** }, */
    currentPassErrors() {
      const errors = [];
      if (!this.$v.current_password.$dirty) return errors;
      !this.$v.current_password.required && errors.push(this.$t("This_field_is_required"));
      !this.$v.current_password.maxLength && errors.push(this.$formatStr(this.$t("This_field_must_have_up_to_X_characters"), 20));
      !this.$v.current_password.minLength && errors.push(this.$formatStr(this.$t("This_field_must_have_at_least_X_characters"), 6));
      return errors;
    },
    passwordErrors() {
      const errors = [];
      if (!this.$v.password.$dirty) return errors;
      !this.$v.password.required && errors.push(this.$t("This_field_is_required"));
      !this.$v.password.maxLength && errors.push(this.$formatStr(this.$t("This_field_must_have_up_to_X_characters"), 20));
      !this.$v.password.minLength && errors.push(this.$formatStr(this.$t("This_field_must_have_at_least_X_characters"), 6));
      this.password === this.current_password && errors.push(this.$t("Password_must_be_different_from_current_password"))
      return errors;
    },
    passConfirmErrors() {
      const errors = [];
      if (!this.$v.password_confirm.$dirty) return errors;
      /* !this.$v.password_confirm.required && errors.push("Password is required."); */
      !this.$v.password_confirm.password_confirm && errors.push(this.$t('password_confirm_does_not_match'));
      return errors;
    },
  }
}
</script>
<style scoped>
.v-application .mb-3 {
    margin-bottom: 0px !important;
}
</style>
