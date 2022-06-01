export default (ctx) => {
	if (!ctx.store.state.user.authenticated){
		ctx.redirect(302, '/')
	}	
}
