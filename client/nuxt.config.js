import { stubFalse } from 'lodash';

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
            { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' },
            { rel: 'stylesheet', href: 'https://fonts.googleapis.com/css2?family=Bitter:wght@400;600;700&family=Open+Sans:wght@300;400&display=swap' }
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
    plugins: [{ src: '~/plugins/persistedState.client.js' }, '~/plugins/axios'],
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

        'nuxt-vuex-localstorage',
        ['@nuxtjs/recaptcha', {
            hideBadge: true,
            siteKey: '6LdjreIZAAAAACuiEgvWpl8EFFeI-EaO5x_Fozst',
            version: 3,
        }],
        '@nuxtjs/style-resources'
    ],

    /*
     ** Axios module configuration
     ** See https://axios.nuxtjs.org/options
     */
    axios: {
        baseURL: 'http://localhost:8000/api',
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
                        base: '#2593BD',
                        lighten3: '#4496C5',
                        lighten5: '#63A7CF',
                    },
                    secondary: {
                        base: '#707070',
                        lighten3: '#8d8d8d',
                        lighten5: '#bebebe',
                    },
                    tertiary: '#101A1D',
                    accent: '#FAC748',
                    error: '#D33D49',
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
                baseURL: 'http://localhost:8000/api'
            }
        }
    }
}
