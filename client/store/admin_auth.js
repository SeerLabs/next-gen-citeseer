export const state = () => ({
    loggedIn: false,
    username: "",
    token: ""
})

export const mutations = {
    loginAdmin(state, user) {
        state.loggedIn = true;
        state.username = user.username;
        state.token = user.access_token;
    },

    logoutAdmin(state) {
        state.loggedIn = false;
        state.user = null;
        state.token = "";
    }
}