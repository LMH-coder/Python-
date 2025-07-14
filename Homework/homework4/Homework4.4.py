#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

def main():
    # 1. 读取数据（假设 CSV 文件在脚本同目录下）
    df = pd.read_csv('专家.csv', encoding='utf-8')

    # 2. 选取用于分析的列
    cols = [
        '彩龄',
        '文章数量',
        '大乐透一等奖次数',
        '大乐透二等奖次数',
        '大乐透三等奖次数',
        '总得分'
    ]
    data = df[cols]

    # 3. 绘制 QQ 图（检验正态性）并美化
    plt.figure(figsize=(12, 8))
    for i, col in enumerate(cols):
        plt.subplot(2, 3, i+1)
        stats.probplot(data[col], dist='norm', plot=plt)
        plt.title(f'QQ 图 — {col}', fontsize=12)
    plt.tight_layout()
    plt.show()

    # 4. 计算 Pearson 相关系数矩阵
    corr = data.corr()

    # 5. 绘制相关系数热力图（美化）
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5, cbar=True, vmin=-1, vmax=1, 
                annot_kws={'size': 12, 'weight': 'bold'}, cbar_kws={'label': '相关性'})
    plt.title('相关系数热力图', fontsize=16)
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    plt.tight_layout()
    plt.show()

    # 6. 计算 Pearson 相关性假设检验的 p 值矩阵
    pvals = pd.DataFrame(np.ones((len(cols), len(cols))), index=cols, columns=cols)
    for i in range(len(cols)):
        for j in range(i+1, len(cols)):
            _, p = stats.pearsonr(data[cols[i]], data[cols[j]])
            pvals.iloc[i, j] = p
            pvals.iloc[j, i] = p

    # 7. 绘制 p 值热力图（美化）
    plt.figure(figsize=(10, 8))
    sns.heatmap(pvals.astype(float), annot=True, cmap='Blues', fmt='.4f', linewidths=0.5, cbar=True,
                annot_kws={'size': 12, 'weight': 'bold'}, cbar_kws={'label': 'p 值'})
    plt.title('p 值热力图', fontsize=16)
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    plt.tight_layout()
    plt.show()

    # 8. 可视化专家信息：彩龄、文章数量、获奖情况和总得分
    # 8.1 彩龄分布直方图
    plt.figure(figsize=(10, 6))
    sns.histplot(df['彩龄'], kde=True, color='teal', bins=15, stat='density')
    plt.title('彩龄分布图', fontsize=16)
    plt.xlabel('彩龄（年）', fontsize=12)
    plt.ylabel('密度', fontsize=12)
    plt.tight_layout()
    plt.show()

    # 8.2 文章数量分布直方图
    plt.figure(figsize=(10, 6))
    sns.histplot(df['文章数量'], kde=True, color='orange', bins=20, stat='density')
    plt.title('文章数量分布图', fontsize=16)
    plt.xlabel('文章数量', fontsize=12)
    plt.ylabel('密度', fontsize=12)
    plt.tight_layout()
    plt.show()

    # 8.3 获奖次数分布（一等奖、二等奖、三等奖）
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    sns.histplot(df['大乐透一等奖次数'], kde=True, color='blue', bins=10, stat='density', ax=axes[0])
    sns.histplot(df['大乐透二等奖次数'], kde=True, color='green', bins=10, stat='density', ax=axes[1])
    sns.histplot(df['大乐透三等奖次数'], kde=True, color='red', bins=10, stat='density', ax=axes[2])
    axes[0].set_title('一等奖次数分布', fontsize=16)
    axes[1].set_title('二等奖次数分布', fontsize=16)
    axes[2].set_title('三等奖次数分布', fontsize=16)
    plt.tight_layout()
    plt.show()

    # 8.4 总得分分布箱型图
    plt.figure(figsize=(8, 6))
    sns.boxplot(x=df['总得分'], color='purple')
    plt.title('总得分箱型图', fontsize=16)
    plt.xlabel('总得分', fontsize=12)
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    main()
