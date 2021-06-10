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

    registerUser(email, password, fullName, organization="", department="", webpage="", country="", state="") {
        const config = {headers: {
            'content-type': 'application/x-www-form-urlencoded;charset=utf-8'
        }}

        return CoreApi().post('/register', qs.stringify({password, email, "full_name": fullName, organization, department, "web_page": webpage, country, state}), config)
        .then(function(response) {
            return response;
        })
        .catch(function(error) {
            return error;
        });
    },
    correct_metadata(token, id, title = "", authors = [], abstract="", venue="", venueType="", year=0, volume="", number="", pages="", publisher="", pubAddress="", techReportNum="") {
        const config = {
            headers: {
                "Authorization": `Bearer ${token}`
            }
        }
        if (!venue){
            venue=""
        }
        if (!year){
            year=0
        }
        if (!authors){
            authors = []
        }
        if (!title){
            title = ""
        }
        if (!abstract){
            abstract=""
        }
        return CoreApi().post('/correct_metadata', {id, title, authors, abstract, venue, "venue_type": venueType, year, volume, number, pages, publisher, "pub_address": pubAddress, "tech_report_num": techReportNum}, config)
        .then(function(response) {
            return response;
        })
        .catch(function(error) {
            return error;
        });
    },
    edit_new(token, paperId, reasonOrDetails = "", title = "", abstract="", authors = [], meeting="", publisher="", publishDate="") {
        const config = {
            headers: {
                "Authorization": `Bearer ${token}`
            }
        }
        if (!paperId){
            paperId = ""
        }
        if (!reasonOrDetails){
            reasonOrDetails = ""
        }
        
        if (!authors){
            authors = []
        }
        if (!title){
            title = ""
        }
        if (!abstract){
            abstract=""
        }
        if (!meeting){
            meeting=""
        }
        if (!publisher){
            publisher=""
        }
        if (!publishDate){
            publishDate=""
        }

        return CoreApi().post('/edit/new', {"paper_id": paperId, "reason_or_details": reasonOrDetails, title, abstract, authors, meeting, publisher, "publish_date": publishDate}, config)
        .then(function(response) {
            return response;
        })
        .catch(function(error) {
            return error;
        });
    },
    get_correct_metadatas(){
        return CoreApi().get('/get_correct_metadatas')
        .then(function(response) {
            return response;
        })
        .catch(function(error) {
            return error;
        });
    },
    get_edit_requests(token){
        const config = {
            headers: {
                "Authorization": `Bearer ${token}`
            }
        }
        return CoreApi().get('/edit/get_pending', config)
        .then(function(response) {
            return response;
        })
        .catch(function(error) {
            return error;
        });
    },
    get_edit_archived(token){
        const config = {
            headers: {
                "Authorization": `Bearer ${token}`
            }
        }
        return CoreApi().get('/edit/get_archived', config)
        .then(function(response) {
            return response;
        })
        .catch(function(error) {
            return error;
        });
    },
    edit_commit(token, requestID = "", reviewerComment = ""){
        const config = {
            headers: {
                "Authorization": `Bearer ${token}`
            }
        }
        if (!requestID){
            requestID = ""
        }
        if (!reviewerComment){
            reviewerComment = ""
        }
        return CoreApi().post('/edit/commit', {"request_id" : requestID, "reviewer_comment": reviewerComment}, config)
        .then(function(response) {
            return response;
        })
        .catch(function(error) {
            return error;
        });
    },
    edit_deny(token, requestID, reviewerComment) {
        const config = {
            headers: {
                "Authorization": `Bearer ${token}`
            }
        }
        if (!requestID){
            requestID = ""
        }
        if (!reviewerComment){
            reviewerComment = "deny"
        }
        

        return CoreApi().post('/edit/deny', {"request_id": requestID, "reviewer_comment": reviewerComment}, config)
        .then(function(response) {
            return response;
        })
        .catch(function(error) {
            return error;
        });
    },
       
       

    loginUser(email, password, grant_type="", scope="", client_id="", client_secret="") {
        const config = {headers: {
            'content-type': 'application/x-www-form-urlencoded;charset=utf-8'
        }}
        
        return CoreApi().post('/login', qs.stringify({email, password}), config)
            .then(function(response) {
                return response
            })
    },
    loginAdmin(username, password) {
        const config = {headers: {
            'content-type': 'application/x-www-form-urlencoded;charset=utf-8'
        }}
        
        return CoreApi().post('/admin_login', qs.stringify({username, password}), config)
            .then(function(response) {
                return response
            })
    },

    activateUser(token) {
        const config = {
            headers: {
                "Authorization": `Bearer ${token}`
            }
        }
 
        return CoreApi().post(`/activate_account`, {}, config)
            .then(function(response) {
                return response
            })
            .catch(function(error) {
                // eslint-disable-next-line
                console.error(error);
            })
    },

    sendPasswordResetEmail(email) {
        const config = {headers: {
            'content-type': 'application/x-www-form-urlencoded;charset=utf-8'
        }}

        return CoreApi().post('/password_reset_email', qs.stringify({email}), config)
        .then(function(response) {
            return response
        })
    },

    resetPassword(newPassword, token) {
        const config = {headers: {
            'content-type': 'application/x-www-form-urlencoded;charset=utf-8',
            "Authorization": `Bearer ${token}`
        }}
        return CoreApi().post('/reset_password', qs.stringify({"new_password": newPassword}), config)
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
    addCollectionName(token, collectionName="") {
        const options = {
            headers: {
                "Authorization": `Bearer ${token}`
            }
        }

        return CoreApi().put(`/collection/name?collection_name=${collectionName}`, {}, options)
        .then(function(response) {
            return response
        })
        .catch(function(error) {
            // eslint-disable-next-line
            console.error(error);
        })
    },
    renameCollection(token, currCollectionName, newCollectionName) {
        const config = {
            headers: {
                "Authorization": `Bearer ${token}`
            }
        }

        return CoreApi().put(`/collection/rename?collection_name=${currCollectionName}&new_collection_name=${newCollectionName}`, {}, config)
        .then(function(response) {
            return response
        })
        .catch(function(error) {
            // eslint-disable-next-line
            console.error(error);
        })
    },
    deleteACollection(token, collectionName) {
        const options = {
            headers: {
                "Authorization": `Bearer ${token}`
            }
        }

        return CoreApi().delete(`/collection/name?collection_name=${collectionName}`, options)
        .then(function(response) {
            return response
        })
        .catch(function(error) {
            // eslint-disable-next-line
            console.error(error);
        })
    },
    
    addPaperToCollection(token, pid, collectionName="") {
        const options = {
            headers: {
                "Authorization": `Bearer ${token}`
            }
        }

        return CoreApi().put(`/collection/paper?pid=${pid}&collection_name=${collectionName}`, {}, options)
        .then(function(response) {
            return response
        })
        
    },

    deletePaperFromCollection(token, pid, collectionName) {
        const options = {
            headers: {
                "Authorization": `Bearer ${token}`
            }
        }

        return CoreApi().delete(`/collection/paper?pid=${pid}&collection_name=${collectionName}`, options)
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

        return CoreApi().put(`/liked_paper/${pid}`, {}, options)
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

