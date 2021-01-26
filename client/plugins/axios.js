export default function ({ $axios, $recaptcha, redirect }) {
    $axios.onRequest(async (config) => {
        await $recaptcha.init()
        const token = await $recaptcha.execute('login')
        config.headers.common.token = token;
        
        return config;

    })
  
    $axios.onError(error => {
      const code = parseInt(error.response && error.response.status)
      if (code === 400) {
        redirect('/400')
      }
    })
  }
  