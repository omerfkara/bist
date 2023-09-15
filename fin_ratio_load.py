import pandas as pd
import altair as alt

from matplotlib import pyplot as plt 
import os
import streamlit as st

folder = 'extract/'
files = os.listdir(folder)
df_kpi = pd.DataFrame()
for file in files:
    if file[-8:]=='_KPI.csv':
        COMPANY_NAME = file[:-8]
        temp_df=pd.read_csv(folder + file)
        temp_df['Şirket'] = COMPANY_NAME
        print(temp_df)
        df_kpi = pd.concat([df_kpi,temp_df])
#st.dataframe(df_kpi)


#Tüm kolonlarlı alt, normalize ettim
df_kpi2 = pd.melt(df_kpi, id_vars=['Şirket','TARİH'], var_name='KPI', value_name='Değer')

def drawCompany(COM):
    temp=df_kpi2[df_kpi2['Şirket'] == COM]
    chart = alt.Chart(temp).mark_line().encode(
        x=alt.X('TARİH:N'),
        y=alt.Y('Değer:Q'),
    color=alt.Color("KPI:N")
        ).properties(title=temp['Şirket'].unique())
    st.altair_chart(chart, use_container_width=True)

def drawKPI(KPI):
    temp=df_kpi2[df_kpi2['KPI'] == KPI]
    chart = alt.Chart(temp).mark_line().encode(
        x=alt.X('TARİH:N'),
        y=alt.Y('Değer:Q'),
    color=alt.Color("Şirket:N")
        ).properties(title=temp['KPI'].unique())
    st.altair_chart(chart, use_container_width=True)

kpis = df_kpi2['KPI'].unique()
coms = df_kpi2['Şirket'].unique()

st.set_page_config(
    page_title="k4r4.fin",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    })

tab1, tab2 = st.tabs(['Şirketler', 'Göstergeler'])

with tab1:
    st.header("Şirketler")
    for c in coms:
        drawCompany(c)
with tab2:
    st.header("Göstergeler")
    for k in kpis:
        drawKPI(k)
    