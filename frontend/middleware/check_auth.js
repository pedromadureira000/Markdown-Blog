import api from '~api'

export default async (ctx) => {
		// A middleware can be asynchronous. To do this return a  Promise or use async/await.
	if (process.server && ctx.req.headers.cookie){

    console.log(">>>>>>> middleware/check_auth > ctx.req.headers: ", ctx.req.headers)
		// let csrftoken = ctx.req.headers.cookie
			// .split(";")
			// .find(c => c.trim().startsWith("csrftoken="));
		// if (!csrftoken) {
			// return;
		// }
		// const token = csrftoken.split("=")[1];
		// ctx.store.commit('user/setCsrfOnServer', token) 

		try {
      await api.checkAuthenticated()	
			ctx.store.commit('user/authenticate')
		}
		catch (error) { 
      // if ( error.message == 'timeout of 15000ms exceeded') { 
      // }
      console.log('>>>> error middleware "check_auth": ', error)
		}
	}
}
