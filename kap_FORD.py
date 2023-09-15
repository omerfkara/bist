import pandas as pd 
import os
import matplotlib.pyplot as plt

def fmt(x):
    x=str(x)
    x=x.replace('.','')
    try:
        x=float(x)
    except:
        print(x)
    return x

def calc_kpi(x):
    x['Cari Oran'] = x['TOPLAM DÖNEN VARLIKLAR'] / x['Ticari Borçlar']
    x['Asit Test Oranı (Likidite Oranı)'] = (x['TOPLAM DÖNEN VARLIKLAR'] - x['Stoklar']) / x['Ticari Borçlar']
    x['Karşılama Oranı'] = x['Ticari Alacaklar'] / x['Ticari Borçlar']
    return x #x['Cari Oran'], x['Asit Test Oranı (Likidite Oranı)'], x['Karşılama Oranı']  

folder = 'KAP/Bildirimler/'
files = os.listdir(folder)
sira = 1
df=pd.DataFrame()
df_kpi=pd.DataFrame()

def extract_kpi(df, df_kpi):
    KPI_LIST = ['Nakit ve Nakit Benzerleri',
                'TOPLAM KISA VADELİ YÜKÜMLÜLÜKLER',
                'TOPLAM DÖNEN VARLIKLAR','Stoklar','Diğer Borçlar',
                'Ticari Borçlar', 'Ticari Alacaklar']
    df = df[KPI_LIST]
    df.to_csv('df.csv', mode='a')
    df.drop_duplicates(inplace=True)
    for f in KPI_LIST:
        df[f]=df[f].apply(fmt)
    
    
    df.to_csv('df2.csv', mode='a')
    df_kpi_temp = df.apply(calc_kpi, axis=1, result_type='expand')
    df_kpi_temp.columns = ['Cari Oran','Asit Test Oranı (Likidite Oranı)','Karşılama Oranı']
    df_kpi_temp.to_csv('df-kpi_temp.csv', mode='a')
    df_kpi = pd.concat([df_kpi,df_kpi_temp])

def find_dataframe(list_element, i, df_kpi):
    temp = pd.DataFrame(list_element)
    current_period = temp.loc[0,3].replace('Cari Dönem ','')
    previous_period = temp.loc[0,4].replace('Önceki Dönem ','')
    cols = ['Col1', 'Kalem', 'Col3', current_period, previous_period]
    temp = temp.drop([0])
    temp.columns = cols
    temp = temp[['Kalem', current_period, previous_period]]
    #print(temp.head())
    temp = temp.set_index('Kalem')
    temp=temp.dropna()
    temp.drop_duplicates(inplace=True)
    df = temp.transpose()
    #df = df.dropna()
    df.drop_duplicates(inplace=True)
    print(i)
    #df.to_csv('csv/FORD'+str(i)+'.csv')
    print('başarılı')
    extract_kpi(df=df, df_kpi=df_kpi)

def extract(raw_df, folder, file, df_kpi):
    path = folder + file
    print(path)
    raw_list = pd.read_html(path)
    print('Dosya index sayısı: ' + str(len(raw_list)))
    for i in range(len(raw_list)):
        #print(i)
        try:
            find_dataframe(list_element=raw_list[i], i=i, df_kpi=df_kpi)
        except:
            pass
            #print('Hatalı')
    return raw_df

extract(df, folder='KAP/Bildirimler/', file='Bildirimler-14.xls', df_kpi=df_kpi)

'''
df_kpi.reset_index(inplace=True)
df_kpi['index'] = pd.to_datetime(df_kpi['index'])
df_kpi.drop_duplicates(inplace=True)
df_kpi.set_index('index',inplace=True)
df_kpi.sort_index(inplace=True)
print(df_kpi)
df_kpi.to_csv('KPI_FORD.csv')
df_kpi.plot()
plt.show()
'''

'''
for file in files:
    try:
        extract(df, folder=folder, file=file)
    except:
        print('Hata')
    
'''