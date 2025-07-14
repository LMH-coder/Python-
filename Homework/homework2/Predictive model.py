import matplotlib

matplotlib.use('TkAgg')
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.statespace.sarimax import SARIMAX


def prepare_data():
    # 读取历史数据 (2022-2024)
    df = pd.read_csv('output/clean_大连天气_2022-2024.csv')
    df['日期'] = pd.to_datetime(df['日期'], format='%Y年%m月%d日')
    df['年份'] = df['日期'].dt.year
    df['月份'] = df['日期'].dt.month

    # 计算每月平均最高温度
    monthly_avg = df.groupby(['年份', '月份'])['最高温度'].mean().reset_index()

    # 创建时间序列
    history_ts = pd.Series(
        monthly_avg['最高温度'].values,
        index=pd.to_datetime(
            monthly_avg['年份'].astype(str) + '-' +
            monthly_avg['月份'].astype(str) + '-01'
        )
    )

    # 读取2025年实际数据
    actual_2025 = pd.read_csv('output/大连天气_2025_1-6月.csv')
    actual_2025['日期'] = pd.to_datetime(actual_2025['日期'], format='%Y年%m月%d日')
    actual_2025_avg = actual_2025.groupby(actual_2025['日期'].dt.to_period('M'))['最高温度'].mean()

    return history_ts, actual_2025_avg


def model_and_predict(history_ts, actual_2025_avg):
    # 建立SARIMA模型
    model = SARIMAX(history_ts,
                    order=(1, 0, 1),
                    seasonal_order=(0, 1, 1, 12),
                    enforce_stationarity=False,
                    enforce_invertibility=False)

    model_fit = model.fit(disp=False)

    # 预测2025年1-6月
    forecast = model_fit.get_forecast(steps=6)
    forecast_mean = forecast.predicted_mean
    conf_int = forecast.conf_int()

    # 可视化
    plt.figure(figsize=(10, 6))
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
    month_numbers = range(1, 7)

    # 置信区间
    plt.fill_between(month_numbers,
                     conf_int.iloc[:, 0],
                     conf_int.iloc[:, 1],
                     color='lightcoral', alpha=0.3, label='95% Confidence Interval')

    # 预测值
    plt.plot(month_numbers, forecast_mean.values, 'r--o', label='Forecast', linewidth=2)

    # 实际值
    actual_dates = pd.to_datetime(actual_2025_avg.index.to_timestamp())
    plt.plot(month_numbers, actual_2025_avg.values, 'b-s', label='Actual', linewidth=2)

    # 添加数据标签
    for i, (month, temp) in enumerate(zip(months, forecast_mean)):
        plt.text(i + 1, temp + 0.5, f'{temp:.1f}°C', ha='center', color='red', fontweight='bold')

    for i, (month, temp) in enumerate(zip(months, actual_2025_avg)):
        plt.text(i + 1, temp - 0.8, f'{temp:.1f}°C', ha='center', color='blue', fontweight='bold')

    plt.title('Dalian Monthly Average High Temperature (2025 Jan-Jun)', fontsize=14)
    plt.xlabel('Month', fontsize=12)
    plt.ylabel('Temperature (°C)', fontsize=12)
    plt.xticks(month_numbers, months)
    plt.legend(loc='upper left')
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.show()

    return forecast_mean, conf_int


if __name__ == "__main__":
    # 数据准备
    history_ts, actual_2025_avg = prepare_data()

    # 建模与预测
    forecast_mean, conf_int = model_and_predict(history_ts, actual_2025_avg)

    # 打印预测结果
    print("\n2025年预测结果:")
    for month, temp, lower, upper in zip(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
                                         forecast_mean,
                                         conf_int.iloc[:, 0],
                                         conf_int.iloc[:, 1]):
        print(f"{month}: {temp:.1f}°C (95% CI: {lower:.1f}~{upper:.1f})")