import subprocess
import os
import signal
audiopath ="auido.mp3"
subprocess.call('play-audio '+audiopath, shell=True)
#p = subprocess.Popen('play-audio auido.mp3' ,close_fds=True, stdout=subprocess.PIPE,preexec_fn=os.setsid, shell=True)      # 播放不影响其他代码操作
#os.killpg(p.pid,signal.SIGUSR1)  # 关闭
subprocess.call('mpv '+audiopath, shell=True)