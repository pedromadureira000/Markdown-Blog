export interface UserState {
  authenticated: boolean,
}

export const state = (): UserState => ({
  authenticated: false,
})  

// --------------------------------------------/MUTATIONS/---------------------------------------------

import {MutationTree} from "vuex"
import {ErrorHandler} from "~/helpers/functions";

export const mutations: MutationTree<UserState> = { 
	authenticate(state) {
		state.authenticated = true;
	},
	deauthenticate(state) {
		state.authenticated = false;
	},
}
// ------------------------------------------/ACTIONS/-------------------------------------------

import {ActionTree, Commit, Dispatch} from "vuex"
import {RootState} from "@/store/index"
 // @ts-ignore: This module is dynamically added in nuxt.config.js
import api from "~api"
import axios from '~/plugins/axios'

export const actions: ActionTree<UserState, RootState> = {

	async login({commit, dispatch}: {commit: Commit, dispatch: Dispatch}, payload: any){
		try {
			let auth_token = await api.login(payload)
      axios.defaults.headers.common['Authorization'] = 'token ' + auth_token;
			dispatch("authenticate")
			dispatch("setAlert", {message: this.app.i18n.t('login_success_msg'), alertType: "success"}, { root: true })
		} catch(error){
      console.log(">>>>>>> login error: ", error)
        ErrorHandler(error, commit, dispatch, this.app.i18n, this.app.i18n.t("login_error_msg"))
		}
	},
	
	async logout({commit, dispatch}: {commit: Commit, dispatch: Dispatch}){
		try {
		await api.logout()
    axios.defaults.headers.common['Authorization'] = '' 
    delete axios.defaults.headers.common.Authorization // TODO Test it
		dispatch("deauthenticate")
		dispatch("setAlert", {message: this.app.i18n.t('logout_success_msg'), alertType: "success"}, { root: true })
		this.$router.push("/")
		} catch (error) {
      console.log(">>>>>>> logout error: ", error)
      ErrorHandler(error, commit, dispatch, this.app.i18n, this.app.i18n.t("logout_error_msg"))
		}
	},

	// async updateOwnPassword({commit, dispatch}: {commit: Commit, dispatch: Dispatch}, payload: any){
		// try {
			// await api.updateOwnPassword(payload)
			// commit("deleteUser")
			// dispatch("setAlert", {message: this.app.i18n.t('updatePassword_success_msg'), alertType: "success"}, { root: true })
			// setTimeout(() => {
				// this.$router.push("/")
			// }, 600);
		// }
		// catch(error){
      // ErrorHandler(error, commit, dispatch, this.app.i18n, this.app.i18n.t("updatePassword_error_msg"))
		// }
	// },

}
