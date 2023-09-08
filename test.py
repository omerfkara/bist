import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sbs
import xgboost as xgb
#import xgboost as xgb
color_pal = sbs.color_palette()

def extract(stock):
    df = pd.read_csv('historical/' + stock + ' Historical Data.csv')
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.set_index('Date')
    df['Change'] = df['Change %'].apply(to_number)
    df['Price'] = df['Price'].apply(to_number)
    df = df[['Price']]
    df = df[df.index>='2021-01-01']
    df = df[df.index<'2023-09-01']
    return df

def to_number(x):
    r = str(x).replace('%','').replace(',','')
    return float(r)

fig, ax = plt.subplots()

df_TUPRS = extract('TUPRS')
df_XAU_USD = extract('XAU_USD')
df_USD_TRY = extract('USD_TRY')
df_BRENT = extract('Brent Oil Futures')
df_BIST = extract('BIST 30')
df_FROTO = extract('FROTO')
'''
ax.legend(['TUPRS', 'XAU_USD', 'USD_TRY', 'BRENT', 'BIST 30']);
df_TUPRS.plot(ax=ax, color=color_pal[0])
df_XAU_USD.plot(ax=ax, color=color_pal[1])
df_USD_TRY.plot(ax=ax, color=color_pal[2])
df_BRENT.plot(ax=ax, color=color_pal[3])
df_BIST.plot(ax=ax, color=color_pal[4])
plt.show()
plt.close()
'''
df=pd.merge(left=df_TUPRS, right=df_BRENT, how='left', suffixes=['', 'BRENT'], left_index=True, right_index=True)
df=pd.merge(left=df, right=df_XAU_USD, how='left', suffixes=['', 'XAU_USD'], left_index=True, right_index=True)
df=pd.merge(left=df, right=df_USD_TRY, how='left', suffixes=['', 'USD_TRY'], left_index=True, right_index=True)
df=pd.merge(left=df, right=df_USD_TRY, how='left', suffixes=['', 'BIST'], left_index=True, right_index=True)
df=pd.merge(left=df, right=df_FROTO, how='left', suffixes=['', 'FROTO'], left_index=True, right_index=True)


FEATURES = ['PriceBRENT', 'PriceXAU_USD', 'PriceUSD_TRY','PriceBIST', 'PriceFROTO']
TARGET = 'Price'

train_test_divide = '2023-08-01'
df_train = df[df.index<train_test_divide]
df_test  = df[df.index>=train_test_divide]


X_train = df_train[FEATURES]
y_train = df_train[TARGET]

X_test = df_test[FEATURES]
y_test = df_test[TARGET]

reg = xgb.XGBRegressor(n_estimators = 1000, early_stopping_rounds = 50)
reg.fit(X_train, y_train, 
        eval_set=[(X_train, y_train),(X_test, y_test)],  
        verbose=True)

print(FEATURES)
feature_importances = reg.feature_importances_
print(feature_importances)

df_test['predictions'] = reg.predict(X_test)

#print(df_test)
df_test[[TARGET]].plot(ax=ax, color=color_pal[0])

df_test[['predictions']].plot(ax=ax, color=color_pal[1])
plt.show()