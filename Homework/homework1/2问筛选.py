import pandas as pd

# --- 1. 参数配置 ---
# *** 您需要修改的部分 ***
# 因为您的脚本和CSV文件在同一个文件夹，所以可以直接写文件名。
# 这种方式是最佳实践，因为代码不依赖于具体的盘符和用户目录。
input_csv_path = '胡润百富榜完整数据.csv'

# 如果您不想把它们放一起，也可以使用绝对路径，注意路径的写法。
# 写法1 (推荐): 使用r''来防止转义字符问题
# input_csv_path = r'C:\Users\cucopestle\Desktop\胡润百富榜完整数据.csv'
# 写法2: 使用双反斜杠'\\'
# input_csv_path = 'C:\\Users\\cucopestle\\Desktop\\胡润百富榜完整数据.csv'

# 输出的Excel文件名（它将被保存在与脚本相同的文件夹中）
output_excel_path = '各行业财富与富豪数量统计报告.xlsx'

# 根据test表确定的列名，这部分无需修改
industry_column = 'hs_Rank_Rich_Industry_Cn'
wealth_column = 'hs_Rank_Rich_Wealth'
person_column = 'hs_Character'

# --- 2. 加载并处理数据 ---
try:
    # 使用 pandas 读取您本地的CSV文件
    df = pd.read_csv(input_csv_path)
    print(f"成功加载文件: {input_csv_path}")
    print(f"数据共有 {len(df)} 行。")

except FileNotFoundError:
    # 这里的错误提示现在对您本地环境更有意义了
    print(f"错误：未能找到文件 '{input_csv_path}'。")
    print("请确认：1. CSV文件名是否正确；2. Python脚本和CSV文件是否在同一个文件夹下。")
    exit() # 如果文件未找到，则停止执行

# --- 3. 数据清洗与预处理 ---
df_cleaned = df.dropna(subset=[industry_column, wealth_column])
print(f"数据清洗后，剩余 {len(df_cleaned)} 行有效数据进行分析。")

df_cleaned[wealth_column] = pd.to_numeric(df_cleaned[wealth_column], errors='coerce')
df_cleaned = df_cleaned.dropna(subset=[wealth_column])
print(f"财富值转换为数字后，剩余 {len(df_cleaned)} 行可用于计算。")

# --- 4. 核心统计分析 ---
print("正在按行业统计富豪数量和总财富...")
industry_analysis = df_cleaned.groupby(industry_column).agg(
    富豪数量=(person_column, 'count'),
    行业总财富=(wealth_column, 'sum')
)

# --- 5. 结果整理与输出 ---
industry_analysis = industry_analysis.reset_index()
industry_analysis_sorted = industry_analysis.sort_values(by='行业总财富', ascending=False)
industry_analysis_sorted = industry_analysis_sorted.rename(columns={industry_column: '行业'})
industry_analysis_sorted.to_excel(output_excel_path, index=False)

# --- 6. 完成与展示 ---
print("\n🎉 分析完成！")
print(f"统计报告已成功生成并保存至: {output_excel_path}")
print("\n--- 各行业财富与富豪数量统计概览 (按总财富排名前10) ---")
# 使用 to_string() 保证在终端能对齐显示
print(industry_analysis_sorted.head(10).to_string())
