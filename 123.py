import subprocess
import threading

# 定义一个函数来启动FFmpeg进程
def start_ffmpeg(input_url, output_url):
    ffmpeg_command = [
        'ffmpeg',
        '-re',
        '-stream_loop', '-1',
        '-user_agent', 'okhttp/4.12.0',  # 设置User-Agent
        '-i', input_url,
        '-c:v', 'libx264',  # 使用libx264编解码器
        '-preset', 'veryfast',  # 可以调整压缩速度和质量
        '-c:a', 'aac',  # 明确设置AAC音频编解码器
        '-b:a', '128k',  # 设置音频比特率
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
    ('http://success.success52592.online/61fd7113def5e604643efccde83c2b08/38c2dce17fcac06647c991ba83cf682cb95cd399ec40cbe2967294d048d7df80/5aff1bcab410e069b92a56e0123fe342/index.m3u8', 'rtmp://ali.push.yximgs.com/live/cs1'),
#    ('https://ali-m-l.cztv.com/channels/lantian/channel010/1080p.m3u8', 'rtmp://ali.push.yximgs.com/live/cs2'),
 #   ('https://ali-m-l.cztv.com/channels/lantian/channel008/1080p.m3u8', 'rtmp://ali.push.yximgs.com/live/cs3'),
#    ('https://ali-m-l.cztv.com/channels/lantian/channel004/1080p.m3u8', 'rtmp://ali.push.yximgs.com/live/cs4'),
 #   ('https://ali-m-l.cztv.com/channels/lantian/channel012/1080p.m3u8', 'rtmp://ali.push.yximgs.com/live/cs5'),
 #   ('https://ali-m-l.cztv.com/channels/lantian/channel006/1080p.m3u8', 'rtmp://ali.push.yximgs.com/live/cs6'),
#    ('https://ali-m-l.cztv.com/channels/lantian/channel003/1080p.m3u8', 'rtmp://ali.push.yximgs.com/live/cs7'),
#    ('https://ali-m-l.cztv.com/channels/lantian/channel002/1080p.m3u8', 'rtmp://ali.push.yximgs.com/live/cs8'),

]     #播放地址 http://ali.hlspull.yximgs.com/live/cs1.flv

# 为每个流启动一个独立的线程来推流
threads = []
for input_url, output_url in streams:
    thread = threading.Thread(target=start_ffmpeg, args=(input_url, output_url))
    thread.start()
    threads.append(thread)

# 等待所有线程结束
for thread in threads:
    thread.join()
