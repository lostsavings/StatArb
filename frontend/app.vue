<template>
  <div>
    <div v-for="(e, i) in comparisonList" class="w-1/3 h-80 inline-block p-2">
      <ComparisonTimeseries :ticker-a="e.ticker_a" :ticker-b="e.ticker_b" />
    </div>
  </div>
</template>

<script setup lang="ts">
let comparisonList: Ref<any[]> = ref([])
onMounted(async () => {
  comparisonList.value = await api.getHighZScorePairs()
})
</script>