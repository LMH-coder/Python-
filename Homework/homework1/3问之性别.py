import pandas as pd
import matplotlib.pyplot as plt

input_filename = '胡润百富榜完整数据2.0.xlsx' 

gender_column = 'hs_Rank_Rich_Gender' 


def create_gender_pie_chart(filename, column_name):
    
    print(f"正在读取数据文件: {filename}...")
    try:
        df = pd.read_excel(filename)
        print("文件读取成功。")
    except FileNotFoundError:
        print(f"错误：找不到文件 '{filename}'")
        return

    # --- 1. 数据清洗 ---
    print(f"正在清洗和分析 '{column_name}' 列...")
    # 筛选出有效数据，排除 '未知' 和空值 (NaN)
    # .copy() 用于避免 pandas 的 SettingWithCopyWarning 警告
    valid_genders = df[df[column_name].notna() & (df[column_name] != '未知')].copy()
    
    if valid_genders.empty:
        print("错误：清洗后没有发现任何有效的性别数据（'先生'或'女士'）。无法生成图表。")
        return

    # --- 2. 数据统计 ---
    gender_counts = valid_genders[column_name].value_counts()
    print("性别统计结果：")
    print(gender_counts)
    
    # --- 3. 准备绘图参数 ---
    
    # 设置中文字体，以防图表中的中文显示为方框
    # 你可以根据你的操作系统选择 'SimHei', 'Microsoft YaHei', 'KaiTi' 等
    plt.rcParams['font.sans-serif'] = ['SimHei'] 
    plt.rcParams['axes.unicode_minus'] = False # 解决负号显示问题

    labels = gender_counts.index
    sizes = gender_counts.values
    
    # 智能“突出”效果：找到数量最少的类别并使其“爆炸”出来
    explode = [0] * len(labels) # 创建一个全为0的列表
    if len(sizes) > 1:
        min_index = sizes.argmin() # 找到最小值的索引
        explode[min_index] = 0.1 # 将最小项的突出值设为0.1
        print(f"\n将突出显示 '{labels[min_index]}' (数量较少者)。")

    # 定义一组柔和、美观的颜色
    colors = ['#66b3ff', '#ff9999'] 
    
    # --- 4. 生成饼状图 ---
    fig, ax = plt.subplots(figsize=(10, 7)) # 创建画布和坐标轴
    
    wedges, texts, autotexts = ax.pie(
        sizes, 
        explode=tuple(explode), # 突出显示部分
        labels=labels,          # 每个扇区的标签
        colors=colors,          # 自定义颜色
        autopct='%1.1f%%',      # 显示百分比，保留一位小数
        shadow=False,           # 核心要求：无阴影
        startangle=90,          # 旋转饼图的起始角度，让布局更好看
        textprops={'fontsize': 14} # 设置标签字体大小
    )

    # 优化图表外观
    ax.axis('equal')  # 确保饼图是正圆形
    plt.setp(autotexts, size=12, weight="bold", color="white") # 设置百分比文字样式
    output_image_filename = '性别分布饼状图.png'
    ax.set_title('胡润百富榜上榜者性别分布', fontsize=20, pad=20) # 设置标题

    print("\n正在生成图表...")
    plt.savefig(output_image_filename, dpi=300, bbox_inches='tight')
    plt.show()
    print("图表已显示。")

# --- 脚本执行入口 ---
if __name__ == "__main__":
    create_gender_pie_chart(input_filename, gender_column)
