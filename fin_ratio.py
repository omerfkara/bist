import pandas as pd 
import os

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


def out(df, fileid, filename):
    filename = 'csv/'+filename+'_'+str(fileid)+'.csv' 
    df.to_csv(filename)

folder = 'KAP/Bildirimler/'
files = os.listdir(folder)
sira = 1
df=pd.DataFrame()
df_kpi=pd.DataFrame()
KPI_LIST = ['Nakit ve Nakit Benzerleri',
                'TOPLAM KISA VADELİ YÜKÜMLÜLÜKLER',
                'TOPLAM DÖNEN VARLIKLAR','Stoklar','Diğer Borçlar',
                'Ticari Borçlar', 'Ticari Alacaklar']
    
folder='KAP/Bildirimler/' 
file='Bildirimler-14.xls'
path = folder + file
raw_list = pd.read_html(path)
print('Dosya index sayısı: ' + str(len(raw_list)))
for i in range(len(raw_list)):
    temp = pd.DataFrame(raw_list[i])
    out(temp,i,'table')
    try:
        if temp.loc[ 1, 1]=='Finansal Durum Tablosu (Bilanço)':
            print(i, temp.loc[ 1, 1])
    except:
        continue
exit()
temp = pd.DataFrame(raw_list[7])
temp.to_csv('csv/fin_ratio.csv')
current_period = temp.loc[0,3].replace('Cari Dönem ','')
previous_period = temp.loc[0,4].replace('Önceki Dönem ','')
cols = ['Col1', 'LEVEL3', 'Col3', current_period, previous_period]
temp.columns = cols
temp = temp[['LEVEL3', current_period, previous_period]]
temp['LEVEL1'] = ''
temp['LEVEL2'] = ''
temp.loc[  3:257, 'LEVEL1'] = 'VARLIKLAR'
temp.loc[  5:109, 'LEVEL2'] = 'DÖNEN VARLIKLAR'
temp.loc[111:255, 'LEVEL2'] = 'DURAN VARLIKLAR'
temp.loc[259:593, 'LEVEL1'] = 'KAYNAKLAR'
temp.loc[261:381, 'LEVEL2'] = 'KISA VADELİ YÜKÜMLÜLÜKLER'
temp.loc[383:481, 'LEVEL2'] = 'UZUN VADELİ YÜKÜMLÜLÜKLER'
temp.loc[485:591, 'LEVEL2'] = 'ÖZKAYNAKLAR'

temp.to_csv('csv/fin_ratio_2.csv')

temp=temp.dropna(subset=['LEVEL3'])
temp.to_csv('csv/fin_ratio_3.csv')

temp = temp.melt(id_vars=['LEVEL1','LEVEL2','LEVEL3'], var_name='TARİH', value_name='DEĞER')
temp.to_csv('csv/FROTO.csv')

exit()    

for i in range(len(raw_list)):
    temp = pd.DataFrame(raw_list[i])
    print(temp[temp.index==22])
    continue
    temp.to_csv('csv/temp_'+str(i)+'.csv')
    try:
        current_period = temp.loc[0,3].replace('Cari Dönem ','')
    except:
        print('Bizim istediğimiz dosya değil: ' + str(i))
        continue
    previous_period = temp.loc[0,4].replace('Önceki Dönem ','')
    cols = ['Col1', 'Kalem', 'Col3', current_period, previous_period]
    temp = temp.drop([0])
    try:
        temp.columns = cols
    except:
        print('Kolonlar beklendiği gibi değil: ' + str(i) )
        error_out(temp,i)
        continue
    temp.to_csv('csv/temp2_'+str(i)+'.csv')

    temp = temp[['Kalem', current_period, previous_period]]

    temp = temp.set_index('Kalem')
    temp.to_csv('csv/temp3_'+str(i)+'.csv')
    temp = temp.dropna()
    temp = temp[temp.index.isin(KPI_LIST)]
    #temp = temp.drop_duplicates()
    temp.to_csv('csv/temp4_'+str(i)+'.csv')

    df = temp.transpose()
    #df.drop_duplicates(inplace=True)
    #print(i)
    #df.to_csv('csv/FORD'+str(i)+'.csv')
    df.to_csv('csv/df_'+str(i)+'.csv')
    #try:
    #    df = df[KPI_LIST]
    #except:
    #    print('KPI_LIST dosyada yok', str(i))
    #    error_out(df, i)
    #    continue
    #df.to_csv('df.csv', mode='a')
    df.to_csv('csv/before_duplicate_'+str(i)+'.csv')
    df.drop_duplicates(inplace=True)
    df.to_csv('csv/after_duplicate_'+str(i)+'.csv')
    
    for f in KPI_LIST:
        df[f]=df[f].apply(fmt)
    
    df_kpi_temp = df.apply(calc_kpi, axis=1, result_type='expand')
    df_kpi_temp.columns = ['Cari Oran','Asit Test Oranı (Likidite Oranı)','Karşılama Oranı']
    df_kpi_temp.to_csv('df-kpi_temp.csv', mode='a')
    df_kpi = pd.concat([df_kpi,df_kpi_temp])
