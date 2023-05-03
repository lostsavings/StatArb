import * as functions from 'firebase-functions'
import * as express from 'express'
import * as cors from 'cors'

import { Storage } from '@google-cloud/storage'
import { initializeApp } from 'firebase-admin/app'
import { getAuth } from 'firebase-admin/auth'

const app = express()
app.use(cors())

const storage = new Storage()
const bucket = storage.bucket('stat-arb-data')

const fbApp = initializeApp(functions.config().firebase)
const auth = getAuth(fbApp)

async function authenticateToken(req: any, res: any, next: any) {
  const idToken = req.headers.authorization?.split('Bearer ')[1]
  if (!idToken) {
    res.status(401).send('Unauthorized')
  }
  try {
    const decodedToken = await auth.verifyIdToken(idToken)
    req.user = decodedToken
    next()
  } catch (e) {
    res.status(401).send('Unauthorized')
  }
}

app.use(authenticateToken)

app.get('getComparisonPairs', async (request, response) => {
  const file = bucket.file('comparison_list.json')
  const [contents] = await file.download()
  response.send(contents.toString())
})

app.get('getComparison', async (request, response) => {
  const { tickerA, tickerB } = request.query

  const file = bucket.file(`comparisons/${tickerA}_${tickerB}.json`)
  const [contents] = await file.download()
  response.send(contents.toString())
})

export const api = functions.https.onRequest(app)