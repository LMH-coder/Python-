import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

# 输入数据
years = np.array([2020, 2021, 2022, 2023, 2024, 2025]).reshape(-1, 1)
papers = np.array([1864, 1961, 1624, 2021, 2866, 3486])

# 创建并训练线性回归模型
model = LinearRegression()
model.fit(years, papers)

# 预测2026年
year_2026 = np.array([[2026]])
prediction_2026 = model.predict(year_2026)[0]

# 计算R²得分
r2 = r2_score(papers, model.predict(years))

# 可视化结果
plt.figure(figsize=(12, 7))
plt.scatter(years, papers, color='blue', s=100, label='Actual Data')
plt.plot(years, model.predict(years), color='red', linewidth=3, label='Linear Regression')
plt.scatter(year_2026, prediction_2026, color='green', marker='*', s=300, label='2026 Prediction')

# 标注每个数据点
for i, txt in enumerate(papers):
    plt.annotate(txt, (years[i], papers[i]), textcoords="offset points", xytext=(0,10), ha='center')

plt.title('AAAI Conference Paper Count Prediction (2020-2026)', fontsize=16, pad=20)
plt.xlabel('Year', fontsize=14, labelpad=10)
plt.ylabel('Number of Papers', fontsize=14, labelpad=10)
plt.legend(fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)
plt.xticks(np.arange(2020, 2027, 1), fontsize=12)
plt.yticks(fontsize=12)

# 显示回归方程和R²值
equation = f'Regression Line: y = {model.coef_[0]:.1f}x + {model.intercept_:.1f}'
r2_text = f'R² = {r2:.3f} (Excellent Fit)' if r2 > 0.9 else f'R² = {r2:.3f}'
plt.text(2020.5, 2200, f'{equation}\n{r2_text}', fontsize=13, 
         bbox=dict(facecolor='white', edgecolor='gray', boxstyle='round,pad=0.5'))

# 添加趋势分析注释
trend_note = "• 2022 dip likely due to pandemic\n• Significant growth in 2024-2025"
plt.text(2024.2, 1500, trend_note, fontsize=11, 
         bbox=dict(facecolor='lightyellow', alpha=0.8))

plt.tight_layout()
plt.show()

# 控制台输出详细分析
print("\n" + "="*60)
print("AAAI Conference Paper Submission Trend Analysis".center(60))
print("="*60)
print(f"\nRegression Equation: {equation}")
print(f"2026 Prediction: {int(prediction_2026)} papers")
print(f"\nKey Insights:")
print(f"- Annual Growth Rate: {model.coef_[0]:.1f} papers per year")
print(f"- 2022 Anomaly: {papers[2]} papers (likely pandemic impact)")
print(f"- Recent Surge: {papers[5]-papers[4]} paper increase from 2024 to 2025")
print(f"\nModel Evaluation:")
print(f"- R-squared: {r2:.3f} ({'Strong correlation' if r2 > 0.8 else 'Moderate correlation'})")
print("- The model explains {:.1f}% of variance".format(r2*100))
print("\n" + "="*60)