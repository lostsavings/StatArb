<template>
  <div>
    <div v-if="user">
      <div v-for="(e, i) in comparisonList" class="w-1/3 h-80 inline-block p-2">
        <ComparisonTimeseries :ticker-a="e.ticker_a" :ticker-b="e.ticker_b" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { signInWithEmailAndPassword } from 'firebase/auth'
import { httpsCallable } from "firebase/functions"
const { $auth, $functions } = useNuxtApp()

const user = ref(null)

onMounted(async () => {
  $auth.onAuthStateChanged(async (userState) => {
    user.value = userState
    if (!user.value) {
      const email = prompt('Email')
      const password = prompt('Password')
      user.value = (await signInWithEmailAndPassword($auth, email, password)).user
    }
    const api = httpsCallable($functions, 'api')
    api('test')


  })
})

const comparisonList: Ref<any[]> = ref([])
// onMounted(async () => {
//   comparisonList.value = await api.getHighZScorePairs()
// })
</script>