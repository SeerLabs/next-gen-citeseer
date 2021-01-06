import axios from 'axios'

export default () => {
  return axios.create({
    baseURL: 'http://lrs-giles05:8000/api/',
    withCredentials: false,
    headers: {
      Accept: 'application/json',
      'Content-Type': 'application/json'
    }
  })
}
