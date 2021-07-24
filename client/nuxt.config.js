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
        link: [
            { 
                rel: 'icon',
                type: 'image/x-icon',
                href: '/favicon.ico',
            },
            {
                rel: 'stylesheet',
                href: 'https://fonts.googleapis.com/css2?family=Open+Sans:wght@300;400;600;700&display=swap',
            }
        ]
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
        '@nuxtjs/eslint-module',
        '@nuxtjs/vuetify',
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
            siteKey: process.env.RECAPTCHA_SITE_KEY, // || '6LdjreIZAAAAACuiEgvWpl8EFFeI-EaO5x_Fozst',
            version: 3,
        }],
        '@nuxtjs/style-resources'
    ],

    /*
     ** Axios module configuration
     ** See https://axios.nuxtjs.org/options
     */
    axios: {
        baseURL: process.env.DEBUG ? 'http://localhost:8000/api' : '/api',
    },

    vuetify: {
        defaultAssets: {
            font: true,
            icons: 'md'
        },
        icons: {
            iconfont: 'md'
        },
        theme: {
            options: {
                customProperties: true,
            },
            themes: {
                light: {
                    primary: {
                        base: '#2882A6',
                        lighten3: '#68A7C0',
                        lighten5: '#93C0D2',
                    },
                    secondary: {
                        base:'#FFFFFF',
                        darken3: '#BBBBBB',
                        darken5: '#7D7D7D',
                    },
                    tertiary: '#101A1D',
                    accent: '#E8871E',
                    error: '#D33D49',
                }
            }
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
            baseURL: process.env.DEBUG ? 'http://localhost:8000/api' : '/api',
        }
    }
};
