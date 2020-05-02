from aip import AipSpeech
import subprocess
from playsound import playsound
APP_ID = '19693595'
API_KEY = 'zgnl35SISRuSCd6WKnSSGzcF'
SECRET_KEY = 'KeDaWswzDa532gV6iKSr2YVW9smYaXnD'
client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
result  = client.synthesis('百度', 'zh', 1, {  'vol': 5,'per':4})
# 识别正确返回语音二进制 错误则返回dict 参照下面错误码
if not isinstance(result, dict):
    with open('auido.mp3', 'wb') as f:
        f.write(result)
 
subprocess.call('mpv auido.mp3', shell=True)