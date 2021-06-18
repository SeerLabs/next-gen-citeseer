export const state = () => ({
    loggedIn: false,
    user: null,
    token: ""
})

export const mutations = {
    login(state, user) {
        state.loggedIn = true;
        state.user = user;
        state.token = user.access_token;
    },

    logout(state) {
        state.loggedIn = false;
        state.user = null;
        state.token = "";
    }
}