import requests
import pandas as pd
import time
import json # 导入json模块，用于美化打印JSON

def scrape_full_rich_list():
    """
    通过循环调用API来获取完整的胡润榜单数据，并自动处理分页。
    """
    
    base_api_url = "https://www.hurun.net/zh-CN/Rank/HsRankDetailsList?num=ODBYW2BI&search=&offset={offset}&limit={limit}"
    
    limit = 20
    offset = 0
    
    all_records = []
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Referer': 'https://www.hurun.net/zh-CN/Rank/HsRankDetails?pagetype=rich',
    }

    print("--- 开始爬取完整榜单（自动翻页）---")
    
    while True:
        current_url = base_api_url.format(offset=offset, limit=limit)
        
        page_num = (offset // limit) + 1
        print(f"\n正在爬取第 {page_num} 页数据...")
        print(f"URL: {current_url}")
        
        try:
            response = requests.get(current_url, headers=headers, timeout=20)
            response.raise_for_status() # 检查HTTP状态码，如果不是200则抛出异常
            data = response.json()

            # --- 调试步骤：打印完整的JSON响应以确认结构 ---
            # 请在遇到问题时取消注释下面两行，查看API返回的实际JSON结构
            # print("--- 原始JSON响应（用于调试）---")
            # print(json.dumps(data, indent=2, ensure_ascii=False)) 
            # print("----------------------------")
            # --- 调试结束 ---

            # 根据您提供的JSON片段，假定完整的富豪列表仍在 'data' -> 'rows' 路径下
            # 但我们会更谨慎地检查每一个层级
            
            if 'rows' in data: # 直接检查根级别是否有 'rows' 键
                new_records = data['rows'] # 直接从根级别获取 'rows'
                if not isinstance(new_records, list):
                    print(f"❌ 错误: 'rows' 存在，但它不是一个列表。实际类型: {type(new_records)}")
                    break # 数据结构不符合预期，退出
            else:
                print(f"❌ 错误: JSON响应中未找到 'rows' 键。")
                print(f"根级别键: {list(data.keys())}") # 打印根级别的所有键，方便排查
                break # 结构不对，退出循环

            # --- 判断是否到达最后一页 ---
            if not new_records:
                print("\n✅ 数据全部加载完毕，没有新内容了。")
                break # 如果返回的数据为空，说明已经爬完了，退出循环
                
            print(f"✅ 成功获取 {len(new_records)} 条新记录。")
            all_records.extend(new_records)
            
            # 准备下一页
            offset += limit
            
            # 礼貌性地暂停一下
            time.sleep(0.5)

        except requests.exceptions.RequestException as e:
            print(f"❌ 错误: 请求第 {page_num} 页时发生网络错误或HTTP错误: {e}")
            break # 网络出错了，也退出循环
        except json.JSONDecodeError as e:
            print(f"❌ 错误: 无法解析第 {page_num} 页的JSON响应: {e}")
            print(f"尝试获取的响应文本: {response.text[:500]}...") # 打印部分响应文本
            break # JSON解析失败，退出循环
        except Exception as e:
            print(f"❌ 发生未知错误: {e}")
            break


    if not all_records:
        print("\n--- 任务失败 ---")
        print("未能爬取到任何数据，请检查网络或API是否已变更。")
        return

    print("\n--- 数据整合 ---")
    print(f"总计爬取到 {len(all_records)} 条记录。")
    df = pd.DataFrame(all_records)
    print("正在将数据转换为表格...")

    output_filename = "胡润百富榜完整数据.csv"
    df.to_csv(output_filename, index=False, encoding='utf-8-sig')

    print(f"\n🎉🎉🎉 任务圆满完成！ 🎉🎉🎉")
    print(f"所有数据已保存至文件: '{output_filename}'")
    
    print("\n数据预览 (前5行):")
    print(df.head())

# --- 程序主入口 ---
if __name__ == '__main__':
    scrape_full_rich_list()