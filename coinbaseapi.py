import requests, re 
from pprint import pprint 
from bs4 import BeautifulSoup 
import pandas as pd 
import numpy as np
from datetime import datetime 

url = "https://api.exchange.coinbase.com/products/ETH-USDT/book?level=2"
response = requests.get(url)
data = response.json()

#pprint(data)

ask_masterlist = data['asks']
bid_masterlist = data['bids']

for alist in ask_masterlist:
	alist[0] = float(alist[0])
	alist[1] = float(alist[1])


for blist in bid_masterlist:
	blist[0] = float(blist[0])
	blist[1] = float(blist[1])

df_bid = pd.DataFrame(bid_masterlist,columns=['Bid Price','Bid Size','Bid Amount'])
df_ask = pd.DataFrame(ask_masterlist,columns=['Ask Price','Ask Size','Ask Amount'])
df_bidask = pd.merge(df_bid,df_ask,left_index=True,right_index=True)

df_bidask['Bid-Ask Spread Percentage'] = ((df_bidask['Ask Price'] - df_bidask['Bid Price'])/df_bidask['Ask Price'])*100

#pprint(df_bidask.head())

coinbaseurl2 = "https://api.exchange.coinbase.com/products/ETH-USDT/candles"
r = requests.get(coinbaseurl2)
data2 = r.json()

for candlist in data2: 
	candlist[0] = datetime.fromtimestamp(candlist[0])

df_product = pd.DataFrame(data2,columns=['time','open','high','low','close','volume'])


###minute volatility###

minute_df = pd.concat([df_product['time'],df_product['close'],df_product['open']],axis=1)
minute_df['minute volatility'] = np.log(minute_df['close']) - np.log(minute_df['close'].shift(1))
minute_df_final = minute_df.set_index('time')

#pprint(minute_df_final.head())

###hourly volatility###

hourly_df = pd.concat([df_product['time'],df_product['close'],df_product['open']],axis=1)
hourly_df['time'] = pd.to_datetime(hourly_df['time'])
hourly_df2 = hourly_df[hourly_df['time'].dt.minute == 0]

hourly_df2['hourly volatility'] = np.log(hourly_df2['close']) - np.log(hourly_df2['close'].shift(1))
hourly_df2_final = hourly_df2.set_index('time')

pprint(hourly_df2_final.head())



#hourly_df

