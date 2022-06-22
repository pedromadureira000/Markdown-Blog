export interface AdminState {
	test: false
}

export const state = (): AdminState => ({
	test: false,
})  

// ------------------------------------------/ACTIONS/-------------------------------------------

import {ActionTree, Commit, Dispatch} from "vuex"
import {RootState} from "@/store/index"
 // @ts-ignore: This module is dynamically added in nuxt.config.js
import api from "~api"

export const actions: ActionTree<AdminState, RootState> = {

  async createMenu({commit, dispatch}: {commit: Commit, dispatch: Dispatch}, payload: any){
    try {
      let data = await api.createMenu(payload)
      dispatch("setAlert", {message: this.app.i18n.t('createMenu_success_msg'), alertType: "success"}, { root: true })
      return data
    }
    catch(error){
      ErrorHandler(error, commit, dispatch, this.app.i18n, this.app.i18n.t("createMenu_error_msg"))
    }
  },

	async fetchMenus({commit, dispatch}: {commit: Commit, dispatch: Dispatch}){
    try {
		let menus = await api.fetchMenus()
		return menus
    }
		catch(error){
      ErrorHandler(error, commit, dispatch, this.app.i18n, this.app.i18n.t("fetchMenus_error_msg"))
		}
	},

  async updateMenu({commit, dispatch}: {commit: Commit, dispatch: Dispatch}, payload: any){
    try {
    await api.updateMenu(payload)
    dispatch("setAlert", {message: this.app.i18n.t('updateMenu_success_msg'), alertType: "success"}, { root: true })
    return "ok"
    }
    catch(error){
      ErrorHandler(error, commit, dispatch, this.app.i18n, this.app.i18n.t("updateMenu_error_msg"))
    }
  },

  async deleteMenu({commit, dispatch}: {commit: Commit, dispatch: Dispatch}, menu_id: string){
    try {
      await api.deleteMenu(menu_id)
      dispatch("setAlert", {message: this.app.i18n.t('deleteMenu_success_msg'), alertType: "success"}, { root: true })
      return "ok"
    }
    catch(error){
      ErrorHandler(error, commit, dispatch, this.app.i18n, this.app.i18n.t("deleteMenu_error_msg"))
    }
  },

  async createSubmenu({commit, dispatch}: {commit: Commit, dispatch: Dispatch}, payload: any){
    try {
      let data = await api.createSubmenu(payload)
      dispatch("setAlert", {message: this.app.i18n.t('createSubmenu_success_msg'), alertType: "success"}, { root: true })
      return data
    }
    catch(error){
      ErrorHandler(error, commit, dispatch, this.app.i18n, this.app.i18n.t("createSubmenu_error_msg"))
    }
  },

	async fetchSubmenus({commit, dispatch}: {commit: Commit, dispatch: Dispatch}, menu_id: string){
    try {
		let submenus = await api.fetchSubmenus(menu_id)
		return submenus
    }
		catch(error){
      ErrorHandler(error, commit, dispatch, this.app.i18n, this.app.i18n.t("fetchSubmenus_error_msg"))
		}
	},

  async updateSubmenu({commit, dispatch}: {commit: Commit, dispatch: Dispatch}, payload: any){
    try {
    await api.updateSubmenu(payload)
    dispatch("setAlert", {message: this.app.i18n.t('updateSubmenu_success_msg'), alertType: "success"}, { root: true })
    return "ok"
    }
    catch(error){
      ErrorHandler(error, commit, dispatch, this.app.i18n, this.app.i18n.t("updateSubmenu_error_msg"))
    }
  },

  async deleteSubmenu({commit, dispatch}: {commit: Commit, dispatch: Dispatch}, submenu_id: string){
    try {
      await api.deleteSubmenu(submenu_id)
      dispatch("setAlert", {message: this.app.i18n.t('deleteSubmenu_success_msg'), alertType: "success"}, { root: true })
      return "ok"
    }
    catch(error){
      ErrorHandler(error, commit, dispatch, this.app.i18n, this.app.i18n.t("deleteSubmenu_error_msg"))
    }
  },

  async createPage({commit, dispatch}: {commit: Commit, dispatch: Dispatch}, payload: any){
    try {
      let data = await api.createPage(payload)
      dispatch("setAlert", {message: this.app.i18n.t('createPage_success_msg'), alertType: "success"}, { root: true })
      return data
    }
    catch(error){
      ErrorHandler(error, commit, dispatch, this.app.i18n, this.app.i18n.t("createPage_error_msg"))
    }
  },

	async fetchPages({commit, dispatch}: {commit: Commit, dispatch: Dispatch}, submenu_id: string){
    try {
		let pages = await api.fetchPages(submenu_id)
		return pages
    }
		catch(error){
      ErrorHandler(error, commit, dispatch, this.app.i18n, this.app.i18n.t("fetchPages_error_msg"))
		}
	},

  async updatePage({commit, dispatch}: {commit: Commit, dispatch: Dispatch}, payload: any){
    try {
    let data = await api.updatePage(payload)
    dispatch("setAlert", {message: this.app.i18n.t('updatePage_success_msg'), alertType: "success"}, { root: true })
    return data
    }
    catch(error){
      ErrorHandler(error, commit, dispatch, this.app.i18n, this.app.i18n.t("updatePage_error_msg"))
    }
  },

  async deletePage({commit, dispatch}: {commit: Commit, dispatch: Dispatch}, page_id: string){
    try {
      await api.deletePage(page_id)
      dispatch("setAlert", {message: this.app.i18n.t('deletePage_success_msg'), alertType: "success"}, { root: true })
      return "ok"
    }
    catch(error){
      ErrorHandler(error, commit, dispatch, this.app.i18n, this.app.i18n.t("deletePage_error_msg"))
    }
  },


}

// --------------------------------------------/MUTATIONS/---------------------------------------------

import {MutationTree} from "vuex"
import {ErrorHandler} from "~/helpers/functions";

export const mutations: MutationTree<AdminState> = { 
}
