// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  ssr: false,
  css: ['~/assets/css/main.css'],
  postcss: {
    plugins: {
      tailwindcss: {},
      autoprefixer: {},
    },
  },
  modules: [
    'nuxt-vuefire'
  ],
  // @ts-ignore
  vuefire: {
    auth: true,
    config: {
      apiKey: "AIzaSyD9vHAEG9U1ny8OEH8IxQtcZCEDrcjhvWg",
      authDomain: "stat-arb-9bc39.firebaseapp.com",
      projectId: "stat-arb-9bc39",
      storageBucket: "stat-arb-9bc39.appspot.com",
      messagingSenderId: "938724022260",
      appId: "1:938724022260:web:139d76f81c4d81a29f4ba1"
    }
  }
})
