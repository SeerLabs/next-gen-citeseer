import axios from 'axios'

var API_URL

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

instance.interceptors.request.use((config) => {
    console.log(config.headers);
    }, (error) => {
    return Promise.reject(error);
});

export default instance
