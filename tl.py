import subprocess
import threading

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
        # 读取并打印FFmpeg进程的输出
        while True:
            line = process.stderr.readline().decode('utf-8').strip()
            if not line:
                break
            print(line)
        process.wait()
    except Exception as e:
        print(f"An error occurred while streaming {input_url}: {e}")

# 输入流和对应的推流地址
streams = [
    ('http://95.179.139.113:5566/4gtv/1', 'rtmp://ali.push.yximgs.com/live/cs1'),
    ('http://95.179.139.113:5566/4gtv/2', 'rtmp://ali.push.yximgs.com/live/cs2'),
    ('http://95.179.139.113:5566/4gtv/4', 'rtmp://ali.push.yximgs.com/live/cs3'),
    ('http://95.179.139.113:5566/4gtv/6', 'rtmp://ali.push.yximgs.com/live/cs4'),
    ('http://95.179.139.113:5566/4gtv/7', 'rtmp://ali.push.yximgs.com/live/cs5'),  
    ('http://95.179.139.113:5566/4gtv/8', 'rtmp://ali.push.yximgs.com/live/cs6')
]

# 为每个流启动一个独立的线程来推流
threads = []
for input_url, output_url in streams:
    thread = threading.Thread(target=start_ffmpeg, args=(input_url, output_url))
    thread.start()
    threads.append(thread)

# 等待所有线程结束
for thread in threads:
    thread.join()
