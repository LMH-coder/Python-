import requests
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm
import time
import os

def scrape_aaai_from_dblp(start_year=2020):
    """
    从DBLP爬取AAAI会议论文信息(2020年至今)
    
    参数:
        start_year (int): 起始年份，默认为2020
        
    返回:
        pd.DataFrame: 包含论文信息的DataFrame
    """
    base_url = "https://dblp.org/db/conf/aaai/"
    papers = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    print("开始从DBLP爬取AAAI会议论文信息...")
    
    for year in tqdm(range(start_year, 2026), desc="处理年份"):
        url = f"{base_url}aaai{year}.html"
        try:
            # 添加延迟避免被封
            time.sleep(1)
            
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            
            # 检查响应内容是否为HTML
            if 'html' not in response.headers.get('Content-Type', ''):
                print(f"警告: {year}年返回的内容可能不是HTML")
                continue
                
            soup = BeautifulSoup(response.text, 'html.parser')
            entries = soup.find_all('li', class_='entry inproceedings')
            
            if not entries:
                print(f"警告: {year}年没有找到论文条目")
                continue
                
            for paper_entry in tqdm(entries, desc=f"处理{year}年论文", leave=False):
                try:
                    # 提取标题
                    title_elem = paper_entry.find('span', class_='title')
                    title = title_elem.text if title_elem else "无标题"
                    
                    # 提取作者
                    authors = [a.text for a in paper_entry.find_all('span', itemprop='author')]
                    
                    # 提取链接
                    doi_tag = paper_entry.find('a', {'itemprop': 'url'})
                    url = doi_tag['href'] if doi_tag else None
                    
                    # 提取DOI (如果有)
                    doi = None
                    if url and 'doi.org' in url:
                        doi = url.split('doi.org/')[-1]
                    
                    paper_info = {
                        "title": title,
                        "authors": ", ".join(authors),  # 将作者列表转为字符串
                        "year": year,
                        "conference": f"AAAI {year}",
                        "url": url,
                        "doi": doi
                    }
                    papers.append(paper_info)
                    
                except Exception as e:
                    print(f"处理{year}年某篇论文时出错: {str(e)}")
                    continue
                    
        except requests.exceptions.RequestException as e:
            print(f"获取{year}年数据时网络错误: {str(e)}")
            continue
        except Exception as e:
            print(f"处理{year}年数据时出错: {str(e)}")
            continue
    
    return pd.DataFrame(papers)

def save_to_excel(df, filename):
    """保存DataFrame到Excel文件"""
    try:
        # 确保输出目录存在
        os.makedirs('output', exist_ok=True)
        
        # 移除文件扩展名(如果有)
        filename = os.path.splitext(filename)[0]
        
        # 设置完整文件路径
        csv_path = os.path.join('output', f"{filename}.csv")
        excel_path = os.path.join('output', f"{filename}.xlsx")
        
        # 先保存为CSV
        df.to_csv(csv_path, index=False, encoding='utf-8-sig')
        print(f"数据已临时保存为CSV: {csv_path}")
        
        # 将CSV转换为Excel
        # 重新读取CSV文件以确保编码正确
        df_from_csv = pd.read_csv(csv_path, encoding='utf-8-sig')
        
        # 使用ExcelWriter保存为XLSX格式
        with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
            df_from_csv.to_excel(writer, index=False, sheet_name='AAAI Papers')
        
        print(f"数据已成功转换为Excel: {excel_path}")
        
        # 可选: 删除临时CSV文件
        # os.remove(csv_path)
        # print("临时CSV文件已删除")
        
    except Exception as e:
        print(f"保存文件时出错: {str(e)}")

if __name__ == "__main__":
    try:
        # 获取数据
        print("正在从DBLP获取AAAI会议论文...")
        aaai_papers_df = scrape_aaai_from_dblp()
        
        # 显示前几行数据
        if not aaai_papers_df.empty:
            print("\n获取到的论文样例:")
            print(aaai_papers_df.head())
            
            # 保存到Excel
            save_to_excel(aaai_papers_df, "aaai_papers_2020_present.xlsx")
        else:
            print("警告: 没有获取到任何论文数据")
            
    except KeyboardInterrupt:
        print("\n用户中断了程序")
    except Exception as e:
        print(f"程序运行出错: {str(e)}")