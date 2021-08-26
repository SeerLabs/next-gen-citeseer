export default {
    state : () => ({
        reCaptchaSiteKey: "6LfmtpgaAAAAAI9u-W21_48xQqUIo_z3lBjxJAC8",
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
