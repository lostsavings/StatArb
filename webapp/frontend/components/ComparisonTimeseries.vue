<template>
  <div>
    <h1 class="text-center">{{ tickerA }} - {{ tickerB }}</h1>
    <div>
      <Timeseries v-if="chartData" :chartData="chartData" class="h-72"/>
    </div>
  </div>
</template>

<script setup lang="ts">
import { collection, doc } from 'firebase/firestore'

const props = defineProps<{
  tickerA: string,
  tickerB: string
}>()

const db = useFirestore()
const statdata = collection(db, 'statdata')
const comparisonData = useDocument(doc(statdata, `${props.tickerA}_${props.tickerB}`)).data

const chartData = computed(() => {
  if (!comparisonData.value) {
    return null
  }

  const data = comparisonData?.value.items
  const labels = data.map(e => e.tradeDate_)
  let datasets = [
    {
      label: 'Spread',
      data: data.map(e => e.ratio_),
      borderColor: 'green',
    },
    {
      label: 'Rolling Mean Spread',
      data: data.map(e => e.meanRatio_),
      borderColor: 'red',
    },
    {
      label: 'Rolling 3 std dev upper',
      data: data.map(e => e.upBand_),
      borderColor: 'blue',
    },
    {
      label: 'Rolling 3 std dev lower',
      data: data.map(e => e.downBand_),
      borderColor: 'blue',
    },
    {
      label: 'Market width upper',
      data: data.map(e => e.upHurdle_),
      borderColor: 'orange',
    },
    {
      label: 'Market width lower',
      data: data.map(e => e.downHurdle_),
      borderColor: 'orange',
    },
  ]

  datasets = datasets.map(e => ({
    ...e,
    pointStyle: false,
    backgroundColor: e.borderColor
  }))

  return {
    labels,
    datasets
  }
})
</script>
