import yfinance as yahooFinance
#https://www.geeksforgeeks.org/get-financial-data-from-yahoo-finance-with-python/


import pandas as pd
#import yfinance as yf
import pandas_datareader.data as web
import pandas_ta as ta
import matplotlib.pyplot as plt
from datetime import date
#https://tradewithpython.com/generating-buy-sell-signals-using-python

#https://www.qmr.ai/yfinance-library-the-definitive-guide/

from fin_yahoo_helper import al_yat, buy_sell, simulation, MACD_Strategy, MACD_color, out
plt.style.use('fivethirtyeight')
yahooFinance.pdr_override()
stock_list=['TUPRS.IS', 'EREGL.IS', 'FROTO.IS', 'SISE.IS', 'ASELS.IS']

for s in stock_list:
    data_stock = yahooFinance.Ticker(s)
    company=data_stock.info['shortName']
    #for k,v in data_stock.info.items():
    #    pr
    # 
    # int(k,v)

    data = data_stock.history(period='3mo', interval='1h')

    data['SMA 30'] = ta.sma(data['Close'],30)
    data['SMA 100'] = ta.sma(data['Close'],100)
    #SMA BUY SELL
    #Function for buy and sell signal


    data['Buy_Signal_price'], data['Sell_Signal_price'] = buy_sell(data)

    data['balance_try'], data['balance_stock'], data['calc_balance_try'] = simulation(data)

    data['balance_try_al_yat'], data['balance_stock_al_yat'], data['calc_balance_try_al_yat'] = al_yat(data)

    data['company']=company

    print(data[['company','calc_balance_try', 'calc_balance_try_al_yat']].iloc[-1])

    startdate = data.index.min()
    end_date = data.index.max()

    fig, ax = plt.subplots(figsize=(14,8))
    ax.plot(data['Close'] , label = company ,linewidth=0.5, color='blue', alpha = 0.9)
    ax.plot(data['SMA 30'], label = 'SMA30', alpha = 0.85)
    ax.plot(data['SMA 100'], label = 'SMA100' , alpha = 0.85)
    ax.scatter(data.index , data['Buy_Signal_price'] , label = 'Buy' , marker = '^', color = 'green',alpha =1 )
    ax.scatter(data.index , data['Sell_Signal_price'] , label = 'Sell' , marker = 'v', color = 'red',alpha =1 )
    ax.set_title(company + " Price History with buy and sell signals",fontsize=10, backgroundcolor='blue', color='white')
    ax.set_xlabel(f'{startdate} - {end_date}' ,fontsize=18)
    ax.set_ylabel('Close Price INR (₨)' , fontsize=18)
    legend = ax.legend()
    ax.grid()
    plt.tight_layout()
    plt.savefig(company + '.png')

    macd = ta.macd(data['Close'])

    data = pd.concat([data, macd], axis=1).reindex(data.index)

    data['MACD_Buy_Signal_price'], data['MACD_Sell_Signal_price'] =  MACD_Strategy(data, 0.025)
    
    data['positive'] = MACD_color(data)


    plt.rcParams.update({'font.size': 10})
    fig, ax1 = plt.subplots(figsize=(14,8))
    fig.suptitle(company, fontsize=10, backgroundcolor='blue', color='white')
    ax1 = plt.subplot2grid((14, 8), (0, 0), rowspan=8, colspan=14)
    ax2 = plt.subplot2grid((14, 12), (10, 0), rowspan=6, colspan=14)
    ax1.set_ylabel('Price in ₨')
    ax1.plot('Close',data=data, label='Close Price', linewidth=0.5, color='blue')
    ax1.scatter(data.index, data['MACD_Buy_Signal_price'], color='green', marker='^', alpha=1)
    ax1.scatter(data.index, data['MACD_Sell_Signal_price'], color='red', marker='v', alpha=1)
    ax1.legend()
    ax1.grid()
    ax1.set_xlabel('Date', fontsize=8)
    ax2.set_ylabel('MACD', fontsize=8)
    ax2.plot('MACD_12_26_9', data=data, label='MACD', linewidth=0.5, color='blue')
    ax2.plot('MACDs_12_26_9', data=data, label='signal', linewidth=0.5, color='red')
    ax2.bar(data.index,'MACDh_12_26_9', data=data, label='Volume', color=data.positive.map({True: 'g', False: 'r'}),width=1,alpha=0.8)
    ax2.axhline(0, color='black', linewidth=0.5, alpha=0.5)
    ax2.grid()

    plt.savefig(company + '_2.png')
    out(data,company,'fin_yahoo')
    
    

