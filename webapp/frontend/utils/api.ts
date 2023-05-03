const baseUrl = process.env.NODE_ENV === 'production' ? 'https://example.com' : 'http://127.0.0.1:5001/stat-arb-9bc39/us-central1'

async function getHeaders() {
  return {
    'Authorization': `Bearer ${(await $auth.currentUser?.getIdToken())}`
  }
}

export default {
  async getHighZScorePairs() {
    return await $fetch(`${baseUrl}/getComparisonPairs`, {
      headers: await getHeaders()
    })
  },
  async getComparison(tickerA: string, tickerB: string) {
    return await $fetch(`${baseUrl}/getComparison`, {
      params: { tickerA, tickerB },
      headers: await getHeaders()
    })
  }
}