import axios from 'axios'

const API_URL

if (process.NODE_ENV === 'production') {
    // SWAP OUT WITH PUBLIC API
    API_URL = 'http://istcsxfe01.ist.psu.edu:8080/api'
}
else {
    API_URL = 'http://localhost:8000/api'
}

export default () => {
  return axios.create({
    baseURL: 'http://127.0.0.1:8000/api/',
    withCredentials: false,
    headers: {
      Accept: 'application/json',
      'Content-Type': 'application/json'
    }
  })
}
