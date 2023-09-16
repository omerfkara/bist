import yfinance as yahooFinance
#https://www.geeksforgeeks.org/get-financial-data-from-yahoo-finance-with-python/



import yfinance as yf
import pandas_datareader.data as web
import pandas_ta as ta
import matplotlib.pyplot as plt
from datetime import date
#https://tradewithpython.com/generating-buy-sell-signals-using-python

from fin_yahoo_helper import al_yat, buy_sell, simulation

plt.style.use('fivethirtyeight')
yf.pdr_override()
stock_list=['TUPRS.IS', 'EREGL.IS', 'FROTO.IS', 'SISE.IS', 'ASELS.IS']

for s in stock_list:
    data_stock = yahooFinance.Ticker(s)
    company=data_stock.info['shortName']
    #for k,v in data_stock.info.items():
    #    print(k,v)

    data = data_stock.history(period='5y')

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