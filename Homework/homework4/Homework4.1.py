import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_squared_error

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 1. 加载数据
file_path = '超级大乐透.xlsx'  # 请确保该文件在当前工作目录下
df = pd.read_excel(file_path, sheet_name=0)

# 2. 选择与“天数”和“销售额”相关的列
df = df[['天数', '销售额']]

# 3. 特征和目标变量
X = df[['天数']]
y = df['销售额']

# 4. 数据标准化
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 5. 训练集和测试集划分（80%训练，20%测试）
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42
)

# 6. 网格搜索：多项式阶数 1-10，正则化项 alpha 取值 [0.1, 1, 10, 100]
best_mse = float('inf')
best_degree = None
best_alpha = None
best_model = None
best_poly = None

for degree in range(1, 11):
    poly = PolynomialFeatures(degree=degree)
    X_train_poly = poly.fit_transform(X_train)
    X_test_poly = poly.transform(X_test)
    
    for alpha in [0.1, 0.2, 0.3, 0.4, 0.5, 1, 10, 100]:
        model = Ridge(alpha=alpha)
        model.fit(X_train_poly, y_train)
        y_pred_test = model.predict(X_test_poly)
        mse = mean_squared_error(y_test, y_pred_test)
        
        if mse < best_mse:
            best_mse = mse
            best_degree = degree
            best_alpha = alpha
            best_model = model
            best_poly = poly

# 7. 输出最佳模型参数
print(f"最佳多项式阶数: {best_degree}")
print(f"最佳正则化系数 alpha: {best_alpha}")
print(f"测试集 MSE: {best_mse:.2f}\n")

# 8. 在测试集上预测并可视化对比
X_test_poly = best_poly.transform(X_test)
y_test_pred = best_model.predict(X_test_poly)

plt.figure(figsize=(8, 6))
plt.scatter(y_test, y_test_pred, label='预测 vs 实际')
plt.plot([y_test.min(), y_test.max()],
         [y_test.min(), y_test.max()],
         'r--', label='完美拟合')
plt.xlabel('实际销售额')
plt.ylabel('预测销售额')
plt.title('测试集：实际值 vs 预测值')
plt.legend()
plt.tight_layout()
plt.show()

# 9. 拼接并输出拟合方程
coefs = best_model.coef_
intercept = best_model.intercept_
terms = [f"{intercept:.2f}"]
for i, c in enumerate(coefs[1:], 1):
    terms.append(f"{c:.2f} * X^{i}")
equation = " + ".join(terms)
print("拟合方程:")
print(f"Sales = {equation}\n")

# 10. 预测2025年7月1日之后三天的销售额
# 假设最后一个“天数”值为 df['天数'].max()
last_day = df['天数'].max()
future_days = np.array([[last_day + i] for i in range(1, 4)])
future_days_scaled = scaler.transform(future_days)
future_days_poly = best_poly.transform(future_days_scaled)
future_sales = best_model.predict(future_days_poly)

for i, sale in enumerate(future_sales, 1):
    date = pd.to_datetime('2025-07-01') + pd.Timedelta(days=(i-1))
    print(f"{date.strftime('%Y-%m-%d')} 预测销售额: {sale:.2f} 元")

