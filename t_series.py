import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

color_pal = sns.color_palette()
df = pd.read_excel('tuprs.xlsx')

df = df[['Tarih', 'Kapanış(TL)']]
df.columns = ['ds', 'y']
df['ds'] = pd.to_datetime(df['ds'],format='%d-%m-%Y')
df = df.set_index('ds')

train_test = '2023-05-01'

train = df[df.index<train_test]
test = df[df.index>=train_test]
fig, ax = plt.subplots()

train.plot(ax=ax, color=color_pal[0], label='train')
test.plot(ax=ax, color=color_pal[1], label = 'test')
plt.show()
'''print(df.head())

model = Prophet()

model.fit(df)'''