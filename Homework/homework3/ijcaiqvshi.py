import matplotlib.pyplot as plt
import seaborn as sns
from ijcaixx import scrape_ijcai_from_dblp  # 修改导入函数

def analyze_ijcai_papers():
    # 从DBLP获取IJCAI论文数据
    print("正在获取IJCAI会议论文数据...")
    ijcai_papers_df = scrape_ijcai_from_dblp(start_year=2020)
    
    if ijcai_papers_df.empty:
        print("没有获取到论文数据，无法进行分析")
        return
    
    # 统计各年份的论文数量
    paper_counts = ijcai_papers_df['year'].value_counts().sort_index()
    
    # 设置图表样式
    plt.style.use('seaborn-v0_8')
    plt.figure(figsize=(12, 6))
    
    # 创建柱状图
    ax = sns.barplot(x=paper_counts.index.astype(str), 
                    y=paper_counts.values,
                    palette="Blues_d")
    
    # 添加数据标签
    for p in ax.patches:
        ax.annotate(f"{int(p.get_height())}", 
                   (p.get_x() + p.get_width() / 2., p.get_height()),
                   ha='center', va='center', 
                   xytext=(0, 10), 
                   textcoords='offset points')
    
    # 设置图表标题和标签
    plt.title('IJCAI Conference Papers Count (2020-2025)', fontsize=16, pad=20)
    plt.xlabel('Year', fontsize=12)
    plt.ylabel('Number of Papers', fontsize=12)
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)
    
    # 调整布局
    plt.tight_layout()
    
    # 保存图表
    plt.savefig('ijcai_papers_trend.png', dpi=300, bbox_inches='tight')
    print("图表已保存为 ijcai_papers_trend.png")
    
    # 显示图表
    plt.show()
    
    # 打印统计摘要
    print("\nIJCAI会议论文统计摘要:")
    print(paper_counts.to_string())

if __name__ == "__main__":
    analyze_ijcai_papers()  # 修改主函数调用