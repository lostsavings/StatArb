<template>
  <Line
    :data="props.chartData"
    :options="options"
  />
</template>

<script setup lang="ts">
import { Line } from 'vue-chartjs'
import { Chart as ChartJS, Title, Tooltip, Legend, LineElement, CategoryScale, LinearScale, PointElement, ChartData, ChartOptions } from 'chart.js'

ChartJS.register(Title, Tooltip, Legend, LineElement, CategoryScale, LinearScale, PointElement)

const props = defineProps<{
  chartData: ChartData
}>()

const options: Ref<ChartOptions> = ref({
  responsive: true,
  maintainAspectRatio: false,
  backgroundColor: 'transparent',
  plugins: {
    legend: {
      display: false
    }
  }
})

</script>