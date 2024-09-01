import requests
import re
import time
import concurrent.futures
import json

# 定义初始URL列表
urls = ['https://www.zoomeye.org/api/search?q=udpxy+%2Bsubdivisions%3A%22湖南%22+%2Bcity%3A长沙&page=1&t=v4%2Bv6%2Bweb', 
        'https://www.zoomeye.org/api/search?q=udpxy+%2Bsubdivisions%3A%22湖南%22+%2Bcity%3A衡阳&page=1&t=v4%2Bv6%2Bweb',
        'https://www.zoomeye.org/api/search?q=udpxy+%2Bsubdivisions%3A%22湖南%22+%2Bcity%3A怀化&page=1&t=v4%2Bv6%2Bweb',
        'https://www.zoomeye.org/api/search?q=udpxy+%2Bsubdivisions%3A%22湖南%22+%2Bcity%3A岳阳&page=1&t=v4%2Bv6%2Bweb',
        'https://www.zoomeye.org/api/search?q=udpxy+%2Bsubdivisions%3A%22湖南%22+%2Bcity%3A株洲&page=1&t=v4%2Bv6%2Bweb',


    ]  # 添加更多URL

html_contents = []  # 用于存储获取到的HTML源码


# 发送GET请求，获取HTML源代码
def get_html_content(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()  # 返回JSON格式的内容
    return {}  # 如果请求失败返回空字典

# 使用并发处理来同时发送多个GET请求
with concurrent.futures.ThreadPoolExecutor() as executor:
    # 执行并发的GET请求，并获取HTML源码
    html_contents = list(executor.map(get_html_content, urls))

# 提取ip和port，组合成URL加入到usable_urls中
found_urls = []
for content in html_contents:
    if 'matches' in content:
        for match in content['matches']:
            ip = match['ip']
            port = match['portinfo']['port']
            url = f"http://{ip}:{port}"
            found_urls.append(url)

# 打印提取到的URL
for url in found_urls:
    print(f"提取到的URL: {url}")

    
usable_urls = []
for original_url in found_urls:
    test_url = original_url + '/status'
    try:
        test_response = requests.get(test_url, timeout=2)
        if test_response.status_code == 200:
            print(f"可用URL: {original_url}")
            usable_urls.append(original_url)
    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")
    # 使用集合来存储提取到的URL，以确保不重复
found_urls_set = set()
for original_url in usable_urls:
        for suffix in ['/udp/239.76.245.23:1234','/udp/239.76.245.204:1234','/udp/239.76.245.209:1234','/udp/239.76.245.179:1234','/udp/239.76.245.180:1234','/udp/239.76.245.181:1234','/udp/239.76.245.235:1234','/udp/239.76.246.8:1234','/udp/239.76.246.7:1234','/udp/239.76.246.103:1234','/udp/239.76.246.102:1234','/udp/239.76.246.104:1234','/udp/239.76.246.105:1234','/udp/239.76.252.119:9000','/udp/239.76.246.109:1234','/udp/239.76.246.108:1234','/udp/239.76.246.107:1234','/udp/239.76.246.110:1234','/udp/239.76.246.122:1234','/udp/239.76.246.121:1234','/udp/239.76.248.6:1234','/udp/239.76.248.10:1234','/udp/239.76.248.11:1234','/udp/239.76.248.13:1234','/udp/239.76.248.14:1234','/udp/239.76.248.18:1234','/udp/239.76.248.19:1234','/udp/239.76.252.234:9000','/udp/239.76.248.20:1234','/udp/239.76.248.21:1234','/udp/239.76.248.23:1234','/udp/239.76.248.57:1234','/udp/239.76.255.12:9000',]:
            new_url = original_url + suffix
            found_urls_set.add(new_url)

    # 将集合转换为列表，以便后续处理
urls = list(found_urls_set)


def measure_download_speed(url, name, duration=10):
    try:
        print(f"开始测量下载速度：{url}")
        start_time = time.time()
        response = requests.get(url, stream=True, timeout=3)  # 设置超时时间

        total_downloaded = 0  # total downloaded data in bytes
        for data in response.iter_content(1024*1024):  # read 1MB at a time
            if time.time() - start_time > duration:
                break
            total_downloaded += len(data)

        elapsed_time = time.time() - start_time
        speed = total_downloaded / elapsed_time / 1024 / 1024  # speed in MB/s
        return name, url, speed  # 返回name和url
    except (requests.exceptions.RequestException, ConnectionError) as e:
        print(f"Failed to download {url}: {e}")
        return url, 0.0


def main():
    print("开始处理URL和测量下载速度")
    formatted_names = {}  # 使用字典来存储每个URL对应的名称
    for original_url in urls:
        print(f"正在处理URL: {original_url}")
        if '/udp/111.111.111.111:111' in original_url:
            formatted_names[original_url] = "模板"
        elif '/udp/239.76.245.23:1234' in original_url:
            formatted_names[original_url] = "长沙女姓"
        elif '/udp/239.76.245.204:1234' in original_url:
            formatted_names[original_url] = "长沙影视"
        elif '/udp/239.76.245.209:1234' in original_url:
            formatted_names[original_url] = "湘西综合"
        elif '/udp/239.76.245.179:1234' in original_url:
            formatted_names[original_url] = "河南梨园"
        elif '/udp/239.76.245.180:1234' in original_url:
            formatted_names[original_url] = "文物宝库"
        elif '/udp/239.76.245.181:1234' in original_url:
            formatted_names[original_url] = "武术世界"
        elif '/udp/239.76.245.235:1234' in original_url:
            formatted_names[original_url] = "张家界2"
        elif '/udp/239.76.246.8:1234' in original_url:
            formatted_names[original_url] = "凤凰资讯"
        elif '/udp/239.76.246.7:1234' in original_url:
            formatted_names[original_url] = "凤凰中文"
        elif '/udp/239.76.246.103:1234' in original_url:
            formatted_names[original_url] = "湖南经视"
        elif '/udp/239.76.246.102:1234' in original_url:
            formatted_names[original_url] = "湖南国际"
        elif '/udp/239.76.246.104:1234' in original_url:
            formatted_names[original_url] = "湖南都市"
        elif '/udp/239.76.246.105:1234' in original_url:
            formatted_names[original_url] = "湖南娱乐"
        elif '/udp/239.76.252.119:9000' in original_url:
            formatted_names[original_url] = "湖南电影"
        elif '/udp/239.76.246.109:1234' in original_url:
            formatted_names[original_url] = "湖南公共"
        elif '/udp/239.76.246.108:1234' in original_url:
            formatted_names[original_url] = "湖南电视剧"
        elif '/udp/239.76.246.107:1234' in original_url:
            formatted_names[original_url] = "金鹰卡通"
        elif '/udp/239.76.246.110:1234' in original_url:
            formatted_names[original_url] = "金鹰纪实"
        elif '/udp/239.76.246.122:1234' in original_url:
            formatted_names[original_url] = "长沙政法"
        elif '/udp/239.76.246.121:1234' in original_url:
            formatted_names[original_url] = "长沙新闻"
        elif '/udp/239.76.248.6:1234' in original_url:
            formatted_names[original_url] = "浏阳"
        elif '/udp/239.76.248.10:1234' in original_url:
            formatted_names[original_url] = "常德综合"
        elif '/udp/239.76.248.11:1234' in original_url:
            formatted_names[original_url] = "常德公共"
        elif '/udp/239.76.248.13:1234' in original_url:
            formatted_names[original_url] = "衡阳综合"
        elif '/udp/239.76.248.14:1234' in original_url:
            formatted_names[original_url] = "衡阳公共"
        elif '/udp/239.76.248.18:1234' in original_url:
            formatted_names[original_url] = "娄底综合"
        elif '/udp/239.76.248.19:1234' in original_url:
            formatted_names[original_url] = "娄底公共"
        elif '/udp/239.76.252.234:9000' in original_url:
            formatted_names[original_url] = "张家界综合"
        elif '/udp/239.76.248.20:1234' in original_url:
            formatted_names[original_url] = "LDETV"
        elif '/udp/239.76.248.21:1234' in original_url:
            formatted_names[original_url] = "XNXTV"
        elif '/udp/239.76.248.23:1234' in original_url:
            formatted_names[original_url] = "邵阳新闻"
        elif '/udp/239.76.248.57:1234' in original_url:
            formatted_names[original_url] = "永州新闻"
        elif '/udp/239.76.255.12:9000' in original_url:
            formatted_names[original_url] = "怀化综合"








    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = list(executor.map(lambda url: measure_download_speed(url, formatted_names.get(url, "Unknown")), urls))

    unique_urls = set()  # 存储唯一的URL
    for result in results:
        if len(result) >= 3 and result[2] > 0:  # 检查result的长度是否至少为3
          unique_urls.add(result[0])  # 将结果按相同的 result[0] 进行存储

    # 将结果按相同的 result[0] 进行排序
    sorted_results = sorted(results, key=lambda x: x[0])

    # 在插入内容前添加标签
    with open("cs.txt", "w") as file:
        file.write("\n#湖南,#genre#\n")
        
    # 输出结果到文件 ztv.txt
    with open("cs.txt", "a") as file:
        for result in sorted_results:
            if len(result) >= 3 and result[2] > 0:  # 同样在这里检查
                file.write(f"{result[0]},{result[1]} -- {result[2]:.2f} MB/s\n")
    print("处理完成，结果已写入 cs.txt 文件")
if __name__ == "__main__":
    main()
