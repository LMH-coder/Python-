import requests
import pprint
import csv


# 设置请求参数

fw = open('大乐透第四页.csv',mode='a',encoding='utf-8-sig',newline='')
csv_writer = csv.DictWriter(fw,fieldnames=[
    '期号',
    '开奖日期',
    '前区号码',
    '后区号码',
    '销售额',
    '星期几'
])

csv_writer.writeheader()

url = 'https://jc.zhcw.com/port/client_json.php'

params = {
        'transactionType': '10001001',
        'lotteryId': '281',
        'issueCount': '100',
        'startIssue': '',
        'endIssue': '',
        'startDate': '',
        'endDate': '',
        'type': '0',
        'pageNum': '4',
        'pageSize': '30',
        }

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0',
    'Referer':'https://www.zhcw.com/',
    'Cookie':'Hm_lvt_692bd5f9c07d3ebd0063062fb0d7622f=1751435567,1751524080,1751534716,1751866166; Hm_lpvt_692bd5f9c07d3ebd0063062fb0d7622f=1751866166; HMACCOUNT=592316AB2CD92AF8; PHPSESSID=kta4ulv9pttghj3l966vq22un6; _ga_9FDP3NWFMS=GS2.1.s1751866166$o10$g0$t1751866166$j60$l0$h0; Hm_lvt_12e4883fd1649d006e3ae22a39f97330=1751435572,1751524080,1751534717,1751866167; Hm_lpvt_12e4883fd1649d006e3ae22a39f97330=1751866167; _ga=GA1.2.618448768.1751435570; _gid=GA1.2.746003422.1751866167'
}


# 发送 GET 请求
response = requests.get(url=url, params=params,headers=headers)

response.encoding = 'utf-8'

result = response.json()['data']

# 打印返回的 JSON 数据
for index in result:
    dit = {
        '期号':index['issue'],
        '开奖日期':index['openTime'],
        '前区号码':index['frontWinningNum'],
        '后区号码':index['backWinningNum'],
        '销售额':index['saleMoney'],
        '星期几':index['week']
    }
    pprint.pprint(dit)

    csv_writer.writerow(dit)


