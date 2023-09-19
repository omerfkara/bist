import numpy as np
import pandas as pd

sim_start_balance_try = 100000

def buy_sell(data):
    signalBuy = []
    signalSell = []
    position = False 

    for i in range(len(data)):
        if data['SMA 30'][i] > data['SMA 100'][i]:
            if position == False :
                signalBuy.append(data['Close'][i])
                signalSell.append(np.nan)
                position = True
            else:
                signalBuy.append(np.nan)
                signalSell.append(np.nan)
        elif data['SMA 30'][i] < data['SMA 100'][i]:
            if position == True:
                signalBuy.append(np.nan)
                signalSell.append(data['Close'][i])
                position = False
            else:
                signalBuy.append(np.nan)
                signalSell.append(np.nan)
        else:
            signalBuy.append(np.nan)
            signalSell.append(np.nan)
    return pd.Series([signalBuy, signalSell])


def simulation(data):
    balance_stock = []
    balance_try = [] 
    calc_balance_try = []
    buy_price=np.nan
    sell_price=np.nan
    for i in range(len(data)):
        if i == 0: 
            balance_try.append(sim_start_balance_try)
            balance_stock.append(0)
            calc_balance_try.append(sim_start_balance_try)
        else:

            if buy_price>0:
                balance_try.append(0)
                balance_stock.append(balance_try[i-1]/buy_price)
                calc_balance_try.append(balance_stock[i] * data['Close'][i] + balance_try[i])
            elif sell_price>0:
                balance_try.append(sell_price * balance_stock[i-1])
                balance_stock.append(0)
                calc_balance_try.append(balance_stock[i] * data['Close'][i] + balance_try[i])
            else:
                balance_try.append(balance_try[i-1])
                balance_stock.append(balance_stock[i-1])
                calc_balance_try.append(balance_try[i-1] + balance_stock[i-1] * data['Close'][i-1])
                
        buy_price = data['Buy_Signal_price'][i]
        sell_price = data['Sell_Signal_price'][i]

    return pd.Series([balance_try, balance_stock, calc_balance_try])


def al_yat(data):
    balance_stock = []
    balance_try = [] 
    calc_balance_try = []
    buy_price=np.nan
    sell_price=np.nan
    for i in range(len(data)):
        if i == 0: 
            balance_try.append(sim_start_balance_try)
            balance_stock.append(0)
            calc_balance_try.append(sim_start_balance_try)
        else:

            if buy_price>0 and balance_stock[i-1]==0:
                balance_try.append(0)
                balance_stock.append(balance_try[i-1]/buy_price)
                calc_balance_try.append(balance_stock[i] * data['Close'][i] + balance_try[i])
            else:
                balance_try.append(balance_try[i-1])
                balance_stock.append(balance_stock[i-1])
                calc_balance_try.append(balance_try[i-1] + balance_stock[i-1] * data['Close'][i-1])
                
        buy_price = data['Buy_Signal_price'][i]
        sell_price = data['Sell_Signal_price'][i]

    return pd.Series([balance_try, balance_stock, calc_balance_try])

def MACD_Strategy(df, risk):
    MACD_Buy=[]
    MACD_Sell=[]
    position=False

    for i in range(0, len(df)):
        if df['MACD_12_26_9'][i] > df['MACDs_12_26_9'][i] :
            MACD_Sell.append(np.nan)
            if position ==False:
                MACD_Buy.append(df['Close'][i])
                position=True
            else:
                MACD_Buy.append(np.nan)
        elif df['MACD_12_26_9'][i] < df['MACDs_12_26_9'][i] :
            MACD_Buy.append(np.nan)
            if position == True:
                MACD_Sell.append(df['Close'][i])
                position=False
            else:
                MACD_Sell.append(np.nan)
        elif position == True and df['Close'][i] < MACD_Buy[-1] * (1 - risk):
            MACD_Sell.append(df["Close"][i])
            MACD_Buy.append(np.nan)
            position = False
        elif position == True and df['Close'][i] < df['Close'][i - 1] * (1 - risk):
            MACD_Sell.append(df["Close"][i])
            MACD_Buy.append(np.nan)
            position = False
        else:
            MACD_Buy.append(np.nan)
            MACD_Sell.append(np.nan)
    
    return pd.Series([MACD_Buy, MACD_Sell])


def MACD_color(data):
    MACD_color = []
    for i in range(0, len(data)):
        if data['MACDh_12_26_9'][i] > data['MACDh_12_26_9'][i - 1]:
            MACD_color.append(True)
        else:
            MACD_color.append(False)
    return MACD_color

def out(df, fileid, filename):
    filename = 'csv/'+filename+'_'+str(fileid)+'.csv' 
    df.to_csv(filename)