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
            return error;
        });
    },

    loginUser(username, password, grant_type="", scope="", client_id="", client_secret="") {
        const config = {headers: {
            'content-type': 'application/x-www-form-urlencoded;charset=utf-8'
        }}
        
        return CoreApi().post('/login', qs.stringify({username, password, grant_type, scope, client_id, client_secret}), config)
            .then(function(response) {
                return response
            })
    },

    activateUser(token) {
        return CoreApi().post(`/activate_account?token=${token}`)
            .then(function(response) {
                return response
            })
            .catch(function(error) {
                // eslint-disable-next-line
                console.error(error);
            })
    },

    sendPasswordResetEmail(email) {
        return CoreApi().get(`/password_reset_email?email=${email}`)
        .then(function(response) {
            return response
        })
    },

    resetPassword(newPassword, token) {
        return CoreApi().put(`/reset_password?new_password=${newPassword}&token=${token}`)
        .then(function(response) {
            return response
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
        const options = {
            headers: {
                "Authorization": `Bearer ${token}`
            }
        }

        return CoreApi().put(`/collection?pid=${pid}&collection=${collection}`, options)
        .then(function(response) {
            return response
        })
    },

    deleteFromCollection(token, pid, collection="") {
        const options = {
            headers: {
                "Authorization": `Bearer ${token}`
            }
        }

        return CoreApi().delete(`/collection?pid=${pid}&collection=${collection}`, options)
        .then(function(response) {
            return response
        })
        .catch(function(error) {
            // eslint-disable-next-line
            console.error(error);
        })
    },

    addMoniteredPaper(token, pid) {
        const options = {
            headers: {
                "Authorization": `Bearer ${token}`
            }
        }

        return CoreApi().put(`/moniter_paper/${pid}`, {}, options)
        .then(function(response) {
            return response
        })
    },

    deleteMoniteredPaper(token, pid) {
        const options = {
            headers: {
                "Authorization": `Bearer ${token}`
            }
        }
        
        return CoreApi().delete(`/moniter_paper/${pid}`, options)
        .then(function(response) {
            return response
        })
    },

    addLikedPaper(token, pid) {
        const options = {
            headers: {
                "Authorization": `Bearer ${token}`
            }
        }

        return CoreApi().post(`/liked_paper/${pid}`, {}, options)
        .then(function(response) {
            return response
        })
    },

    deleteLikedPaper(token, pid) {
        const options = {
            headers: {
                "Authorization": `Bearer ${token}`
            }
        }
        
        return CoreApi().delete(`/liked_paper/${pid}`, options)
        .then(function(response) {
            return response
        })
    }
}

