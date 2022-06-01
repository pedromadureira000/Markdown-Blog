import axios from '~/plugins/axios'

export default {

  // --------------------------------------/ Auth APIs /----------------------------------------
	async checkAuthenticated(){
    return await axios.get("/api/user/check_authenticated").then((data)=> {return data.data})
	},

	// async getCsrf(){
		// return await axios.get("/api/user/getcsrf").then(() => {})
	// },

	async login(payload){ 
		return await axios({
			method: "post",
			url: "/api/user/gettoken",
			data: { username: payload.username, password: payload.password},
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

	// async updateOwnPassword(payload){
		// return await axios({ 
		// method: "put",
		// url: "/api/user/update_own_password",
		// data:{
			// current_password: payload.current_password,
			// password: payload.password,
		// }
			// }).then((request) => {
					// return request.data 
				// })
	// },

}

