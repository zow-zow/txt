import subprocess
import threading
import requests

# 定义一个函数来启动FFmpeg进程
def start_ffmpeg(input_url, output_url):
    ffmpeg_command = [
        'ffmpeg',
        '-re',
        '-stream_loop', '-1',
        '-i', input_url,
        '-bsf:a', 'aac_adtstoasc',
        '-vcodec', 'copy',
        '-acodec', 'copy',
        '-f', 'flv',
        '-y',
        '-reconnect', '1',
        '-reconnect_at_eof', '1',
        '-reconnect_streamed', '1',
        output_url
    ]

    try:
        process = subprocess.Popen(ffmpeg_command, stderr=subprocess.PIPE)
        while True:
            line = process.stderr.readline().decode('utf-8').strip()
            if not line:
                break
            print(line)
        process.wait()
    except Exception as e:
        print(f"An error occurred while streaming {input_url}: {e}")

# 从指定URL读取输入流和推流地址
def get_streams(url):
    response = requests.get(url)
    lines = response.text.strip().splitlines()
    streams = []
    for line in lines:
        input_url, output_url = line.split(',')
        streams.append((input_url.strip(), output_url.strip()))
    return streams

# 获取流地址
url = 'http://8.138.87.43:2020/源/tl.txt'
streams = get_streams(url)

# 为每个流启动一个独立的线程来推流
threads = []
for input_url, output_url in streams:
    thread = threading.Thread(target=start_ffmpeg, args=(input_url, output_url))
    thread.start()
    threads.append(thread)

# 等待所有线程结束
for thread in threads:
    thread.join()
