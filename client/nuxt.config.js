export default {
config: {
nuxt: {
host: "0.0.0.0",
port: "3000"
}
},
    mode: 'universal',
    /*
     ** Headers of the page
     */
    head: {
        title: process.env.npm_package_name || '',
        meta: [
            { charset: 'utf-8' },
            {
                name: 'viewport',
                content: 'width=device-width, initial-scale=1'
            },
            {
                hid: 'description',
                name: 'description',
                content: process.env.npm_package_description || ''
            }
        ],
        link: [{ rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' }]
    },
    /*
     ** Customize the progress-bar color
     */
    loading: { color: '#30769E' },
    /*
     ** Global CSS
     */
    css: ['assets/scss/custom.scss'],
    /*
     ** Plugins to load before mounting the App
     */
    plugins: ['~/plugins/axios'],
    /*
     ** Nuxt.js dev-modules
     */
    buildModules: [
        // Doc: https://github.com/nuxt-community/eslint-module
        '@nuxtjs/eslint-module'
    ],
    /*
     ** Nuxt.js modules
     */
    modules: [
        '@nuxtjs/vuetify',
        // Doc: https://axios.nuxtjs.org/usage
        '@nuxtjs/axios',
        '@nuxtjs/pwa',
        ['@nuxtjs/recaptcha', {
            hideBadge: true,
            siteKey: process.env.RECAPTCHA_SITE_KEY,
            version: 3,
        }],
        '@nuxtjs/style-resources'
    ],

    /*
     ** Axios module configuration
     ** See https://axios.nuxtjs.org/options
     */
    axios: {
        baseURL: '/api',
    },

    vuetify: {
        defaultAssets: {
            font: true,
            icons: 'md'
        },
        icons: {
            iconfont: 'md'
        }
    },
    /*
     ** Build configuration
     */
    build: {
        /*
         ** You can extend webpack config here
         */
        extend(config, ctx) {
            config.module.rules.push({
                enforce: 'pre',
                test: /\.(js|vue)$/,
                loader: 'eslint-loader',
                exclude: /(node_modules)/,
                options: {
                    fix: true
                }
            });
        }
    },

    privateRuntimeConfig: {
        axios: {
            baseURL: '/api'
        }
    }
};
