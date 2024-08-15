import requests

url = "http://freegat.us.kg/"

response = requests.get(url)
print(response.text)
if response.status_code == 200:
    content = response.text
    # 将内容写入到txt文件
    with open("output22.txt", "w", encoding="utf-8") as file:
        file.write(content)
        print("内容已写入到output.txt文件中")
else:
    print("Failed to retrieve content from the URL")
