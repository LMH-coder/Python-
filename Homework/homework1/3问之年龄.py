import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# --- 1. 全局美化与中文显示设置 ---
# 确保图表能正常显示中文
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# --- 2. 数据加载与准备 ---
try:
    # 从新的Excel文件加载数据
    file_path = '胡润百富榜完整数据2.0.xlsx'
    df = pd.read_excel(file_path)
    print(f"成功加载文件: {file_path}")
except FileNotFoundError:
    print(f"错误：未找到 '{file_path}'。请确保文件与Python脚本在同一目录下。")
    exit()

# 定义年龄列名
age_column = 'hs_Rank_Rich_Age'

# --- 3. 数据清洗、分类与统计 ---
# a. 筛选出年龄列不为空的记录
df_age = df.dropna(subset=[age_column]).copy()

# b. 统计“未知”年龄的数量
unknown_count = (df_age[age_column] == '未知').sum()
print(f"年龄未知的富豪数量为: {unknown_count}")

# c. 将已知年龄转换为数值类型，无法转换的（即'未知'）会变为NaN
numeric_ages = pd.to_numeric(df_age[age_column], errors='coerce')

# d. 筛选出所有年龄为有效数字的行
df_known_age = df_age[numeric_ages.notna()].copy()
df_known_age[age_column] = df_known_age[age_column].astype(int)
print(f"年龄已知的富豪数量为: {len(df_known_age)}")

# e. 对已知年龄进行分段
bins = [0, 40, 50, 60, 70, 120]
labels = ['40岁以下', '40-49岁', '50-59岁', '60-69岁', '70岁及以上']
df_known_age['年龄分段'] = pd.cut(df_known_age[age_column], bins=bins, labels=labels, right=False)

# f. 统计每个年龄分段的富豪数量
age_distribution = df_known_age['年龄分段'].value_counts().sort_index()

# g. 将“未知”数量合并到最终的统计结果中
if unknown_count > 0:
    unknown_series = pd.Series({'年龄未知': unknown_count})
    final_distribution = pd.concat([age_distribution, unknown_series])
else:
    final_distribution = age_distribution

# --- 4. 可视化：绘制包含“未知”项的柱状图 ---
print("正在生成年龄分布柱状图...")

plt.figure(figsize=(14, 8))
# 使用一个更鲜明的调色板
ax = sns.barplot(x=final_distribution.index, y=final_distribution.values, palette='plasma')

# 添加数据标签
for p in ax.patches:
    ax.annotate(f'{int(p.get_height())}',
                (p.get_x() + p.get_width() / 2., p.get_height()),
                ha='center', va='center',
                xytext=(0, 9),
                textcoords='offset points',
                fontsize=12,
                fontweight='bold')

# 设置图表标题和坐标轴标签
plt.title('富豪年龄分布情况 (含未知年龄)', fontsize=22, fontweight='bold', pad=20)
plt.xlabel('年龄分段', fontsize=15)
plt.ylabel('上榜富豪数量', fontsize=15)
plt.xticks(fontsize=13, rotation=15) # 稍微旋转x轴标签以防重叠
plt.yticks(fontsize=13)

# 优化图表样式
ax.yaxis.grid(True, linestyle='--', alpha=0.7)
sns.despine()

# 调整y轴范围
plt.ylim(0, final_distribution.max() * 1.2)

# --- 5. 保存并展示图表 ---
output_path = '富豪年龄分布(含未知)_柱状图.png'
plt.savefig(output_path, dpi=300, bbox_inches='tight')
plt.show()

print(f"\n🎉 可视化完成！图表已保存为 '{output_path}'")
