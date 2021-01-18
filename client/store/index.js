export default {
    state : () => ({
        reCaptchaSiteKey: "6LdjreIZAAAAACuiEgvWpl8EFFeI-EaO5x_Fozst",
        displayNotification: false,
        notificationText: "",
        notificationType: "success"
    }),

    getters : {

    },

    mutations: {
        showNotification (state, {text, type}) {
            state.displayNotification = true;
            state.notificationText = text;
            state.notificationType = type;
        },

        closeNotification (state) {
            state.displayNotification = false;
            state.notificationText = null
            state.notificationType = null
        }
    }
}
