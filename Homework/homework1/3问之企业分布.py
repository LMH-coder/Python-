import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

excel_filename = '胡润百富榜完整数据2.0.xlsx'

headquarters_column = 'hs_Rank_Rich_ComHeadquarters_Cn'

map_filepath = '中华人民共和国.json'

output_image_filename = '公司总部所在地热力图.png'

PROVINCE_LIST = [
    '北京', '上海', '天津', '重庆', '河北', '山西', '辽宁', '吉林', '黑龙江',
    '江苏', '浙江', '安徽', '福建', '江西', '山东', '河南', '湖北', '湖南',
    '广东', '海南', '四川', '贵州', '云南', '陕西', '甘肃', '青海', '台湾',
    '内蒙古', '广西', '西藏', '宁夏', '新疆', '香港', '澳门'
]

def extract_province(location_str):
    if not isinstance(location_str, str):
        return None
    
    for province in PROVINCE_LIST:
        if location_str.startswith(province):
            return province
    return None # 如果循环结束都没找到，说明不是国内地址

def create_headquarters_heatmap(excel_path, map_path, column_name, output_path):
    
    print("开始生成企业总部所在地热力图")
    
    
    try:
        df_rich = pd.read_excel(excel_path)
        print(" 成功读取Excel文件。")
    except FileNotFoundError:
        print(f"错误：找不到Excel文件 '{excel_path}'。")
        return
    except KeyError:
        print(f"错误：找不到名为 '{column_name}' 的列。")
        return

    # 智能提取函数 
    print("正在从地址中智能提取省份信息...")
    df_rich['province'] = df_rich[column_name].apply(extract_province)
    
    # 统计每个省份的企业数量（.dropna() 会自动移除无法匹配的国外地址）
    province_counts = df_rich['province'].dropna().value_counts().reset_index()
    province_counts.columns = ['province', 'count']
    print(" 已统计各省份企业数量：")
    print(province_counts.head())


    try:
        gdf_map = gpd.read_file(map_path)
        print("\n成功读取地图文件。")
    except Exception as e:
        print(f"错误：读取地图文件 '{map_path}' 失败，{e}")
        return

    gdf_map['province_clean'] = gdf_map['name'].str.replace('省|市|自治区|维吾尔|壮族|回族', '', regex=True)
    merged_gdf = gdf_map.merge(province_counts, left_on='province_clean', right_on='province', how='left')
    merged_gdf['count'] = merged_gdf['count'].fillna(0)
    print(" 已将企业数据与地图数据合并。")

    print("\n 正在绘制热力图...")
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    fig, ax = plt.subplots(1, 1, figsize=(15, 12))
    merged_gdf.plot(column='count', cmap='Reds', linewidth=0.8, ax=ax, edgecolor='0.8', legend=True)


    ax.axis('off')
    ax.set_title('胡润百富榜企业总部所在地分布热力图', fontdict={'fontsize': '25', 'fontweight': '3'})
    ax.annotate('数据来源: 胡润百富榜 | 制图: AI Agent', 
                xy=(0.1, .08), xycoords='figure fraction', 
                ha='left', va='top', fontsize=12, color='#555555')
    
    legend = ax.get_legend()
    if legend:
        legend.set_title('企业数量')
    

    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close(fig) 
    
    print(f"\n热力图生成完毕！已保存为图片: {output_path}")

if __name__ == '__main__':
    create_headquarters_heatmap(excel_filename, map_filepath, headquarters_column, output_image_filename)
