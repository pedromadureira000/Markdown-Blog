import colors from 'vuetify/es5/util/colors'
import {messages} from './messages'
const _isdev = process.env.DEV
const axios = require("axios");

export default {
  target: 'static',

  // Global page headers: https://go.nuxtjs.dev/config-head
  head: {
    titleTemplate: 'My Blog',
    title: 'My Blog',
    htmlAttrs: {
      lang: 'en'
    },
    meta: [
      { charset: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      { hid: 'description', name: 'description', content: '' },
      { name: 'format-detection', content: 'telephone=no' }
    ],
    link: [
      { rel: 'icon', type: 'image/x-icon', href: '/favicon.jpg' }
    ]
  },

  loading: { color: '#fff' },

  // Global CSS: https://go.nuxtjs.dev/config-css
  css: [
  ],

  // Plugins to run before rendering page: https://go.nuxtjs.dev/config-plugins
  plugins: [
		'@/plugins/vuetify',
		'~/plugins/myFunctions',
  ],

  // Auto import components: https://go.nuxtjs.dev/config-components
  components: true,

  // Modules for dev and build (recommended): https://go.nuxtjs.dev/config-modules
  buildModules: [
    // https://go.nuxtjs.dev/typescript
    '@nuxt/typescript-build',
    // https://go.nuxtjs.dev/vuetify
    '@nuxtjs/vuetify',
  ],

  // Modules: https://go.nuxtjs.dev/config-modules
  modules: [
    '@nuxtjs/i18n',
    '@nuxtjs/proxy',
  ],

  i18n: {
    locales: ['pt-BR', 'en'],
    strategy: 'prefix_except_default',
    defaultLocale: 'pt-BR',
    detectBrowserLanguage: {
      useCookie: true,
      cookieKey: 'lang',
      redirectOn: 'root',  // recommended
    },
    parsePages: false,   // Disable babel parsing. To use custom pages
    // If a custom path is missing for one of the locales, the defaultLocale custom path is used, if set.
    pages: {
      about: {
        en: '/about',
        'pt-BR': '/sobre',
      },
      myaccount: {
        en: '/my-account',
        'pt-BR': '/minha-conta',
      },
      admin: {
        en: '/admin',
        'pt-BR': '/admin',
      },
      'admin/menu': {
        en: '/admin/menu',
        'pt-BR': '/admin/menu',
      },
      'admin/submenu': {
        en: '/admin/submenu',
        'pt-BR': '/admin/submenu',
      },
      'admin/page': {
        en: '/admin/page',
        'pt-BR': '/admin/pagina',
      },
      // 'menu': {
        // en: 'menu',
        // 'pt-BR': 'menu',
      // },
      // 'menu/:menu': {
        // en: 'menu/:menu',
        // 'pt-BR': 'menu/:menu',
      // },
      // 'menu/:menu/submenu/:submenu': {
        // en: 'menu/:menu/submenu/:submenu',
        // 'pt-BR': 'menu/:menu/submenu/:submenu',
      // },
      // 'menu/:menu/submenu/:submenu/:page': {
        // en: 'menu/:menu/submenu/:submenu/:page',
        // 'pt-BR': 'menu/:menu/submenu/:submenu/:page',
      // },
    },
    vueI18n: {
      fallbackLocale: 'pt-BR',
      messages: messages
    }
  },

  // Vuetify module configuration: https://go.nuxtjs.dev/config-vuetify
  vuetify: {
    customVariables: ['~/assets/variables.scss'],
    theme: {
      dark: false,
      themes: {
        dark: {
          primary: colors.blue.darken2,
          accent: colors.grey.darken3,
          secondary: colors.amber.darken3,
          info: colors.teal.lighten1,
          warning: colors.amber.base,
          error: colors.deepOrange.accent4,
          success: colors.green.accent3
        }
      }
    },
  },

	// Build Configuration: https://go.nuxtjs.dev/config-build
	build: {
		//You can extend webpack config here
		// loaders: {
			// sass: {
				// implementation: require('sass'),
			// },
		// },
		extend (config, ctx) {
			const home = config.resolve.alias['~']
			config.resolve.alias['~api'] = home + '/helpers/api' 
		}
	},

	proxy: _isdev ? {
		'/api': 'http://127.0.0.1:8000/',
	} : null,

	transpileDependencies: [
		'vuetify'
	],

  publicRuntimeConfig: {
    email: process.env.EMAIL,
    phone_number: process.env.PHONE_NUMBER,
    company_name: process.env.COMPANY_NAME,
  },	

  generate: {
    exclude: [
      /^\/admin/
    ],
    // generate routes with dynamic params
    routes: function() {
      return axios
        .get(process.env.GENERATE_PROXY_URL + "/api/core/get_menus_submenus_and_pages")
        .then(res => {

          let menus_only = []
          let submenu_routes = []
          let page_routes = []

          // let basic_routes = [  // TODO This is possible?
            // {route: '/', payload: {menus: menus_only}},
            // {route: '/en', payload: {menus: menus_only}},
          // ]

          res.data.forEach(menu => {
            // menus_only
            let menu_only = (({ id, slug, title, icon, to }) => ({ id, slug, title, icon, to }))(menu)
            let menu_only__en = (({ id, slug, title, icon, to }) => ({ id, slug, title, icon, to }))(menu_only)
            menu_only__en.to = '/en' + menu_only__en.to
            menus_only.push(menu_only, menu_only__en)
            //-------/ submenu
            submenu_routes
            menu.submenus.forEach(submenu=>{
                submenu.pages.forEach(page=>{
                  let page_with_md_file = (({ id, slug, submenu, title, description, image, markdown_text, to }) => ({ id, slug, submenu, title,
                      description, image, markdown_text, to }))(page)
                  page_routes.push({route: page_with_md_file.to, payload: {page: page_with_md_file}})
                  page_routes.push({route: '/en' + page_with_md_file.to, payload: {page: page_with_md_file}})
                  delete page.markdown_text
                })
                submenu_routes.push(
                  {route: submenu.to, payload: {allPagesItems: submenu.pages}},
                  {route: '/en' + submenu.to, payload: {allPagesItems: submenu.pages}},
                )
            })

            menu.submenus.forEach(el=> delete el.pages)
          })

          // let all_routes = menus_only.concat(submenu_routes, page_routes, basic_routes)
          let all_routes = menus_only.concat(submenu_routes, page_routes)
          return all_routes 
        });
    }
  }
}
