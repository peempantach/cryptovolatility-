import requests, re 
from pprint import pprint 
from bs4 import BeautifulSoup 
import pandas as pd 
import numpy as np
from datetime import datetime 



kraken_url = 'https://api.kraken.com/0/public/Depth?pair=XBTUSD&since=1577836800000' #didnt include timestamp because of timeframe 
#inconsistencies in api and inability to access the api of certain exchanges 
r = requests.get(kraken_url)
data = r.json()

result_dict = data['result']
pairing1_dict= result_dict['XXBTZUSD']

bid_masterlist= pairing1_dict['asks']
ask_masterlist= pairing1_dict['bids']

if len(data['error']) > 0: 
    print("Orderbook error detected")

for alist in bid_masterlist:
    alist[0] = float(alist[0])
    alist[1] = float(alist[1])
    alist[2] = datetime.fromtimestamp(alist[2])

for blist in ask_masterlist:
    blist[0] = float(alist[0])
    blist[1] = float(alist[1])



df_bid = pd.DataFrame(bid_masterlist, columns= ['Bidding Price','Volume','Timestamp'])
df_ask = pd.DataFrame(ask_masterlist, columns= ['Asking Price','Volume','Timestamp'])
df_bidask = pd.concat([df_bid,df_ask['Asking Price']],axis=1)
df_bidask['Bid-Ask Spread Percentage'] = ((df_bidask['Asking Price'] - df_bidask['Bidding Price'])/df_bidask['Asking Price'])*100
df_bidask_final = df_bidask.set_index('Timestamp')

pprint(df_bidask_final)

kraken_url2 = 'https://api.kraken.com/0/public/OHLC?pair=XBTUSD&since=1577836800000'

r2 = requests.get(kraken_url2)
data2 = r2.json()

#pprint(data2)

result_dict2 = data2['result']
pairing1_dict2 = result_dict2['XXBTZUSD']
#pprint(pairing1_dict2)

for alist2 in pairing1_dict2:
    alist2[0] = datetime.fromtimestamp(alist2[0])
    alist2[1] = float(alist2[1])
    alist2[2] = float(alist2[2])
    alist2[3] = float(alist2[3])
    alist2[4] = float(alist2[4])
    alist2[5] = float(alist2[5])
    alist2[6] = float(alist2[6])
    

df_ohlc = pd.DataFrame(pairing1_dict2, columns= ['time','open','high','low','close','vwap','volume','count'])
#pprint(df_ohlc.head())
new_df = pd.concat([df_ohlc['time'],df_ohlc['close']],axis=1)
new_df['minute_volatility'] = np.log(new_df['close']) - np.log(new_df['close'].shift(1))
#pprint(new_df)

#hourly volatility
#only calculate hourly vollatility and by minute, need timeframe from traditional remittance 

new_df['time'] = pd.to_datetime(new_df['time'])
hourly_df = new_df[new_df['time'].dt.minute == 0]
hourly_df2 = hourly_df.drop(['minute_volatility'],axis=1)
hourly_df2 = hourly_df2.reset_index()
hourly_df2['hourly volatility'] = np.log(new_df['close']) - np.log(new_df['close'].shift(1))

#pprint(hourly_df2)













