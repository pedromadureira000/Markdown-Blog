import axios from '~/plugins/axios'

export default {

  // --------------------------------------/ Auth APIs /----------------------------------------
	async checkAuthenticated(){
    return await axios.get("/api/user/check_authenticated").then((data)=> {return data.data})
	},

  async getCsrf(){
    return await axios.get("/api/user/getcsrf").then(() => {})
  },

	async login(payload){ 
		return await axios({
			method: "post",
			url: "/api/user/login",
			data: { username: payload.username, password: payload.password },
			headers: { "X-CSRFToken": payload.csrftoken },
		})
			.then((response) => {
				return response.data
			})
		},	

	async logout(){
		return await axios({
				method: "post",
				url: "/api/user/logout",
			})
				.then(() => {})
		},

	// async updateCurrentUserProfile(payload){
		// return await axios({ 
		// method: "put",
		// url: "/api/user/own_profile",
		// data:{
			// username: payload.username,
			// email: payload.email,
		// }
			// }).then((request) => {
					// return request.data 
				// })
	// },

  async updateOwnPassword(payload){
    return await axios({ 
    method: "put",
    url: "/api/user/update_own_password",
    data:{
      current_password: payload.current_password,
      password: payload.password,
    }
      }).then((request) => {
          return request.data 
        })
  },

  //---------------------------------------------------  Menu
	async createMenu(payload){
    let data_body = {
      slug: payload.slug,
      title: payload.title,
      icon: payload.icon,
		}
		return await axios({ 
		method: "post",
		url: "/api/core/menu",
		data: data_body}).then((request) => {
					return request.data 
				})
	},

	async fetchMenus(){
		return await axios({ 
		method: "get",
		url: "/api/core/menu",
			}).then((request) => {
					return request.data 
				})
	},

	async updateMenu(payload){
    let data_body = {
      default_submenu: payload.default_submenu,
      slug: payload.slug,
      title: payload.title,
      icon: payload.icon,
		}
		return await axios({ 
		method: "put",
		url: `/api/core/menu/${payload.id}`,
		data: data_body}).then((request) => {
					return request.data 
				})
	},

	async deleteMenu(menu_id){
		return await axios({ 
		method: "delete",
		url: `/api/core/menu/${menu_id}`,
			}).then((request) => {
					return request.data 
				})
	},

  //---------------------------------------------------  Sub-Menu
  //
	async createSubmenu(payload){
    let data_body = {
      menu: payload.menu,
      slug: payload.slug,
      title: payload.title,
      icon: payload.icon,
		}
		return await axios({ 
		method: "post",
		url: "/api/core/submenu",
		data: data_body}).then((request) => {
					return request.data 
				})
	},

	async fetchSubmenus(menu_id){
		return await axios({ 
		method: "get",
		url: `/api/core/submenu/${menu_id}`,
			}).then((request) => {
					return request.data 
				})
	},

	async updateSubmenu(payload){
    let data_body = {
      slug: payload.slug,
      title: payload.title,
      icon: payload.icon,
		}
		return await axios({ 
		method: "put",
		url: `/api/core/submenu/${payload.id}`,
		data: data_body}).then((request) => {
					return request.data 
				})
	},

	async deleteSubmenu(submenu_id){
		return await axios({ 
		method: "delete",
		url: `/api/core/submenu/${submenu_id}`,
			}).then((request) => {
					return request.data 
				})
	},

  //---------------------------------------------------  Page
  //
	async createPage(payload){
		return await axios({ 
		method: "post",
		url: "/api/core/page",
		data: payload}).then((request) => {
					return request.data 
				})
	},

	async fetchPages(menu_id){
		return await axios({ 
		method: "get",
		url: `/api/core/page/${menu_id}`,
			}).then((request) => {
					return request.data 
				})
	},

	async updatePage(payload){
		return await axios({ 
		method: "put",
		url: `/api/core/page/${payload.get('id')}`,
		data: payload}).then((request) => {
					return request.data 
				})
	},

	async deletePage(submenu_id){
		return await axios({ 
		method: "delete",
		url: `/api/core/page/${submenu_id}`,
			}).then((request) => {
					return request.data 
				})
	},

}
