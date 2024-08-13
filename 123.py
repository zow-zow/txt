import os
import re
import requests
import subprocess 

# 初始化变量和目录检查
id = "cscs"
if not os.path.isdir(f"./tscache/{id}/"):
    os.makedirs(f"./tscache/{id}/", exist_ok=True)

url = 'https://www.123iptv.tv/tw/tv/tvbfeicuitai.html'

# 定义一个函数来获取网页源码
def get_url_content(url):
    headers = {
        'cache-control': 'max-age=0',
        'sec-ch-ua': '"Chromium";v="123", "Not:A-Brand";v="8"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'sec-fetch-site': 'none',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'accept-language': 'zh-CN,zh;q=0.9,ja;q=0.8,ko;q=0.7',
        'priority': 'u=0, i',
    }
    response = requests.get(url, headers=headers)
    return response.text

html = get_url_content(url)
# print(html)

pattern = re.compile(r'play-line2.*?url="([^"]+)"')
matches = pattern.findall(html)
url = matches[0]
# print(url)

buri = "https://www.123iptv.tv"
one_url = buri + url
# print(one_url)

new_html = get_url_content(one_url)
# print(new_html)

pattern = re.compile(r'url=([^\']+)')
matches = pattern.findall(new_html)
liveurl = matches[0]
#print(liveurl)



 
  
# 定义FFmpeg命令  
ffmpeg_command = [  
    'ffmpeg',  
    '-re',  
    '-stream_loop', '-1',  
    '-i', liveurl,  # 替换为你的输入流URL  
    '-bsf:a', 'aac_adtstoasc',  
    '-vcodec', 'copy',  
    '-acodec', 'copy',  
    '-f', 'flv',  
    '-y',  
    '-reconnect', '1',  
    '-reconnect_at_eof', '1',  
    '-reconnect_streamed', '1',  
    'rtmp://ali.push.yximgs.com/live/feicui'  # 替换为你的推流服务器地址  
]  
  
# 使用subprocess启动FFmpeg进程  
try:  
    process = subprocess.Popen(ffmpeg_command, stderr=subprocess.PIPE)  
    # 你可以在这里添加代码来监控FFmpeg进程的输出或错误  
    # 例如，读取stderr来查看FFmpeg的日志输出  
    while True:  
        line = process.stderr.readline().decode('utf-8').strip()  
        if not line:  
            break  
        print(line)  
    process.wait()  # 等待FFmpeg进程结束  
except Exception as e:  
    print(f"An error occurred: {e}")
