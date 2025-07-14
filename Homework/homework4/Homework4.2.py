import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random

# 保证中文和负号正常显示
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 1. 读取并预处理数据
file_path = '超级大乐透.xlsx'  # 修改为您的实际路径
df = pd.read_excel(file_path, sheet_name='Sheet1', parse_dates=['开奖日期'])
df = df.sort_values('开奖日期', ascending=False).reset_index(drop=True)

# 2. 拆分位置列
# 前区 5 位
front_df = df['前区号码'].str.split(expand=True).astype(int)
front_df.columns = [f'前区位{i}' for i in range(1, 6)]
# 后区 2 位
back_df = df['后区号码'].str.split(expand=True).astype(int)
back_df.columns = [f'后区位{i}' for i in range(1, 3)]

# —— 将拆分出的列拼回原 df —— 
df = pd.concat([df, front_df, back_df], axis=1)

# 3. 非加权频率统计 & 可视化
cmap_map = {
    '前区位1': plt.cm.rainbow,
    '前区位2': plt.cm.autumn,
    '前区位3': plt.cm.viridis,
    '前区位4': plt.cm.plasma,
    '前区位5': plt.cm.cool,
    '后区位1': plt.cm.magma,
    '后区位2': plt.cm.inferno
}

for col in list(front_df.columns) + list(back_df.columns):
    vals = df[col]
    freq = vals.value_counts().sort_index()

    plt.figure(figsize=(8, 3))
    colors = cmap_map[col](np.linspace(0, 1, len(freq)))
    plt.bar(freq.index, freq.values, color=colors)
    plt.title(f'{col} 历史频率分布（非加权）')
    plt.xlabel('号码')
    plt.ylabel('出现次数')
    plt.tight_layout()
    plt.show()

# 4. 指数衰减加权频率计算
gamma = 0.1
df['rank'] = np.arange(1, len(df) + 1)
df['weight'] = gamma * (1 - gamma) ** (df['rank'] - 1)

def weighted_freq(pos_col, max_num):
    arr = df[[pos_col, 'weight']].values
    w = np.zeros(max_num + 1)
    for num, wt in arr:
        w[int(num)] += wt
    probs = w[1:] / w[1:].sum()
    return dict(zip(range(1, max_num + 1), probs))

# 5. 加权概率可视化 & 存储分布
front_weighted = {}
back_weighted  = {}

for col in front_df.columns:
    dist = weighted_freq(col, 35)
    front_weighted[col] = dist

    plt.figure(figsize=(8, 3))
    colors = cmap_map[col](np.linspace(0, 1, 35))
    plt.bar(list(dist.keys()), list(dist.values()), color=colors)
    plt.title(f'{col} 指数衰减加权概率分布')
    plt.xlabel('号码')
    plt.ylabel('概率')
    plt.tight_layout()
    plt.show()

for col in back_df.columns:
    dist = weighted_freq(col, 12)
    back_weighted[col] = dist

    plt.figure(figsize=(8, 3))
    colors = cmap_map[col](np.linspace(0, 1, 12))
    plt.bar(list(dist.keys()), list(dist.values()), color=colors)
    plt.title(f'{col} 指数衰减加权概率分布')
    plt.xlabel('号码')
    plt.ylabel('概率')
    plt.tight_layout()
    plt.show()

# 6. 基于加权概率逐位抽样推荐号码（去掉随机种子可获得不同结果）
random.seed(42)
recommend_front = []
for col in front_df.columns:
    nums, probs = zip(*sorted(front_weighted[col].items()))
    recommend_front.append(random.choices(nums, weights=probs, k=1)[0])

recommend_back = []
for col in back_df.columns:
    nums, probs = zip(*sorted(back_weighted[col].items()))
    recommend_back.append(random.choices(nums, weights=probs, k=1)[0])

print("推荐号码（基于指数加权、逐位抽样）：")
print("前区：", recommend_front)
print("后区：", recommend_back)
