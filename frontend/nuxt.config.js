import colors from 'vuetify/es5/util/colors'
import {messages} from './messages'
const _isdev = process.env.DEV
const axios = require("axios");

export default {

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
      // Admin
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
    company_name: process.env.COMPANY_NAME
  },	

  generate: {
    exclude: [
      /^\/admin/ // path starts with /admin
    ],
    // generate routes with dynamic params
    // routes: function() {
      // return axios
        // .get(process.env.BASE_URL + "/api/core/get_menus_submenus_and_pages")
        // .then(res => {
          // const routes = [];
          // for (const key in res.data) {
            // routes.push({
              // route: "/posts/" + key,
              // payload: {postData: res.data[key]}
            // });
          // }
          // return routes;
        // });
    // }
  }
}
