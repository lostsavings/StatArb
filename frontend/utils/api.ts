export default {
  async getHighZScorePairs() {
    return await $fetch('/data/comparison_list.json')
  },
  async getComparison(tickerA: string, tickerB: string) {
    return await $fetch(`/data/tickers/${tickerA}_${tickerB}.json`)
  }
}