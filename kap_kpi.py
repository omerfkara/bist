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


'''

    #KPI CALCULATION
    #1)Cari Oran: Dönen Varlıklar / Kısa Vadeli Yükümlülükler
    #2)Asit Test Oranı (Likidite Oranı): (Dönen Varlıklar - Stoklar) / Kısa Vadeli Yükümlülükler
    #3)Hazır Değerler Oranı (Nakit Oranı): Hazır Değerler/Kısa Vadeli Yabancı Kaynaklar 
    #4)Karşılama Oranı: Ticari Alacaklar/Ticari Borçlar
'''
def calc_kpi(x):
    x['Cari Oran'] = x['TOPLAM DÖNEN VARLIKLAR'] / x['Ticari Borçlar']
    x['Asit Test Oranı (Likidite Oranı)'] = (x['TOPLAM DÖNEN VARLIKLAR'] - x['Stoklar']) / x['Ticari Borçlar']
    x['Karşılama Oranı'] = x['Ticari Alacaklar'] / x['Ticari Borçlar']
    return x['Cari Oran'], x['Asit Test Oranı (Likidite Oranı)'], x['Karşılama Oranı']  
folder = 'KAP/2023-Tum Donemler/'
files = os.listdir(folder)

sira = 1

df=pd.DataFrame()
df_kpi=pd.DataFrame()
'''
Dosya_0002
Dosya_0301
Dosya_0373
Dosya_0458
Dosya_0663
'''
for file in files:
    lst = pd.read_html(folder + file)
    temp = pd.DataFrame(lst[1])
    current_period = temp.loc[0,3].replace('Cari Dönem ','')
    previous_period = temp.loc[0,4].replace('Önceki Dönem ','')
    cols = ['Col1', 'Kalem', 'Col3', current_period, previous_period]
    temp = temp.drop([0])
    temp.columns = cols
    temp = temp[['Kalem', current_period, previous_period]]
    #print(temp.head())
    temp = temp.set_index('Kalem')
    temp=temp.dropna()
    temp.to_csv('temp'+file+'.csv')
    df = temp.transpose()
    df = df.dropna()

    #print(df.columns.values)
    

    KPI_LIST = ['Nakit ve Nakit Benzerleri',
                'TOPLAM KISA VADELİ YÜKÜMLÜLÜKLER',
                'TOPLAM DÖNEN VARLIKLAR','Stoklar','Diğer Borçlar',
                'Ticari Borçlar', 'Ticari Alacaklar']
    df = df[KPI_LIST]
    for f in KPI_LIST:
        df[f]=df[f].apply(fmt)

    df_kpi_temp = df.apply(calc_kpi, axis=1, result_type='expand')
    df_kpi_temp.columns = ['Cari Oran','Asit Test Oranı (Likidite Oranı)','Karşılama Oranı']
    df.to_csv('Workbook_'+file+'.csv')
    print(df_kpi_temp)
    df_kpi = pd.concat([df_kpi,df_kpi_temp])
df_kpi.reset_index(inplace=True)
df_kpi['index'] = pd.to_datetime(df_kpi['index'])
df_kpi.drop_duplicates(inplace=True)
df_kpi.set_index('index',inplace=True)
df_kpi.sort_index(inplace=True)
print(df_kpi)
df_kpi.to_csv('KPI.csv')
df_kpi.plot()
plt.show()
