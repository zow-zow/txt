import os
import requests

url = "http://freegat.us.kg/"
response = requests.get(url)
print(response.text)

if response.status_code == 200:
    content = response.text
    # Get the path to the repository
    repo_path = os.getenv('GITHUB_WORKSPACE')
    # Create the full path to the file
    file_path = os.path.join(repo_path, "output22.txt")
    # Write the content to the file
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(content)
        print("内容已写入到output.txt文件中")
else:
    print("Failed to retrieve content from the URL")
