import requests
import pprint
import csv


# 设置请求参数
id = {1788067,1875298,1846715,1838877,2058614,2111662,2064020,1839782,1944892,1727859,1775972,2117019,1813276,1688383,2151752,2151595,1777615,1804038,1775908,1917369,2365486}
fw = open('专家.csv',mode='a',encoding='utf-8-sig',newline='')
csv_writer = csv.DictWriter(fw,fieldnames=[
    '名字',
    '彩龄',
    '文章数量',
    '大乐透一等奖次数',
    '大乐透二等奖次数',
    '大乐透三等奖次数'
])

csv_writer.writeheader()

url = 'https://i.cmzj.net/expert/queryExpertById'


headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0',
            'Referer':'https://www.cmzj.net/',
        }

for i in id:
    params = {
                'expertId':i                    
                }
    response = requests.get(url=url, params=params,headers=headers)

    response.encoding = 'utf-8'

    expert = response.json().get('data',{})

    pprint.pprint(expert)

    # 打印返回的 JSON 数据
    dit = {
            '名字':expert.get('name',''),
            '彩龄':expert.get('age',''),
            '文章数量':expert.get('articles',''),
            '大乐透一等奖次数':expert.get('dltOne',''),
            '大乐透二等奖次数':expert.get('dltTwo',''),
            '大乐透三等奖次数':expert.get('dltThree','')
            }
                
    csv_writer.writerow(dit)


