import requests
import re
from concurrent.futures import ThreadPoolExecutor

# 定义电视频道映射
n = {
    '1': 'tv-show-20052-3',  # 翡翠台
    '2': 'tv-show-20058-3',  # 明珠台
    '3': 'tv-show-20053-2',  # 无线新闻
    '4': 'tv-show-20076-1',  # HOY资讯台
    '5': 'tv-show-20054-3',  # 星河台
    '6': 'tv-show-20073-2',  # ViuTV
    '7': 'tv-show-20057-3.',  # 无线财经
    '8': 'tv-show-20059-1',  # hk31
    '9': 'tv-show-20060-2',  # hk32
    '10': 'tv-show-20062-2',  # 凤凰资讯
    '11': 'tv-show-20063-1',  # 凤凰中文
    '12': 'tv-show-20064-2',  # 凤凰香港
    '13': 'tv-show-20070-2',  # 天映频道
    '14': 'tv-show-20071-2',  # 天映经典
    '15': 'tv-show-20066-1',  # Now Sports
    '16': 'tv-show-20067-1',  # Now 新闻台
    '17': 'tv-show-20065-1',  # Now 华剧台
    '18': 'tv-show-20055-1',  # 娱乐新闻台
    '19': 'tv-show-20072-2',  # TVB PLUS
    '20': 'tv-show-20075-1',  # HOY
    '21': 'tv-show-20074-3',  # ViuTVsix
    '50': 'tv-show-20081-1',  # 中天综合台
    '51': 'tv-show-20082-1',  # 中天亚洲台
    '52': 'tv-show-20083-1',  # 纬来日本
    '53': 'tv-show-20084-1',  # 纬来综合台
    '54': 'tv-show-20085-1',  # TVBS Asia
    '55': 'tv-show-20086-1',  # 东森综合台
    '56': 'tv-show-20087-1',  # 东森超视
    '57': 'tv-show-20088-1',  # 台视
    '58': 'tv-show-20089-1',  # 八大综合台
    '59': 'tv-show-20090-1',  # 八大第一台
    '60': 'tv-show-20091-1',  # 中视
    '61': 'tv-show-20092-1',  # 华视
    '62': 'tv-show-20093-1',  # ELTA 综合
    '63': 'tv-show-20094-1',  # 客家电视台
    '64': 'tv-show-20095-1',  # 公视3台
    '65': 'tv-show-20096-1',  # 公视
    '66': 'tv-show-20097-1',  # 靖天国际台
    '67': 'tv-show-20098-1',  # 大爱一台
    '68': 'tv-show-20099-1',  # 大爱二台
    '69': 'tv-show-20100-2',  # 中天新闻
    '70': 'tv-show-20101-1',  # TVBS
    '71': 'tv-show-20102-1',  # TVBS 新闻台
    '72': 'tv-show-20103-1',  # 东森新闻
    '73': 'tv-show-20104-1',  # 东森财经新闻
    '74': 'tv-show-20105-1',  # 壹新闻
    '75': 'tv-show-20106-1',  # 中视新闻
    '76': 'tv-show-20107-1',  # 年代新闻
    '77': 'tv-show-20108-1',  # 寰宇新闻台
    '78': 'tv-show-20109-1',  # 台视新闻
    '79': 'tv-show-20110-1',  # 非凡新闻
    '80': 'tv-show-20111-1',  # 华视新闻
    '81': 'tv-show-20112-1',  # 镜新闻
    '82': 'tv-show-20113-1',  # 靖天资讯台
    '83': 'tv-show-20114-1',  # 星卫电影台
    '84': 'tv-show-20115-1',  # 纬来电影台
    '85': 'tv-show-20116-1',  # 纬来戏剧台
    '86': 'tv-show-20117-1',  # 东森电影
    '87': 'tv-show-20118-1',  # 东森洋片
    '88': 'tv-show-20119-1',  # 东森戏剧
    '89': 'tv-show-20120-1',  # 卫视电影台
    '90': 'tv-show-20121-1',  # 星卫娱乐台
    '91': 'tv-show-20122-1',  # 卫视中文台
    '92': 'tv-show-20123-1',  # 龙华电影台
    '93': 'tv-show-20124-1',  # 龙华洋片台
    '94': 'tv-show-20125-1',  # 好莱坞电影台
    '95': 'tv-show-20126-1',  # TVBS 欢乐台
    '96': 'tv-show-20127-1',  # ELTA 影剧
    '97': 'tv-show-20128-1',  # 龙祥电影台
    '98': 'tv-show-20129-1',  # EYE 戏剧台
    '99': 'tv-show-20130-1',  # 八大戏剧台
    '100': 'tv-show-20131-1',  # 八大娱乐台
    '101': 'tv-show-20132-1',  # MTV Live
    '102': 'tv-show-20133-1',  # 靖天电影台
    '103': 'tv-show-20134-1',  # 中天娱乐台
    '104': 'tv-show-20135-1',  # 靖洋戏剧台
    '105': 'tv-show-20136-1',  # 美亚电影台
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
    with ThreadPoolExecutor(max_workers=10) as executor:  # 可以调整 max_workers 来控制线程数
        futures = [executor.submit(process_channel, id) for id in n]
        for future in futures:
            result = future.result()
            if result:
                results.append(result)

    for result in results:
        print(result)
