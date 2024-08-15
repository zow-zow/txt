import requests
import re

# 定义电视频道映射
n = {
    '1': 'tv-show-20052-3',  # 翡翠台
    '2': 'tv-show-20058-3',  # 明珠台
    '3': 'tv-show-20053-2',  # 无线新闻

    '55': 'tv-show-20086-1',  # 东森综合台
    '56': 'tv-show-20087-1',  # 东森超视

    '74': 'tv-show-20105-1',  # 壹新闻

    '76': 'tv-show-20107-1',  # 年代新闻

}

def get_liveurl(id):
    url = f'https://www.xhzb.tw/{n[id]}.html'
    response = requests.get(url)
    response.encoding = 'utf-8'
    html_content = response.text
    
    match = re.search(r'<input name="ps" id="ps" type="hidden" value="([^"]+)">', html_content)
    if match:
        psValue = match.group(1)
        post_url = 'https://www.xhzb.tw/get_video.php'
        post_data = {'vu': psValue}
        headers = {
            'Host': 'www.xhzb.tw',
            'Content-Length': '59',
            'sec-ch-ua': '"Chromium";v="123", "Not:A-Brand";v="8"',
            'content-type': 'application/x-www-form-urlencoded',
            'x-requested-with': 'XMLHttpRequest',
            'sec-ch-ua-mobile': '?0',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
            'sec-ch-ua-platform': '"Windows"',
            'origin': 'https://www.xhzb.tw',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': url,
        }
        response = requests.post(post_url, data=post_data, headers=headers)
        response.encoding = 'utf-8'
        match = re.search(r'video-url="([^"]+)', response.text)
        if match:
            liveurl = match.group(1)
            print(f'{id} {liveurl}')
            return f'{liveurl},rtmp://ali.push.yximgs.com/live/ttt80182503722594288llltw{id}'
    return None

def process_channel(id):
    result = get_liveurl(id)

    if result:
        return result

if __name__ == "__main__":
    results = []
    for id in n:
        result = process_channel(id)
        if result:
            results.append(result)

    for result in results:
        print(result)
