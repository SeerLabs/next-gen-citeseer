import axios from 'axios'

var API_URL

if (process.env.NODE_ENV === 'production') {
    // SWAP OUT WITH PUBLIC API
    API_URL = 'http://istcsxfe01.ist.psu.edu:8080/api'
}
else {
    API_URL = 'http://localhost:8000/api'
}

export default () => {
  return axios.create({
    baseURL: API_URL,
    withCredentials: false,
    headers: {
      Accept: 'application/json',
      'Content-Type': 'application/json'
    }
  })
}
