import pandas as pd 
import os

def out(df, fileid, filename):
    filename = 'csv/'+filename+'_'+str(fileid)+'.csv' 
    df.to_csv(filename)

sira = 1
df=pd.DataFrame()
df_kpi=pd.DataFrame()

COMPANY_CODE = 'TOASA'    
folder='KAP/'+COMPANY_CODE+'/' 
files = os.listdir(folder)
for file in files:
    path = folder + file
    raw_list = pd.read_html(path)
    print('Dosya index sayısı: ' + str(len(raw_list)))
    for i in range(len(raw_list)):
        temp = pd.DataFrame(raw_list[i])
        print(i, temp.size)
        out(temp,i,'table')
        if temp.size>=14:
            if temp.loc[ 1, 1]=='Finansal Durum Tablosu (Bilanço)':
                print(i, temp.loc[ 1, 1])
                temp = pd.DataFrame(raw_list[i])
                temp.to_csv('csv/fin_ratio.csv')
                current_period = temp.loc[0,3].replace('Cari Dönem ','')
                previous_period = temp.loc[0,4].replace('Önceki Dönem ','')
                try: 
                    pre_previous_period = temp.loc[0,5].replace('Bir Önceki Dönem ','')
                    cols = ['Col1', 'LEVEL3', 'Col3', current_period, previous_period, pre_previous_period]
                except:
                    print('Bir önceki dönem yok')
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
                #temp.to_csv('csv/fin_ratio_2.csv')
                temp=temp.dropna(subset=['LEVEL3'])
                #temp.to_csv('csv/fin_ratio_3.csv')
                temp = temp.melt(id_vars=['LEVEL1','LEVEL2','LEVEL3'], var_name='TARİH', value_name='DEĞER')
                temp.to_csv('extract/'+COMPANY_CODE+'.csv', mode='a')
