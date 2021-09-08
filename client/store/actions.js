import qs from 'qs'

export default {
    getPaperWithPaperId ({context}, { pid }) {
      return this.$axios.$get('/paper', { params: {paper_id: pid}})
    },
    
    async getPaperswithPaperIds (context, {pids}) {
    return await this.$axios.$post(`/mget_paper`, {"paper_id_list": pids})
            .then(function(response) {
                return response.response
            })
            .catch(function(error) {
                // eslint-disable-next-line
                console.error(error);
            })
    },

    getPaperWithClusterId (context, { cid }){
      return this.$axios.$get('/paper', {params: {cluster_id: cid}})
    },

    getCitationsEntities (context, { id, page }) {
      return this.$axios.$get('/citations/' + id, { params: { page, pageSize: 10 } })
    },

    getSimilarPaper (context, { id, algo }) {
      return this.$axios.$get('/similar/' + id, { params: {algo}})
    },

    searchPaper(context, { queryString, page, pageSize, includePdfs=true, yearStart=null, yearEnd=null, author=null, publisher=null}) {

        if (yearStart === "0") {
            yearStart = null;
        }
      
        return this.$axios
            .$post('/search', {
                queryString,
                page,
                pageSize,
                must_have_pdf: includePdfs,
                yearStart,
                yearEnd,
                author,
                publisher,
            })
            .catch(function(error) {
                // eslint-disable-next-line
                console.log(error.response);
            });
    },

    getAggregations(context, { queryString }) {
        return this.$axios
                .$post('/aggregate', {
                    queryString
                })
                .catch(function(error) {
                    // eslint-disable-next-line
                    console.log(error.response);
                });    
    },

    searchAuthor(context, { queryString, includePdfs }) {
        return this.$axios
            .$post('/searchAuthor', {
                queryString,
                must_have_pdf: includePdfs
            })
            .catch(function(error) {
                // eslint-disable-next-line
                console.log(error.response);
            });
    },

    getSuggestions(context, { queryString }) {
        return this.$axios
            .$get(`/suggest`, {params: { query: queryString}})
            .then(function(response) {
                return response;
            })
            .catch(function(error) {
                // eslint-disable-next-line
                console.log(error);
            });
    }, 

    getShowCiting (context, { id, page, pageSize, sortBy }) {
        return this.$axios.$get('/showCiting/' + id, { params: { page, pageSize, sort: sortBy } })
    },

    /// /////////// Myciteseer ////////////////////////////
    checkRecaptcha(context, {token}) {
        return this.$axios.$get(`/recaptcha?token=${token}`) 
        .then(function(response) {
            return response;
        })
        .catch(function(error) {
            // eslint-disable-next-line
            console.error(error);
        })
    },

    

    editNew(context, {token, paperId, reasonOrDetails = "", title = "", abstract="", authors = [], meeting="", publisher="", publishDate=""}) {
        const config = {
            headers: {
                "Authorization": `Bearer ${token}`
            }
        }

        return this.$axios.$post('/edit/new', {"paper_id": paperId, "reason_or_details": reasonOrDetails, title, abstract, authors, meeting, publisher, "publish_date": publishDate}, config)
        .then(function(response) {
            return response;
        })
        .catch(function(error) {
            return error;
        });
    },

    getEditRequests(context, {token}){
        const config = {
            headers: {
                "Authorization": `Bearer ${token}`
            }
        }
        return this.$axios.$get('/edit/get_pending', config)
        .then(function(response) {
            return response;
        })
        .catch(function(error) {
            return error;
        });
    },

    getEditArchived(context, {token}){
        const config = {
            headers: {
                "Authorization": `Bearer ${token}`
            }
        }
        return this.$axios.$get('/edit/get_archived', config)
        .then(function(response) {
            return response;
        })
        .catch(function(error) {
            return error;
        });
    },

    editCommit(context, {token, requestID = "", reviewerComment = ""}){
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
        return this.$axios.$post('/edit/commit', {"request_id" : requestID, "reviewer_comment": reviewerComment}, config)
        .then(function(response) {
            return response;
        })
        .catch(function(error) {
            return error;
        });
    },

    editDeny(context, {token, requestID, reviewerComment}) {
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
        

        return this.$axios.$post('/edit/deny', {"request_id": requestID, "reviewer_comment": reviewerComment}, config)
        .then(function(response) {
            return response;
        })
        .catch(function(error) {
            return error;
        });
    },
    authorClaim(context, {token, email, paperId}){
        const config = {
            headers: {
                "Authorization": `Bearer ${token}`
            }
        }
        return this.$axios.$post('/author_claim', {email, "paper_id": paperId}, config)
        .then(function(response) {
            return response;
        })
        .catch(function(error) {
            return error;
        });
 
    },
    updateProfile(context, {email}){
        const config = {headers: {
            'content-type': 'application/x-www-form-urlencoded;charset=utf-8'
        }}
        return this.$axios.$post('/profile/update', qs.stringify({email}), config)
            .then(function(response) {
                return response
            })
    },

    registerUser(context, {email, password, fullName, organization="", department="", webpage="", country="", state=""}) {
        const config = {headers: {
            'content-type': 'application/x-www-form-urlencoded;charset=utf-8'
        }}

        return this.$axios.$post('/register', qs.stringify({password, email, "full_name": fullName, organization, department, "web_page": webpage, country, state}), config)
        .then(function(response) {
            return response;
        })
    },

    loginUser(context, {email, password}) {
        const config = {headers: {
            'content-type': 'application/x-www-form-urlencoded;charset=utf-8'
        }}
        return this.$axios.$post('/login', qs.stringify({email, password}), config)
            .then(function(response) {
                return response
            })
    },
    loginAdmin(context, {username, password}) {
        const config = {headers: {
            'content-type': 'application/x-www-form-urlencoded;charset=utf-8'
        }}
        
        return this.$axios.$post('/admin_login', qs.stringify({username, password}), config)
            .then(function(response) {
                return response
            })
    },

    activateUser(context, {token}) {
        const config = {
            headers: {
                "Authorization": `Bearer ${token}`
            }
        }
 
        return this.$axios.$post(`/activate_account`, {}, config)
            .then(function(response) {
                return response
            })
            .catch(function(error) {
                // eslint-disable-next-line
                console.error(error);
            })
    },

    sendPasswordResetEmail(context, {email}) {
        const config = {headers: {
            'content-type': 'application/x-www-form-urlencoded;charset=utf-8'
        }}

        return this.$axios.$post('/password_reset_email', qs.stringify({email}), config)
        .then(function(response) {
            return response
        })
    },

    resetPassword(context, {newPassword, token}) {
        const config = {headers: {
            'content-type': 'application/x-www-form-urlencoded;charset=utf-8',
            "Authorization": `Bearer ${token}`
        }}
        return this.$axios.$post('/reset_password', qs.stringify({"new_password": newPassword}), config)
        .then(function(response) {
            return response
        })
    },

    getUserProfile(context, {token}) {
        const options = {
            headers: {
                "Authorization": `Bearer ${token}`
            }
        }

        return this.$axios.$get('/user_profile', options)
        .then(function(response) {
            return response
        })
        .catch(function(error) {
            // eslint-disable-next-line
            console.error(error);
        })
    },
    addCollectionName(context, {token, collectionName=""}) {
        const options = {
            headers: {
                "Authorization": `Bearer ${token}`
            }
        }

        return this.$axios.$put(`/collection/name?collection_name=${collectionName}`, {}, options)
        .then(function(response) {
            return response
        })
        .catch(function(error) {
            // eslint-disable-next-line
            console.error(error);
        })
    },
    renameCollection(context, {token, currCollectionName, newCollectionName}) {
        const config = {
            headers: {
                "Authorization": `Bearer ${token}`
            }
        }

        return this.$axios.$put(`/collection/rename?collection_name=${currCollectionName}&new_collection_name=${newCollectionName}`, {}, config)
        .then(function(response) {
            return response
        })
        .catch(function(error) {
            // eslint-disable-next-line
            console.error(error);
        })
    },
    deleteACollection(context, {token, collectionName}) {
        const options = {
            headers: {
                "Authorization": `Bearer ${token}`
            }
        }

        return this.$axios.$delete(`/collection/name?collection_name=${collectionName}`, options)
        .then(function(response) {
            return response
        })
        .catch(function(error) {
            // eslint-disable-next-line
            console.error(error);
        })
    },
    
    addPaperToCollection(context, {token, pid, collectionName=""}) {
        const options = {
            headers: {
                "Authorization": `Bearer ${token}`
            }
        }

        return this.$axios.$put(`/collection/paper?pid=${pid}&collection_name=${collectionName}`, {}, options)
        .then(function(response) {
            return response
        })
        
    },

    deletePaperFromCollection(context, {token, pid, collectionName}) {
        const options = {
            headers: {
                "Authorization": `Bearer ${token}`
            }
        }

        return this.$axios.$delete(`/collection/paper?pid=${pid}&collection_name=${collectionName}`, options)
        .then(function(response) {
            return response
        })
        .catch(function(error) {
            // eslint-disable-next-line
            console.error(error);
        })
    },

    addMoniteredPaper(context, {token, pid}) {
        const options = {
            headers: {
                "Authorization": `Bearer ${token}`
            }
        }

        return this.$axios.$put(`/moniter_paper/${pid}`, {}, options)
        .then(function(response) {
            return response
        })
    },

    deleteMoniteredPaper(context, {token, pid}) {
        const options = {
            headers: {
                "Authorization": `Bearer ${token}`
            }
        }
        
        return this.$axios.$delete(`/moniter_paper/${pid}`, options)
        .then(function(response) {
            return response
        })
    },

    addLikedPaper(context, {token, pid}) {
        const options = {
            headers: {
                "Authorization": `Bearer ${token}`
            }
        }

        return this.$axios.$put(`/liked_paper/${pid}`, {}, options)
        .then(function(response) {
            return response
        })
    },

    deleteLikedPaper(context, {token, pid}) {
        const options = {
            headers: {
                "Authorization": `Bearer ${token}`
            }
        }
        
        return this.$axios.$delete(`/liked_paper/${pid}`, options)
        .then(function(response) {
            return response
        })
    }
}
