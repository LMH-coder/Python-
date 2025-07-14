import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

# --- 文件和列名配置 ---
excel_filename = '胡润百富榜完整数据2.0.xlsx'
# 根据我们之前的数据，出生地信息的列名是 'hs_Rank_Rich_BirthPlace_Cn'
birthplace_column = 'hs_Rank_Rich_BirthPlace_Cn'
# 地图文件的路径
map_filepath = '中华人民共和国.json' 

def create_birthplace_heatmap(excel_path, map_path, column_name):
    """
    读取富豪数据和中国地图，生成出生地分布热力图。
    """
    print("--- 开始生成富豪出生地热力图 ---")
    
    # --- 1. 读取并处理富豪数据 ---
    try:
        df_rich = pd.read_excel(excel_path)
        print("✅ 成功读取Excel文件。")
    except FileNotFoundError:
        print(f"❌ 错误：找不到Excel文件 '{excel_path}'。")
        return

    # 清理出生地数据：提取省份
    # 数据格式为 '中国-福建-龙岩'，我们只需要 '福建'
    # 使用 .str.split() 分割字符串，然后取第二个元素
    # dropna() 会移除那些出生地为空的记录
    df_rich['province'] = df_rich[column_name].dropna().str.split('-').str[1]
    
    # 统计每个省份的富豪数量
    province_counts = df_rich['province'].value_counts().reset_index()
    province_counts.columns = ['province', 'count']
    print("✅ 已统计各省份富豪数量：")
    print(province_counts.head())

    # --- 2. 读取地图数据 ---
    try:
        gdf_map = gpd.read_file(map_path)
        print("\n✅ 成功读取地图文件。")
    except Exception as e:
        print(f"❌ 错误：读取地图文件 '{map_path}' 失败。请确保文件存在且未损坏。错误信息: {e}")
        return

    # --- 3. 合并数据 ---
    # 将我们的统计数据合并到地理信息数据上
    # GeoDataFrame的 'name' 列通常是省份名，我们需要确保它和我们的 'province' 列能匹配上
    # 为了稳妥，我们对两边的省份名做一点清洗，去掉'省','市'等字样
    gdf_map['province_clean'] = gdf_map['name'].str.replace('省|市|自治区|维吾尔|壮族|回族', '', regex=True)
    
    # 合并两个数据集
    merged_gdf = gdf_map.merge(province_counts, left_on='province_clean', right_on='province', how='left')
    
    # 对于没有富豪的省份，其 'count' 会是 NaN，我们用 0 填充
    merged_gdf['count'] = merged_gdf['count'].fillna(0)
    print("✅ 已将富豪数据与地图数据合并。")

    # --- 4. 绘制地图 ---
    print("\n🎨 正在绘制热力图...")
    
    # 设置中文字体
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False

    # 创建一个足够大的画布
    fig, ax = plt.subplots(1, 1, figsize=(15, 12))

    # 绘制地图，颜色根据 'count' 列的值变化
    # cmap='OrRd' 是一个从橙色到红色的色带，很适合做热力图
    merged_gdf.plot(column='count', cmap='OrRd', linewidth=0.8, ax=ax, edgecolor='0.8', legend=True)

    # --- 5. 美化图表 ---
    # 移除坐标轴
    ax.axis('off')

    # 添加标题
    ax.set_title('胡润百富榜出生地分布热力图', fontdict={'fontsize': '25', 'fontweight': '3'})
    
    # 在地图下方添加数据来源说明
    ax.annotate('数据来源: 胡润百富榜 | 制图: AI Agent', 
                xy=(0.1, .08), xycoords='figure fraction', 
                ha='left', va='top', fontsize=12, color='#555555')

    output_image_filename = '富豪出生地热力图.png'
    # 获取图例对象并修改
    legend = ax.get_legend()
    if legend:
        legend.set_title('富豪数量')
        
    plt.savefig(output_image_filename, dpi=300, bbox_inches='tight')
    plt.show()
    print("🎉 热力图生成完毕！")

# --- 脚本执行入口 ---
if __name__ == '__main__':
    create_birthplace_heatmap(excel_filename, map_filepath, birthplace_column)
