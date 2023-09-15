import pandas as pd
from collections import defaultdict
import json
from matplotlib import pyplot as plt 
COMPANY_CODE = 'TOASA'    

KPI_LIST_2 = ['Nakit ve Nakit Benzerleri',
                'TOPLAM KISA VADELİ YÜKÜMLÜLÜKLER',
                'TOPLAM DÖNEN VARLIKLAR',
                'Stoklar',
                'Diğer Borçlar',
                'Ticari Borçlar', 
                'Ticari Alacaklar']

load = pd.read_csv('extract/'+COMPANY_CODE+'.csv')

print(load)
kpi={
    'Ticari Alacaklar':{'LEVEL1':'VARLIKLAR', 'LEVEL2':'DÖNEN VARLIKLAR', 'LEVEL3':'Ticari Alacaklar'},
    'Ticari Borçlar':{'LEVEL1':'KAYNAKLAR', 'LEVEL2':'KISA VADELİ YÜKÜMLÜLÜKLER', 'LEVEL3':'Ticari Borçlar'},
    'Dönen Varlıklar':{'LEVEL1':'VARLIKLAR', 'LEVEL2': 'DÖNEN VARLIKLAR', 'LEVEL3':	'TOPLAM DÖNEN VARLIKLAR'},
    'Kısa Vadeli Yükümlülükler':{'LEVEL1':'KAYNAKLAR', 'LEVEL2': 'KISA VADELİ YÜKÜMLÜLÜKLER', 'LEVEL3': 'TOPLAM KISA VADELİ YÜKÜMLÜLÜKLER'},
    'Stoklar': {'LEVEL1': 'VARLIKLAR', 'LEVEL2': 'DÖNEN VARLIKLAR', 'LEVEL3': 'Stoklar'}
    }
load['DEĞER'] = pd.to_numeric(load['DEĞER'].str.replace('.',''),errors='coerce')
load['TARİH'] = pd.to_datetime(load['TARİH'], dayfirst=True, errors='coerce')
load = load.set_index('TARİH')

load = load[['LEVEL1','LEVEL2','LEVEL3','DEĞER']]
load_2 = pd.DataFrame()            
for k in kpi:
    print(k)
    temp_df=load.copy()
    for kk in kpi[k]:
        print(kk,kpi[k][kk])
        temp_df=temp_df[temp_df[kk]==kpi[k][kk]]
    temp_df[k]=temp_df['DEĞER']
    temp_df = temp_df[[k]]
    load_2 = load_2.join(temp_df, how='outer')
    print(temp_df)
print('-------LOAD 2----------')
load_2 = load_2.drop_duplicates().sort_index()
print(load_2)

load_2.to_csv('extract/'+COMPANY_CODE+'_transform.csv')
load_2.plot()
plt.savefig('extract/'+COMPANY_CODE+'_transform.png')

def calc_kpi(row):
    row['Cari Oran']=row['Dönen Varlıklar']/row['Kısa Vadeli Yükümlülükler']
    row['Likitide Oranı']=(row['Dönen Varlıklar']-row['Stoklar'])/row['Kısa Vadeli Yükümlülükler']
    row['Karşılama Oranı']=row['Ticari Alacaklar']/row['Ticari Borçlar']
    return row[['Cari Oran', 'Likitide Oranı', 'Karşılama Oranı']]

load_kpi=load_2.apply(calc_kpi, axis=1)
print('-------LOAD KPI----------')
print(load_kpi)

load_kpi.to_csv('extract/'+COMPANY_CODE+'_KPI.csv')
load_kpi.plot()
plt.savefig('extract/'+COMPANY_CODE+'_KPI.png')


'''from collections import defaultdict
dic={}
for l1 in ['VARLIKLAR']:
    dic[l1]=defaultdict(dict)
    for l2 in ['DÖNEN VARLIKLAR']:
        dic[l1][l2]=defaultdict(dict)
        for l3 in ['Ticari Alacaklar']:
            dic[l1][l2][l3]=load[(load['LEVEL1']==l1) & (load['LEVEL2']==l2) & (load['LEVEL3']==l3)].set_index('TARİH').to_dict() #store the DataFrames to a dict of dict

print(json.dumps(dic))'''