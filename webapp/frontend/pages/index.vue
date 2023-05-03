<template>
  <div>
    <div v-for="(e, i) in comparisonList?.items" class="w-1/3 h-80 inline-block p-2">
      <ComparisonTimeseries :ticker-a="e.ticker_a" :ticker-b="e.ticker_b" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { collection, doc } from 'firebase/firestore'

definePageMeta({
  middleware: ['auth'],
})

const db = useFirestore()
const statdata = collection(db, 'statdata')
const comparisonList = useDocument(doc(statdata, 'comparison_list')).data
</script>