<template>
  <div>
    <div
      v-for="(e, i) in comparisonList?.items"
      class="w-full sm:w-1/2 lg:w-1/3 inline-block p-4"
    >
      <ComparisonTimeseries :ticker-a="e.ticker_a" :ticker-b="e.ticker_b" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { collection, doc } from 'firebase/firestore'

definePageMeta({
  middleware: ['require-login'],
})

const db = useFirestore()
const statdata = collection(db, 'statdata')
const comparisonList = useDocument(doc(statdata, 'comparison_list')).data
</script>