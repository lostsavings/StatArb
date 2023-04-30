<template>
  <div>
    <Timeseries v-if="chartData" :chartData="chartData" class="h-96" />
  </div>
</template>

<script setup lang="ts">
import { ChartData } from 'chart.js'

let chartData: Ref<ChartData> = ref({
  datasets: []
})

api.getComparison('AAL', 'BAC')
  .then(data => {
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

    chartData.value = {
      labels,
      datasets
    }
  })


</script>
