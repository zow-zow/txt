import subprocess  
  
# 定义FFmpeg命令  
ffmpeg_command = [  
    'ffmpeg',  
    '-re',  
    '-stream_loop', '-1',  
    '-i', 'https://stream1.freetv.fun/a17566b81efbc7de0bd335ce7dd6083a3150c80a02c0f2d8a6d2d7525435f600.m3u8',  # 替换为你的输入流URL  
    '-bsf:a', 'aac_adtstoasc',  
    '-vcodec', 'copy',  
    '-acodec', 'copy',  
    '-f', 'flv',  
    '-y',  
    '-reconnect', '1',  
    '-reconnect_at_eof', '1',  
    '-reconnect_streamed', '1',  
    'rtmp://ali.push.yximgs.com/live/woshimimi_liu_liang_duo_dao_yong_bu_wan_tui_zhe_wan'  # 替换为你的推流服务器地址  
]  #播放地址http://ali.hlspull.yximgs.com/live/woshimimi_liu_liang_duo_dao_yong_bu_wan_tui_zhe_wan.flv
  
# 使用subprocess启动FFmpeg进程  
try:  
    process = subprocess.Popen(ffmpeg_command, stderr=subprocess.PIPE)  
    # 你可以在这里添加代码来监控FFmpeg进程的输出或错误  
    # 例如，读取stderr来查看FFmpeg的日志输出  
    while True:  
        line = process.stderr.readline().decode('utf-8').strip()  
        if not line:  
            break  
        print(line)  
    process.wait()  # 等待FFmpeg进程结束  
except Exception as e:  
    print(f"An error occurred: {e}")
