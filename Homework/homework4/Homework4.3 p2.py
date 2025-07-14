import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from math import log

# 设置中文和负号正常显示
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
plt.set_cmap('rainbow')

# 1. 读取并筛选
df = pd.read_excel("超级大乐透.xlsx")
df = df[['星期几', '前区号码', '后区号码', '销售额']]
df = df[df['星期几'].isin(['星期一','星期三','星期六'])]

# 2. 构建号码计数表
def build_count_table(df, col, max_num):
    records = df[col].str.split().explode().astype(int)
    days    = df[col].str.split().explode().index.map(df['星期几'])
    cnt = pd.crosstab(days, records, rownames=['星期几'], colnames=['号码']).T
    for n in range(1, max_num+1):
        if n not in cnt.index:
            cnt.loc[n] = 0
    return cnt.sort_index()

front_ct = build_count_table(df, '前区号码', max_num=35)
back_ct  = build_count_table(df, '后区号码', max_num=12)

# 3. Shannon 熵
def shannon_entropy(counts):
    freqs = counts / counts.sum()
    freqs = freqs[freqs > 0]
    return -np.sum(freqs * np.log(freqs))

days = ['星期一','星期三','星期六']
# 计算三天的前区熵、后区熵、以及总销售额
front_ent = {d: shannon_entropy(front_ct[d]) for d in days}
back_ent  = {d: shannon_entropy(back_ct[d])  for d in days}
sales_sum = df.groupby('星期几')['销售额'].sum().reindex(days).to_dict()

print("前区熵：", front_ent)
print("后区熵：", back_ent)
print("总销售额：", sales_sum)

# 4. 置信区间法：百分比差异阈值
ci_pct = 1.0  # 差异百分比阈值，10%以内认为无显著差异

def pairwise_pct_diff(metric_dict):
    """
    计算字典中所有两两组合的百分比差异：
      pct_diff = abs(v1-v2) / ((v1+v2)/2) * 100
    返回 { (day1, day2): pct_diff }。
    """
    days = list(metric_dict.keys())
    res = {}
    for i in range(len(days)):
        for j in range(i+1, len(days)):
            d1, d2 = days[i], days[j]
            v1, v2 = metric_dict[d1], metric_dict[d2]
            pct = abs(v1 - v2) / ((v1 + v2) / 2) * 100
            res[(d1, d2)] = pct
    return res

# 计算三种指标的两两差异
front_diff = pairwise_pct_diff(front_ent)
back_diff  = pairwise_pct_diff(back_ent)
sales_diff = pairwise_pct_diff(sales_sum)

def report_diffs(name, diff_dict, threshold):
    print(f"\n—— {name} 两两差异报告 ——")
    for (d1, d2), pct in diff_dict.items():
        flag = "无显著差异" if pct <= threshold else "存在显著差异"
        print(f"{d1} vs {d2}: 差异百分比 = {pct:.2f}%，{flag}")

# 输出对比结果
report_diffs("前区熵", front_diff, ci_pct)
report_diffs("后区熵", back_diff, ci_pct)
report_diffs("总销售额", sales_diff, ci_pct)

# 5. （可选）可视化结果
# 5.1 熵值柱状图
import numpy as np
fig, ax = plt.subplots(1, 2, figsize=(10,4))
ent_df = pd.DataFrame([
    {"Day": d, "FrontEntropy": front_ent[d], "BackEntropy": back_ent[d]}
    for d in days
])
ax[0].bar(ent_df["Day"], ent_df["FrontEntropy"], label="前区熵", alpha=0.7)
ax[0].bar(ent_df["Day"], ent_df["BackEntropy"], label="后区熵", alpha=0.7)
ax[0].set_title("前后区熵对比"); ax[0].legend()

# 5.2 销售额柱状图
fig, ax2 = plt.subplots(figsize=(6,4))
ax2.bar(list(sales_sum.keys()), list(sales_sum.values()))
ax2.set_title("各开奖日总销售额")
ax2.set_xlabel("星期几"); ax2.set_ylabel("销售额")

plt.tight_layout()
plt.show()
