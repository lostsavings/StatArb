<template>
  <form class="text-center mt-14" @submit.prevent="submit">
    <label for="email">Email</label>
    <br>
    <input v-model="email" id="email" type="email" class="bg-slate-200 rounded" required>
    <br>
    <label for="password">Password</label>
    <br>
    <input v-model="password" id="password" type="password" class="bg-slate-200 rounded" required>
    <br>
    <button type="submit" class="bg-slate-300 rounded mt-3 px-3 py-1">Submit</button>
    <p class="text-red-500 mt-8">{{ errMessage }}</p>
  </form>
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
      const r = redirect || '/'
      navigateTo(r)
    })
    .catch(err => {
      errMessage.value = 'Unable to log in.'
    })
}

</script>