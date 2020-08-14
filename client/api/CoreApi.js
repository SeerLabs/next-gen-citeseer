import axios from 'axios';

export default () => {
    return axios.create({
        baseURL: 'http://127.0.0.1:8002/api/',
        withCredentials: false,
        headers: {
            Accept: 'application/json',
            'Content-Type': 'application/json'
        }
    });
};
