import pandas as pd
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.font_manager import FontProperties

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

# 读取数据
data = pd.read_csv('output/大连天气_2022-2024.csv')

# 转换日期列为datetime类型
data['日期'] = pd.to_datetime(data['日期'], format="%Y年%m月%d日")

# 提取年份和月份
data['年份'] = data['日期'].dt.year
data['月份'] = data['日期'].dt.month

# 计算每月的平均最高温度和平均最低温度
monthly_avg = data.groupby(['月份']).agg({
    '最高温度': 'mean',
    '最低温度': 'mean'
}).reset_index()

# 创建画布
plt.figure(figsize=(12, 6))
ax = plt.gca()  # 获取当前坐标轴
# 绘制折线图
sns.lineplot(data=monthly_avg, x='月份', y='最高温度', label='平均最高温度', marker='o')
sns.lineplot(data=monthly_avg, x='月份', y='最低温度', label='平均最低温度', marker='o')

# 添加数据标签
for i, row in monthly_avg.iterrows():
    # 最高温度标签（显示在点上方）
    ax.text(row['月份'], row['最高温度']+0.5, f"{row['最高温度']:.1f}℃",
            ha='center', va='bottom', fontsize=10)
    # 最低温度标签（显示在点下方）
    ax.text(row['月份'], row['最低温度']-0.5, f"{row['最低温度']:.1f}℃",
            ha='center', va='top', fontsize=10)
# 添加标题和标签
plt.title('大连市近三年(2022-2024)月平均气温变化', fontsize=15)
plt.xlabel('月份', fontsize=12)
plt.ylabel('温度(℃)', fontsize=12)
plt.xticks(range(1, 13), ['1月', '2月', '3月', '4月', '5月', '6月',
                         '7月', '8月', '9月', '10月', '11月', '12月'])

# 设置y轴范围（为标签留出空间）
plt.ylim(monthly_avg['最低温度'].min()-2, monthly_avg['最高温度'].max()+2)
# 添加网格线
plt.grid(True, linestyle='--', alpha=0.6)
# 显示图例
plt.legend(fontsize=12)
# 显示图表
plt.tight_layout()
plt.show()