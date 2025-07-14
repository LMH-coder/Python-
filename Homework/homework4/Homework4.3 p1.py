import pandas as pd
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
from math import log

# 设置中文和负号正常显示
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
# 使用 rainbow colormap 作为默认色图
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
    # 补齐缺失号码
    for n in range(1, max_num+1):
        if n not in cnt.index:
            cnt.loc[n] = 0
    return cnt.sort_index()

front_ct = build_count_table(df, '前区号码', max_num=35)
back_ct  = build_count_table(df, '后区号码', max_num=12)

# 3. 构建分布量化指标：Shannon 熵（Entropy）
def shannon_entropy(counts):
    freqs = counts / counts.sum()
    freqs = freqs[freqs > 0]
    return -np.sum(freqs * np.log(freqs))

days = ['星期一','星期三','星期六']
entropy_list = []

for region_name, ct in [('前区', front_ct), ('后区', back_ct)]:
    for day in days:
        ent = shannon_entropy(ct[day])
        entropy_list.append({
            'Region': region_name,
            'Day': day,
            'Entropy': ent
        })

ent_df = pd.DataFrame(entropy_list)
print(ent_df)

# 4. 熵值置换检验 —— 绕过正态性，直接检验熵值差异显著性
def permutation_test_entropy(df, build_ct_fn, col_name, max_num, days, n_perm=1000, seed=42):
    rng = np.random.RandomState(seed)
    ct_orig = build_ct_fn(df, col_name, max_num)
    obs_ent = { d: shannon_entropy(ct_orig[d]) for d in days }
    obs_stat = np.var(list(obs_ent.values()))

    perm_stats = []
    for _ in range(n_perm):
        df_perm = df.copy()
        df_perm['星期几'] = rng.permutation(df_perm['星期几'].values)
        ct_perm = build_ct_fn(df_perm, col_name, max_num)
        entropies = [shannon_entropy(ct_perm[d]) for d in days]
        perm_stats.append(np.var(entropies))

    p_value = np.mean([s >= obs_stat for s in perm_stats])
    return obs_ent, obs_stat, p_value

for region, col, max_n in [
    ('前区', '前区号码', 35),
    ('后区', '后区号码', 12)
]:
    ent_dict, var_stat, p_val = permutation_test_entropy(
        df, build_count_table, col, max_n,
        days=days,
        n_perm=2000,
        seed=2025
    )
    print(f"{region} 原始熵值：{ent_dict}")
    print(f"{region} 熵值方差 = {var_stat:.4f}，置换检验 p-value = {p_val:.4f}")
    print('-'*50)

# 5. 销售额正态性与差异检验
sales_groups = [df[df['星期几']==d]['销售额'] for d in days]
for name, grp in zip(days, sales_groups):
    w, p = stats.shapiro(grp)
    print(f"{name} 销售额正态性检验: W={w:.3f}, p={p:.4f}")
if all(stats.shapiro(grp)[1] > 0.05 for grp in sales_groups):
    F, p_val = stats.f_oneway(*sales_groups)
    print(f"销售额 ANOVA 检验: F={F:.2f}, p={p_val:.4f}")
else:
    H, p_val = stats.kruskal(*sales_groups)
    print(f"销售额 Kruskal-Wallis 检验: H={H:.2f}, p={p_val:.4f}")

# 6. 可视化：熵值与号码分布
fig, ax = plt.subplots(1, 2, figsize=(10,4))
for i, region in enumerate(['前区','后区']):
    sub = ent_df[ent_df['Region']==region]
    ax[i].bar(sub['Day'], sub['Entropy'], color=plt.cm.rainbow(np.linspace(0,1,3)))
    ax[i].set_title(f"{region} 分布熵对比")
    ax[i].set_xlabel('开奖日')
    ax[i].set_ylabel('Entropy')
plt.tight_layout()
plt.show()

# 7. 可视化：按开奖日分别展示前区和后区号码分布
fig, axes = plt.subplots(len(days), 2, figsize=(14, 12), sharey=False)
for i, day in enumerate(days):
    front_ct[day].plot(kind='bar', ax=axes[i,0], colormap='autumn', width=0.8)
    axes[i,0].set_title(f"{day} 前区号码分布")
    axes[i,0].set_xlabel('号码'); axes[i,0].set_ylabel('出现次数')

    back_ct[day].plot(kind='bar', ax=axes[i,1], colormap='rainbow', width=0.8)
    axes[i,1].set_title(f"{day} 后区号码分布")
    axes[i,1].set_xlabel('号码'); axes[i,1].set_ylabel('出现次数')

plt.tight_layout()
plt.show()

# 8. 可视化销售额（各开奖日总销售额的饼图和柱状图）
sales_sum = df.groupby('星期几')['销售额'].sum().reindex(days)

fig, axes = plt.subplots(1, 2, figsize=(12, 5))
# 饼图
colors = plt.cm.rainbow(np.linspace(0,1,len(days)))
sales_sum.plot(
    kind='pie',
    autopct='%.2f%%',
    startangle=90,
    ax=axes[0],
    ylabel='',
    colors=colors
)
axes[0].set_title('各开奖日销售额占比')

# 柱状图
sales_sum.plot(kind='bar', ax=axes[1], colormap='rainbow')
axes[1].set_title('各开奖日总销售额')
axes[1].set_xlabel('星期几')
axes[1].set_ylabel('销售额')

plt.tight_layout()
plt.show()
