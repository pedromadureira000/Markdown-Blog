export interface RootState {
  alert: {
    alertMessage: string;
    alertType: string;
    showAlert: boolean;
    alertID: number
  },
  connectionError: boolean,
  CDNBaseUrl: string,
  // test: any
  menus: any,
}

export const state = (): RootState => ({
  alert: {
    alertMessage: "",
    alertType: "info",
    showAlert: false,
    alertID: 0
  },
  connectionError: false,
  // @ts-ignore
  CDNBaseUrl: process.env.DEV ? 'http://localhost:8000' : process.env.CDN_URL,
  // test: null,
  menus: [],
});

import { MutationTree } from "vuex";
export const mutations: MutationTree<RootState> = {
  setAlert(state, payload) {
    state.alert = {
      alertMessage: payload.message,
      alertType: payload.alertType,
      showAlert: true,
      alertID: Math.random()
    };
  },
  removeAlert(state) {
    state.alert = {
      alertMessage: "",
      alertType: "info",
      showAlert: false,
      alertID: state.alert.alertID
    };
  },
  switchConnectionError(state, value: boolean){
    state.connectionError = value
  },

  // testMutation(state, value: any){
    // state.test = value
  // }
  setMenus(state, value: any){
    state.menus = value
  }
  

};

 // @ts-ignore: This module is dynamically added in nuxt.config.js
import api from "~api"
// import {ErrorHandler} from "~/helpers/functions";
import { ActionTree, Commit, Dispatch } from "vuex";
export const actions: ActionTree<RootState, RootState> = {
  setAlert({ commit, state }: { commit: Commit, state: RootState }, 
           payload: {alertMessage: string, alertType: string, timeout?: number}) {
    // if showAlert is on. Close it and wait a few time to run the next.
    let timeout = 0
    if (state.alert.showAlert){
      commit("removeAlert")
      timeout = 300
    }
    setTimeout(() => {
      payload["timeout"] = payload["timeout"] ? payload["timeout"] : 3600; // <<<<<<<<< Default value
      commit("setAlert", payload);
      let current_alert = state.alert.alertID
      setTimeout(() => {
        if (state.alert.alertID == current_alert) {
          if (state.alert.alertType !== "error"){
            commit("removeAlert")
          }
        }
      }, payload.timeout);
    }, timeout);
  },

  removeAlert({ commit}: { commit: Commit}){
    commit('removeAlert')
  },
  switchConnectionError({ commit}: { commit: Commit}, value: boolean){
    commit('switchConnectionError', value)
  },

	async testConnection() {
		try {
			await api.getCsrf() 
      return 'ok'
		} catch (error) {
      // console.log(">>>>>>> ", error)
		}
	},

  async setMenus({ commit, dispatch}: { commit: Commit, dispatch: Dispatch}, payload: any){
    commit("setMenus", payload)
  },

  // async testFF({commit, dispatch}: {commit: Commit, dispatch: Dispatch}){
    // try {
      // await api.testFF()
    // }
    // catch(error){
      // ErrorHandler(error, commit, dispatch, this.app.i18n, 'testFF final error')
    // }
  // }

};
