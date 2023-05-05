<template>
  <div>
    <form class="text-left mt-10 p-5 mx-auto w-80" @submit.prevent="submit">
      <div class="space-y-3">
        <InputWrapper v-model="email" label="Email" type="email" required />
        <InputWrapper v-model="password" label="Password" type="password" required />
        <InputWrapper v-model="passwordConfirm" label="Confirm Password" type="password" required />
      <p v-if="!checkPasswordsMatch()" class="text-red-400 mt-2">Passwords don't match.</p>
      </div>
      <button type="submit" class="signature-gradient rounded py-2 mt-5 block w-full">Sign Up</button>
      <p v-if="errMessage" class="text-red-400 mt-2">{{ errMessage }}</p>
    </form>
  </div>
</template>
<script setup lang="ts">
import { createUserWithEmailAndPassword } from 'firebase/auth'

// NOTE: this will only work on the client side
const auth = useFirebaseAuth()!
const route = useRoute()

const email = ref('')
const password = ref('')
const passwordConfirm = ref('')
const errMessage = ref('')

function checkPasswordsMatch() {
  // do not show passwords as not matching until user types in confirm box
  return !passwordConfirm.value || password.value === passwordConfirm.value
}

function submit() {
  errMessage.value = ''
  createUserWithEmailAndPassword(auth, email.value, password.value)
    .then(() => {
      let redirect = route.query.redirect
      if (Array.isArray(redirect)) {
        redirect = redirect[0]
      }
      const r = redirect || '/home'
      navigateTo(r)
    })
    .catch(err => {
      errMessage.value = 'Unable to sign up.'
    })
}
</script>