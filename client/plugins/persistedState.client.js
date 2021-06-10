import createPersistedState from 'vuex-persistedstate'
 
export default ({store}) => {
  createPersistedState({
    paths: ['auth', 'admin_auth']
  })(store)
}
