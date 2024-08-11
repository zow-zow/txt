import subprocess
import threading
import requests
import time

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

# 启动推流线程
def start_streaming_threads(streams):
    threads = []
    for input_url, output_url in streams:
        thread = threading.Thread(target=start_ffmpeg, args=(input_url, output_url))
        thread.start()
        threads.append(thread)
    return threads

# 停止所有正在运行的推流
def stop_streaming_threads(threads):
    for thread in threads:
        if thread.is_alive():
            # 强制停止线程并杀死FFmpeg进程
            # 这里可以加入线程和进程的停止逻辑
            pass

# 主循环：定期更新推流地址
def main(url, interval):
    current_threads = []
    while True:
        # 读取流地址
        streams = get_streams(url)

        # 停止当前的推流线程
        stop_streaming_threads(current_threads)

        # 启动新的推流线程
        current_threads = start_streaming_threads(streams)

        # 等待一段时间后重新读取和更新流地址
        time.sleep(interval)

# 设置URL和重新读取间隔时间（秒）
url = 'http://8.138.87.43:2020/源/tl.txt'
interval = 120  # 每隔5分钟重新读取一次

# 启动主循环
main(url, interval)
