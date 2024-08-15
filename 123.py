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

def get_video_urls(channel):
    try:
        channel_name = channel.find('a').text.strip()  # 获取频道名
        channel_url = channel.find('a')['href']  # 获取频道链接
        response = requests.get(channel_url, headers=headers)
        pattern = re.compile(r'videoUrl: "(.*?)"', re.S)
        video_urls = re.findall(pattern, response.text)
        results = []
        if video_urls:
            for video_url in video_urls:
                results.append(f"{channel_name},{video_url}")
        return results
    except Exception as e:
        return [f"处理频道时出错: {e}"]

response = requests.get('http://freegat.us.kg/', headers=headers)

if response.status_code == 200:
    html_content = response.text

print(html_content)
