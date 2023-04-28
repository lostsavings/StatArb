import pandas as pd
import requests
import numpy as np
import datetime
import matplotlib.pyplot as plt
from datetime import date, timedelta
import seaborn as sns

plt.style.use('ggplot')

#Pull data from ORATS
url = 'https://api.orats.io/datav2/hist/cores'
params = {
    'token': '8ea8d461-2ce6-4bac-bf67-3f24647efbad',
    'ticker': 'GOOG,AAPL',
    'fields': 'ticker,tradeDate,iv30d,mktWidthVol,'
}
res = requests.get(url, params=params).json()

#Convering dict format to dataframe
df = pd.DataFrame.from_dict(res["data"])
cols_to_keep = ['ticker','tradeDate','iv30d','mktWidthVol']
memeDf = df[cols_to_keep]

memeDf["tradeDate"] = pd.to_datetime(memeDf["tradeDate"])

memeDf = memeDf[memeDf.tradeDate > datetime.datetime.now() - pd.to_timedelta('200Day')]

#Formating GME data and adding some columns)
memeDf = pd.pivot_table(memeDf, index = 'tradeDate', columns = 'ticker', values = ['ticker','tradeDate','iv30d','mktWidthVol']).reset_index()

#Calculating the metrics we wanna see
memeDf['ratio'] = memeDf['iv30d']['AAPL'] / memeDf['iv30d']['GOOG']
memeDf['meanRatio'] = abs(memeDf['ratio'].rolling(40).mean())
memeDf['absSpread'] = abs(memeDf['iv30d']['AAPL'] - memeDf['iv30d']['GOOG'])
memeDf['stdDev'] = memeDf['ratio'].rolling(40).std()
memeDf['zScore'] = (memeDf['ratio'] - memeDf['meanRatio']) / memeDf['stdDev']
memeDf['upBand'] = memeDf['meanRatio'] + (memeDf['stdDev'] * 3)
memeDf['downBand'] = memeDf['meanRatio'] - (memeDf['stdDev'] * 3)
memeDf['upHurdle'] = memeDf['upBand'] + (memeDf['mktWidthVol']['GOOG'] / memeDf['iv30d']['GOOG'])
memeDf['downHurdle'] = memeDf['downBand'] - (memeDf['mktWidthVol']['GOOG'] / memeDf['iv30d']['GOOG'])


pd.set_option('display.max_colwidth', None)

memeDf.columns = memeDf.columns.map('_'.join)
print(memeDf)

plt.style.use('ggplot')
plt.plot(memeDf['tradeDate_'], memeDf['ratio_'], color='green',label = 'Spread')
plt.plot(memeDf['tradeDate_'], memeDf['meanRatio_'], color='red', label = 'Rolling Mean Spread')
plt.plot(memeDf['tradeDate_'], memeDf['upBand_'], color='blue', label = 'Rolling 3 std dev')
plt.plot(memeDf['tradeDate_'], memeDf['downBand_'], color='blue')
plt.plot(memeDf['tradeDate_'], memeDf['upHurdle_'], color='orange', label = 'market width')
plt.plot(memeDf['tradeDate_'], memeDf['downHurdle_'], color='orange')


plt.xlabel("date")
plt.ylabel("stuff")
plt.title('dashboard')
plt.legend(loc='best')
plt.show()







