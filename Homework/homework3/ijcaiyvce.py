import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

# 输入数据
years = np.array([2020, 2021, 2022, 2023, 2024]).reshape(-1, 1)
papers = np.array([778, 721, 863, 846, 1048])

# 创建并训练线性回归模型
model = LinearRegression()
model.fit(years, papers)

# 预测2025年
year_2025 = np.array([[2025]])
prediction_2025 = model.predict(year_2025)[0]

# 计算R²得分
r2 = r2_score(papers, model.predict(years))

# 可视化结果
plt.figure(figsize=(10, 6))
plt.scatter(years, papers, color='blue', label='Actual Data')
plt.plot(years, model.predict(years), color='red', label='Linear Regression')
plt.scatter(year_2025, prediction_2025, color='green', marker='*', s=200, label='2025 Prediction')
plt.title('IJCAI Conference Paper Count Prediction (Linear Regression)', fontsize=14)
plt.xlabel('Year', fontsize=12)
plt.ylabel('Number of Papers', fontsize=12)
plt.legend()
plt.grid(True)
plt.xticks(np.arange(2020, 2026, 1))

# 显示回归方程和R²值
equation = f'y = {model.coef_[0]:.1f}x + {model.intercept_:.1f}'
plt.text(2020.5, 950, f'{equation}\nR² = {r2:.3f}', fontsize=12, bbox=dict(facecolor='white', alpha=0.8))

plt.show()

print(f"Linear regression equation: {equation}")
print(f"Predicted number of papers for 2025: {int(prediction_2025)}")
print(f"Model R-squared score: {r2:.3f}")