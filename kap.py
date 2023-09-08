import pandas as pd

import os

import streamlit as st

folder = 'KAP/'

files = os.listdir(folder)

def read(f, folder=folder):
    df = pd.DataFrame(pd.read_html(folder + f)[0])
    #df = df.set_index(0)
    #print(df.loc[0].values)
    #print(df.head())

    df.columns = df.loc[0].values
    df = df.drop([0])
    df['SIRKET']=f.replace('.xls','')
    #df = df.set_index(['SIRKET', 'FİNANSAL DURUM TABLOSU' ])
    #print(df.head())
    return df
df=pd.DataFrame()

def noktasiz(x):
    try:
        return str(x).replace('.','').replace('nan','0')
    except:
        return x
    
for file in files:
    df_read=read(f=file)
    df = pd.concat([df,df_read])

st.set_page_config(layout='wide')

df=df[['SIRKET','FİNANSAL DURUM TABLOSU','2021/12','2022/12','2023/06']]

par_SIRKET = st.selectbox('Şirket:', df['SIRKET'].unique(),)
if len(par_SIRKET)>0:
    df_selected=df[df['SIRKET']==par_SIRKET]
else:
    df_selected=df
    
st.dataframe(df_selected)


df_ozet= df_selected[(df_selected['FİNANSAL DURUM TABLOSU']=='Toplam Varlıklar') | (df_selected['FİNANSAL DURUM TABLOSU']== 'Duran Varlıklar') | (df_selected['FİNANSAL DURUM TABLOSU']== 'Net Dönem Kârı (Zararı)')]
df_ozet=df_ozet[['SIRKET','FİNANSAL DURUM TABLOSU','2021/12','2022/12','2023/06']]

df_ozet=df_ozet.melt(id_vars=['SIRKET','FİNANSAL DURUM TABLOSU'], 
        var_name="Date", 
        value_name="Value")

df_ozet['Date'] = pd.to_datetime(df_ozet['Date'],format='%Y/%m')

df_ozet=df_ozet.set_index(['Date'])
df_ozet['Value'] = pd.to_numeric(df_ozet['Value'].apply(noktasiz))

df_ozet=df_ozet.pivot(columns=['FİNANSAL DURUM TABLOSU'],values='Value')


st.dataframe(df_ozet)
st.line_chart(df_ozet)