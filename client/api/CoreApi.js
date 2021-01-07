import axios from 'axios'

export default () => {
  return axios.create({
    baseURL: 'http://istcsxfe01.ist.psu.edu:8000/api/',
    withCredentials: false,
    headers: {
      Accept: 'application/json',
      'Content-Type': 'application/json'
    }
  })
}
