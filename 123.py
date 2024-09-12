import requests

# 定义请求的URL
url = 'http://192.210.231.23:7878/api.php?act=live&app=10000'

# 定义请求头
headers = {
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'User-Agent': 'okhttp/3.12.11',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Content-Length': '50',  # 这个头部通常不需要手动设置，requests会自动计算
    'Host': '192.210.231.23:7878',
    'Connection': 'Keep-Alive',
    'Accept-Encoding': 'gzip'
}

# 定义请求体
data = {
    't': '1726105348',
    'sign': '17e7c0fedf564d7efb072ddee385dc84'
}

# 尝试发送POST请求
try:
    response = requests.post(url, headers=headers, data=data)
    # 去掉响应数据中的空格和换行符
    cleaned_response_text = response.text.strip()
    # 打印响应状态码
    print(f"Status Code: {response.status_code}")
    
    # 打印响应内容
    print("Response Content:")
    print(cleaned_response_text)
    with open('aiyudata.txt', 'w', encoding='utf-8') as f:
        f.write(cleaned_response_text)
except requests.exceptions.RequestException as e:
    # 打印错误信息
    print("An error occurred while trying to send the request:")
    print(e)
