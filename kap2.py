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
    df['Cari Oran'] = x['TOPLAM DÖNEN VARLIKLAR'] / x['Ticari Borçlar']
    df['Asit Test Oranı (Likidite Oranı)'] = (x['TOPLAM DÖNEN VARLIKLAR'] - x['Stoklar']) / x['Ticari Borçlar']
    df['Karşılama Oranı'] = x['Ticari Alacaklar'] / x['Ticari Borçlar']
    
folder = 'KAP/2023-Tum Donemler/'
files = os.listdir(folder)

sira = 1

df=pd.DataFrame()
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
    temp.to_csv('temp.csv')
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

    df.apply(calc_kpi, axis=1)
    df.to_csv('Workbook.csv')

    df_kpi = df[['Cari Oran','Asit Test Oranı (Likidite Oranı)','Karşılama Oranı']]
    df_kpi.plot()
    plt.show()
    #print(df.head())
    
    break

    df=temp.melt(id_vars=['Kalem'], 
        var_name="Date", 
        value_name="Value")
    df = df.dropna()
    df = df.set_index('Kalem')
    print(df.index.values)
    

    #KPI CALCULATION
    #1)Cari Oran: Dönen Varlıklar / Kısa Vadeli Yükümlülükler
    #2)Asit Test Oranı (Likidite Oranı): (Dönen Varlıklar - Stoklar) / Kısa Vadeli Yükümlülükler
    #3)Hazır Değerler Oranı (Nakit Oranı): Hazır Değerler/Kısa Vadeli Yabancı Kaynaklar 
    '''
    Kısa vadeli yabancı kaynaklar nelerdir sorusunu 9 alt gruba ayrılmak üzere 
    Mali borçlar, 
    -Ticari borçlar, 
    -Diğer borçlar, 
    Alınan avanslar, 
    Yıllara yaygın inşaat ve onarım hakedişleri, 
    Ödenecek vergi ve diğer yükümlülükler, 
    Borç ve gider karşılıkları, 
    Gelecek aylara ait gelirler ve gider tahakkukları, 
    diğer kısa vadeli yabancı kaynaklar olarak cevaplayabiliriz.
    '''
    

    #for k in KPI_LIST:
    #    print(df[df.index==k].Value)
    

    df_kpi = df.transpose()
    print(df_kpi.head())
'''
    for l in lst:
        export_filename = 'Dosya_' + f"{sira:04d}"
        temp = pd.DataFrame(l)
        temp['filename']=export_filename
        df = pd.concat([df, temp])
        sira = sira + 1
'''
    