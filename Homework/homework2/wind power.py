import pandas as pd
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import seaborn as sns


# 1. 数据准备和预处理
def load_and_preprocess_data():
    # 读取数据
    data = pd.read_csv('output/clean_大连天气_2022-2024.csv')

    # 转换日期列并提取年月信息
    data['日期'] = pd.to_datetime(data['日期'], format='%Y年%m月%d日')
    data['年份'] = data['日期'].dt.year
    data['月份'] = data['日期'].dt.month

    # 定义风力等级分类函数
    def classify_wind(wind_str):
        if pd.isna(wind_str) or wind_str == '无持续风向':
            return '0级'
        if '1-2级' in wind_str:
            return '1-2级'
        if '3-4级' in wind_str:
            return '3-4级'
        if '4-5级' in wind_str:
            return '4-5级'
        if '5-6级' in wind_str:
            return '5-6级'
        if '6-7级' in wind_str or '7-8级' in wind_str:
            return '6级以上'
        return '其他'

    # 对白天和夜晚风力进行分类
    data['白天风力等级'] = data['白天风力'].apply(classify_wind)
    data['夜晚风力等级'] = data['夜晚风力'].apply(classify_wind)

    return data


# 2. 创建对比柱状图
def create_wind_comparison_plots(data):
    # 设置风格 - 使用seaborn风格和正确的matplotlib样式
    sns.set_theme(style="whitegrid")
    plt.style.use('ggplot')  # 使用一个可用的样式，如'ggplot'

    # 设置中文字体
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

    # 创建画布
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 8), dpi=120)
    plt.subplots_adjust(wspace=0.3)

    # 颜色方案
    palette = sns.color_palette("YlOrBr", n_colors=5)[::-1]

    # ========== 白天风力 ==========
    # 统计各月份风力分布
    day_wind = data.groupby(['月份', '白天风力等级']).size().unstack(fill_value=0)
    day_wind = day_wind[['1-2级', '3-4级', '4-5级', '5-6级', '6级以上']]

    # 计算三年平均值
    day_avg = day_wind / 3

    # 绘制柱状图
    day_avg.plot(
        kind='bar',
        stacked=True,
        color=palette,
        width=0.8,
        edgecolor='white',
        linewidth=0.5,
        ax=ax1
    )

    # 美化图表
    ax1.set_title('1-12月白天风力等级分布(2022-2024年平均)',
                  fontsize=14, pad=15, fontweight='bold')
    ax1.set_xlabel('月份', fontsize=12, labelpad=10)
    ax1.set_ylabel('平均天数', fontsize=12, labelpad=10)
    ax1.set_xticklabels(range(1, 13), rotation=0)
    ax1.grid(axis='y', linestyle='--', alpha=0.7)

    # 添加数据标签
    for i in range(12):
        height = 0
        for level in day_avg.columns:
            value = day_avg.iloc[i][level]
            if value > 2.5:  # 只显示较大的值
                ax1.text(
                    i,
                    height + value / 2,
                    f"{value:.1f}",
                    ha='center',
                    va='center',
                    fontsize=9,
                    color='white' if level in ['4-5级', '5-6级', '6级以上'] else 'black'
                )
            height += value

    # ========== 夜晚风力 ==========
    # 统计各月份风力分布
    night_wind = data.groupby(['月份', '夜晚风力等级']).size().unstack(fill_value=0)
    night_wind = night_wind[['1-2级', '3-4级', '4-5级', '5-6级', '6级以上']]

    # 计算三年平均值
    night_avg = night_wind / 3

    # 绘制柱状图
    night_avg.plot(
        kind='bar',
        stacked=True,
        color=palette,
        width=0.8,
        edgecolor='white',
        linewidth=0.5,
        ax=ax2
    )

    # 美化图表
    ax2.set_title('1-12月夜晚风力等级分布(2022-2024年平均)',
                  fontsize=14, pad=15, fontweight='bold')
    ax2.set_xlabel('月份', fontsize=12, labelpad=10)
    ax2.set_ylabel('平均天数', fontsize=12, labelpad=10)
    ax2.set_xticklabels(range(1, 13), rotation=0)
    ax2.grid(axis='y', linestyle='--', alpha=0.7)

    # 添加数据标签
    for i in range(12):
        height = 0
        for level in night_avg.columns:
            value = night_avg.iloc[i][level]
            if value > 2.5:
                ax2.text(
                    i,
                    height + value / 2,
                    f"{value:.1f}",
                    ha='center',
                    va='center',
                    fontsize=9,
                    color='white' if level in ['4-5级', '5-6级', '6级以上'] else 'black'
                )
            height += value

    # 添加统一图例
    handles, labels = ax1.get_legend_handles_labels()
    fig.legend(
        handles, labels,
        title='风力等级',
        loc='upper center',
        bbox_to_anchor=(0.5, 1.05),
        ncol=5,
        frameon=True,
        fontsize=11,
        title_fontsize=12
    )

    # 移除子图原有图例
    ax1.get_legend().remove()
    ax2.get_legend().remove()

    # 保存和显示
    plt.tight_layout()
    plt.savefig('monthly_wind_comparison.png', bbox_inches='tight', dpi=300)
    plt.show()


# 主程序
if __name__ == "__main__":
    # 加载和处理数据
    weather_data = load_and_preprocess_data()

    # 创建对比柱状图
    print("正在生成1-12月白天和夜晚风力等级对比图...")
    create_wind_comparison_plots(weather_data)
    print("可视化已完成！图表已保存为monthly_wind_comparison.png")