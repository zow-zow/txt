import subprocess  
  
# 输入流URL和对应的推流地址列表  
streams = [  
    {'input': 'http://124.225.108.170/hlslive-tx-cdn.ysp.cctv.cn/sx/2024078203.m3u8', 'output': 'rtmp://ali.push.yximgs.com/live/feicui'},  
    {'input': 'http://124.225.108.170/hlslive-tx-cdn.ysp.cctv.cn/sx/2024075403.m3u8', 'output': 'rtmp://ali.push.yximgs.com/live/viu'},  
    {'input': 'http://124.225.108.170/hlslive-tx-cdn.ysp.cctv.cn/sx/2024068503.m3u8', 'output': 'rtmp://ali.push.yximgs.com/live/yi'}, 
    # 添加更多输入流和对应的推流地址...  
]  
  
# 为每个输入流启动一个FFmpeg进程  
processes = []  
for stream in streams:  
    ffmpeg_command = [  
        'ffmpeg',  
        '-re',  
        #'-stream_loop', '-1',  # 如果输入流是循环的，请取消注释此行（注意：对于直播流，这通常不是必需的）  
        '-i', stream['input'],  
        '-bsf:a', 'aac_adtstoasc',  
        '-vcodec', 'copy',  # 如果需要转码，请更改此设置  
        '-acodec', 'copy',  # 如果需要转码，请更改此设置  
        '-f', 'flv',  
        '-y',  
        stream['output']  
    ]  
    try:  
        process = subprocess.Popen(ffmpeg_command, stderr=subprocess.PIPE)  
        processes.append(process)  
        print(f"Started streaming from {stream['input']} to {stream['output']}")  
    except Exception as e:  
        print(f"Failed to start streaming from {stream['input']} to {stream['output']}: {e}")  
  
# （可选）监控所有FFmpeg进程  
# ...（与之前的示例类似，但你可能需要根据实际情况进行调整）  
  
# 注意：这里没有包含监控进程的代码，因为那将取决于你的具体需求  
# 你可以使用类似之前示例中的循环和time.sleep()来监控进程  
# 或者，你可以使用更高级的进程管理库，如psutil  
  
# 如果需要停止所有进程，你可以遍历processes列表并调用terminate()方法  
# 但请注意，在实际应用中，你应该先尝试优雅地停止FFmpeg进程（如果可能的话）  
# 例如，通过发送一个特定的信号或命令给FFmpeg进程