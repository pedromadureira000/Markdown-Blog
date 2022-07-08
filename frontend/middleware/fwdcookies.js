import axios from '~/plugins/axios'

export default (ctx) => {
  if (ctx.req){ // XXX This is to run 'nuxt generate'
    if (process.server && !ctx.req.url.includes('/api/') && !ctx.req.url.startsWith('/erro')) {
      // console.log(ctx.req.url)
      // console.log(ctx.req.headers.cookie)
      axios.defaults.headers.common['cookie'] = ctx.req.headers['cookie']
    }
  }
}
