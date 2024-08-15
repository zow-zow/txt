from bs4 import BeautifulSoup
import requests
import re
import concurrent.futures

# 设置请求头
headers = {
    'Host': 'freegat.us.kg',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36 XiaoBai1/10.4.5312.1827 (XBCEF)',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-TW;q=0.6',
    'Cookie': 'PHPSESSID=65s16sjaus4iag4amk00onk3d3',
    'Proxy-Connection': 'keep-alive'
}
response = requests.get('http://freegat.us.kg/', headers=headers)
print(response.text)

with open('output1111.txt', 'w', encoding='utf-8') as file:
    file.write(response.text)
