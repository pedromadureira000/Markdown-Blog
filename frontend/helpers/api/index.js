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
		url: "/api/core/get_menus",
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

	async fetchPages(submenu_id){
		return await axios({ 
		method: "get",
		url: `/api/core/page/${submenu_id}`,
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

  //---------------------------------------------------  Blog APIs

	async fetchSubmenusToBuildBlog(menu_slug){
		return await axios({ 
		method: "get",
		url: `/api/core/fetch_submenus_to_build_blog/${menu_slug}`,
			}).then((request) => {
					return request.data 
				})
	}, 

	async fetchPagesToBuildBlog(payload){
		return await axios({ 
		method: "get",
		url: `/api/core/fetch_pages_to_build_blog/${payload.menu_slug}/${payload.submenu_slug}`,
			}).then((request) => {
					return request.data 
				})
	},

	async fetchPageToBuildBlog(payload){
		return await axios({ 
		method: "get",
		url: `/api/core/fetch_page_to_build_blog/${payload.menu_slug}/${payload.submenu_slug}/${payload.page_slug}`,
			}).then((request) => {
					return request.data 
				})
	},
}
