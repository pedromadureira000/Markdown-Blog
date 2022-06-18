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

}

