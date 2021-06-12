export const state = () => ({
    loggedIn: false,
    username: "",
    token: ""
})

export const mutations = {
    admin_login(state, user) {
        state.loggedIn = true;
        state.username = user.username;
        state.token = user.access_token;
    },

    admin_logout(state) {
        state.loggedIn = false;
        state.user = null;
        state.token = "";
    }
}