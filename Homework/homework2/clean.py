import pandas as pd
# 整理爬虫后的表格
df = pd.read_csv('output/大连天气_2022-2024.csv')

df.dropna(inplace=True)

df.to_csv('output/clean_大连天气_2022-2024.csv', index=False)