export interface BlogState {
	test: false
}

export const state = (): BlogState => ({
	test: false,
})  

// ------------------------------------------/ACTIONS/-------------------------------------------

import {ActionTree, Commit, Dispatch} from "vuex"
import {RootState} from "@/store/index"
 // @ts-ignore: This module is dynamically added in nuxt.config.js
import api from "~api"

export const actions: ActionTree<BlogState, RootState> = {

	// async fetchMenusAndSubmenusToBuildBlog({commit, dispatch}: {commit: Commit, dispatch: Dispatch}){
    // try {
		// let data = await api.fetchMenusAndSubmenusToBuildBlog()
		// return data
    // }
		// catch(error){
      // ErrorHandler(error, commit, dispatch, this.app.i18n, this.app.i18n.t("fetchMenusAndSubmenus_error_msg"))
		// }
	// },
  
	async fetchMenusToBuildBlog({commit, dispatch}: {commit: Commit, dispatch: Dispatch}){
    try {
		let menus = await api.fetchMenus()
		return {menuItems: menus}
    }
		catch(error){
      ErrorHandler(error, commit, dispatch, this.app.i18n, this.app.i18n.t("fetchMenus_error_msg"))
		}
	},

	async fetchSubmenusToBuildBlog({commit, dispatch}: {commit: Commit, dispatch: Dispatch}, menu_slug){
    try {
		let data = await api.fetchSubmenusToBuildBlog(menu_slug)
		return {allSubmenuItems: data}
    }
		catch(error){
      ErrorHandler(error, commit, dispatch, this.app.i18n, this.app.i18n.t("fetchSubmenus_error_msg"))
		}
	},

	async fetchPagesToBuildBlog({commit, dispatch}: {commit: Commit, dispatch: Dispatch}, payload: any){
    try {
		let pages = await api.fetchPagesToBuildBlog(payload)
		return {allPagesItems: pages}
    }
		catch(error){
      ErrorHandler(error, commit, dispatch, this.app.i18n, this.app.i18n.t("fetchPages_error_msg"))
		}
	},

	async fetchPageToBuildBlog({commit, dispatch}: {commit: Commit, dispatch: Dispatch}, payload: any){
    try {
		let page = await api.fetchPageToBuildBlog(payload)
		return {page: page}
    }
		catch(error){
      ErrorHandler(error, commit, dispatch, this.app.i18n, this.app.i18n.t("fetchPage_error_msg"))
		}
	}, 

}

// --------------------------------------------/MUTATIONS/---------------------------------------------

import {MutationTree} from "vuex"
import {ErrorHandler} from "~/helpers/functions";

export const mutations: MutationTree<BlogState> = { 
}
