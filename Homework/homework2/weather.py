import pandas as pd
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.font_manager import FontProperties

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 读取数据
data = pd.read_csv('output/clean_大连天气_2022-2024.csv')

# 转换日期列为datetime类型
data['日期'] = pd.to_datetime(data['日期'], format='%Y年%m月%d日')

# 提取年份和月份
data['年份'] = data['日期'].dt.year
data['月份'] = data['日期'].dt.month

# 定义天气分类函数
def classify_weather(weather):
    if '晴' in weather:
        return '晴天'
    elif '多云' in weather:
        return '多云'
    elif '阴' in weather:
        return '阴天'
    elif '雨' in weather or '阵雨' in weather or '小雨' in weather or '中雨' in weather or '大雨' in weather or '暴雨' in weather:
        return '雨天'
    elif '雪' in weather or '阵雪' in weather or '小雪' in weather or '中雪' in weather or '大雪' in weather or '暴雪' in weather:
        return '雪天'
    elif '雾' in weather:
        return '雾天'
    elif '雷' in weather:
        return '雷雨'
    else:
        return '其他'

# 分类白天和夜晚天气
data['白天天气分类'] = data['白天天气'].apply(classify_weather)
data['夜晚天气分类'] = data['夜晚天气'].apply(classify_weather)

# 统计每月各类天气天数
day_weather_counts = data.groupby(['年份', '月份', '白天天气分类']).size().unstack().fillna(0)
night_weather_counts = data.groupby(['年份', '月份', '夜晚天气分类']).size().unstack().fillna(0)

# 合并三年的数据，计算月平均
day_monthly_avg = day_weather_counts.groupby('月份').mean()
night_monthly_avg = night_weather_counts.groupby('月份').mean()

# 绘制白天天气状况分布图
plt.figure(figsize=(14, 8))
day_monthly_avg.plot(kind='bar', stacked=True, colormap='Paired')
plt.title('大连市白天天气状况月分布(2022-2024年平均)')
plt.xlabel('月份')
plt.ylabel('天数')
plt.legend(title='天气类型', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()

# 绘制夜晚天气状况分布图
plt.figure(figsize=(14, 8))
night_monthly_avg.plot(kind='bar', stacked=True, colormap='Paired')
plt.title('大连市夜晚天气状况月分布(2022-2024年平均)')
plt.xlabel('月份')
plt.ylabel('天数')
plt.legend(title='天气类型', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()