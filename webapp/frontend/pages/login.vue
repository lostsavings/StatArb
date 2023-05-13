<template>
  <div class="text-center">
    <form class="text-left mt-10 p-5 mx-auto w-80" @submit.prevent="submit">
      <div class="space-y-3">
        <InputWrapper v-model="email" label="Email" type="email" required />
        <InputWrapper v-model="password" label="Password" type="password" required />
      </div>
      <button type="submit" class="signature-gradient rounded py-2 mt-5 block w-full">Log In</button>
      <p v-if="errMessage" class="text-red-400 mt-2">{{ errMessage }}</p>
    </form>
  </div>
</template>

<script setup lang="ts">
import { signInWithEmailAndPassword  } from 'firebase/auth'

// NOTE: this will only work on the client side
const auth = useFirebaseAuth()!
const route = useRoute()

const email = ref('')
const password = ref('')
const errMessage = ref('')

function submit() {
  errMessage.value = ''
  signInWithEmailAndPassword(auth, email.value, password.value)
    .then(() => {
      let redirect = route.query.redirect
      if (Array.isArray(redirect)) {
        redirect = redirect[0]
      }
      const r = redirect || '/home'
      navigateTo(r)
    })
    .catch(err => {
      errMessage.value = 'Unable to login.'
    })
}

</script>