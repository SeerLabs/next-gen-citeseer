/*
auth: {
    strategies: {
        local: {
            endpoints: {
                register: { url: 'http://localhost:8001/api/auth/register', method: 'post', propertyName: false },
                login: { url: 'http://localhost:8001/api/auth/login', method: 'post', propertyName: false },
                profile: { url: 'http://localhost:8001/api/auth/user_profile', method: 'get', propertyName: false},
                logout: false
            }
        }
    }
},
*/

import qs from 'qs'
import CoreApi from './CoreApi'

export default {
    checkRecaptcha(token) {
        return CoreApi().get(`/recaptcha?token=${token}`) 
        .then(function(response) {
            return response;
        })
        .catch(function(error) {
            // eslint-disable-next-line
            console.error(error);
        })
    },

    registerUser(username, password, email, fullName, organization="", department="", webpage="", country="", state="") {
        return CoreApi().post('/register', {username, password, email, "full_name": fullName, organization, department, "web_page": webpage, country, state})
        .then(function(response) {
            return response;
        })
        .catch(function(error) {
            // eslint-disable-next-line
            console.error(error);
        });
    },

    loginUser(username, password, grant_type="", scope="", client_id="", client_secret="") {
        const config = {headers: {
            'content-type': 'application/x-www-form-urlencoded;charset=utf-8'
        }}
        
        console.log("Logging in user");
        console.log(username, password);
        return CoreApi().post('/login', qs.stringify({username, password, grant_type, scope, client_id, client_secret}), config)
            .then(function(response) {
                return response
            })
            .catch(function(error) {
                // eslint-disable-next-line
                console.error(error);
            })
    },

    getUserProfile(token) {
        const options = {
            headers: {
                "Authorization": `Bearer ${token}`
            }
        }

        return CoreApi().get('/user_profile', options)
        .then(function(response) {
            return response
        })
        .catch(function(error) {
            // eslint-disable-next-line
            console.error(error);
        })
    },

    addToCollection(token, pid, collection="") {
        return CoreApi().post('/collection', pid, collection)
        .then(function(response) {
            return response
        })
        .catch(function(error) {
            // eslint-disable-next-line
            console.error(error);
        })
    },

    addMoniterPaper(token, pid) {
        return CoreApi().post(`/user_profile/${pid}`)
        .then(function(response) {
            return response
        })
        .catch(function(error) {
            // eslint-disable-next-line
            console.error(error);
        })
    },

    addLikedPaper(token, pid) {
        return CoreApi().post(`/user_profile/${pid}`)
        .then(function(response) {
            return response
        })
        .catch(function(error) {
            // eslint-disable-next-line
            console.error(error);
        })
    },
}

