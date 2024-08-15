import requests

# 使用requests库获取www.baidu.com的网页内容
response = requests.get('https://zow-zow.github.io/3ZTV/')

# 检查请求是否成功
if response.status_code == 200:
    print('请求成功')
    # 打印网页内容
    print(response.text)
else:
    print('请求失败')
