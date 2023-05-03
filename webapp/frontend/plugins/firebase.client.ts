import { initializeApp } from 'firebase/app'
import { getAuth } from 'firebase/auth'
import { getDatabase } from 'firebase/database'
import { getFunctions } from 'firebase/functions'

export default defineNuxtPlugin((nuxtApp) => {
  const firebaseConfig = {
    apiKey: "AIzaSyD9vHAEG9U1ny8OEH8IxQtcZCEDrcjhvWg",
    authDomain: "stat-arb-9bc39.firebaseapp.com",
    projectId: "stat-arb-9bc39",
    storageBucket: "stat-arb-9bc39.appspot.com",
    messagingSenderId: "938724022260",
    appId: "1:938724022260:web:139d76f81c4d81a29f4ba1"
  }

  const app = initializeApp(firebaseConfig)

  return {
    provide: {
      auth: getAuth(app),
      db: getDatabase(app),
      functions: getFunctions(app)
    }
  }
})
