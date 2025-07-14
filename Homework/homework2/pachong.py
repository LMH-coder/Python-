import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timedelta
import time
import os


def get_monthly_weather(year_month):
    base_url = "http://www.tianqihoubao.com/lishi/dalian/month/{}.html"
    url = base_url.format(year_month)

    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers)

        # 关键修改：先检查实际编码，再设置解码方式
        if 'charset=gbk' in response.text.lower() or 'charset=gb2312' in response.text.lower():
            response.encoding = 'gbk'
        else:
            response.encoding = response.apparent_encoding  # 自动检测编码

        print("正确解码后的内容示例:", response.text[:500])  # 打印前500字符检查

        soup = BeautifulSoup(response.text, 'html.parser')

        # 尝试查找所有表格，而不仅限于class="b"
        table = soup.find('table')
        if not table:
            print("未找到表格元素")
            return None

        rows = table.find_all('tr')[1:]  # 跳过表头
        print(f"找到{len(rows)}行数据")

        monthly_data = []
        for row in rows:
            cols = row.find_all('td')
            if len(cols) >= 4:
                try:
                    date = cols[0].get_text(strip=True)
                    weather = cols[1].get_text(strip=True).split('/')
                    weather_day = weather[0].strip()
                    weather_night = weather[1].strip() if len(weather) > 1 else ''

                    temp = cols[2].get_text(strip=True).replace('℃', '').split('/')
                    temp_high = temp[0].strip()
                    temp_low = temp[1].strip() if len(temp) > 1 else ''

                    wind = cols[3].get_text(strip=True).split('/')
                    wind_day = wind[0].strip()
                    wind_night = wind[1].strip() if len(wind) > 1 else ''

                    monthly_data.append({
                        '日期': date,
                        '白天天气': weather_day,
                        '夜晚天气': weather_night,
                        '最高温度': temp_high,
                        '最低温度': temp_low,
                        '白天风力': wind_day,
                        '夜晚风力': wind_night
                    })
                except Exception as e:
                    print(f"处理行时出错: {e}")
                    continue

        print(f"成功提取{len(monthly_data)}条数据")
        return monthly_data

    except Exception as e:
        print(f"获取{year_month}数据时出错: {e}")
        return None


def get_weather_data(start_year=2022, end_year=2024):
    """获取指定年份范围的天气数据"""
    all_data = []

    for year in range(start_year, end_year + 1):
        for month in range(1, 13):
            year_month = f"{year}{month:02d}"
            print(f"正在获取 {year}年{month}月 数据...")

            monthly_data = get_monthly_weather(year_month)
            if monthly_data:
                all_data.extend(monthly_data)

            time.sleep(2)  # 礼貌性延迟，避免被封

    # 转换为DataFrame并保存
    df = pd.DataFrame(all_data)

    # 保存为CSV
    os.makedirs('output', exist_ok=True)
    filename = f"output/大连天气_{start_year}-{end_year}.csv"
    df.to_csv(filename, index=False, encoding='utf_8_sig')
    print(f"数据已保存到 {filename}")

    return df


# 执行爬取
weather_df = get_weather_data(2022, 2024)