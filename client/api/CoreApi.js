import axios from 'axios'
import { load } from 'recaptcha-v3'

let API_URL

if (process.env.NODE_ENV === 'production') {
    // SWAP OUT WITH PUBLIC API
    API_URL = 'http://localhost:8080/api'
}
else {
    API_URL = 'http://localhost:8000/api'
}

const instance = axios.create({
    baseURL: API_URL,
    withCredentials: false,
    headers: {
      Accept: 'application/json',
      'Content-Type': 'application/json'
    }
  })

instance.interceptors.request.use(async (config) => {
    const recaptcha = await load('6LdjreIZAAAAACuiEgvWpl8EFFeI-EaO5x_Fozst');
    const token = await recaptcha.execute('login');

    config.headers.common.token = token;
    
    return config;
    }, (error) => {
    return Promise.reject(error);
});

export default () => { return instance }
