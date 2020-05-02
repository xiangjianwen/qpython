import itchat
import time
import re
from aip import AipSpeech
import subprocess
from playsound import playsound
APP_ID = '19693595'
API_KEY = 'zgnl35SISRuSCd6WKnSSGzcF'
SECRET_KEY = 'KeDaWswzDa532gV6iKSr2YVW9smYaXnD'
client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
@itchat.msg_register(itchat.content.TEXT, isGroupChat=True)

def reply_msg(msg):
    res2 = re.search(r"(?<=NickName).*?HeadImgUrl", str(msg))
    res3 = re.search(r"(?<=NickName)(?!.*?NickName).*?HeadImgUrl", res2.group(0))
    res4 = re.search(r"[\u4e00-\u9fa5]+",res3.group(0))
    #print(msg)
    print("收到一条群信息：",res4.group(0)+','+msg['ActualNickName'], msg['Content'])
    result  = client.synthesis('来自微信群,'+res4.group(0)+'的消息:'+msg['ActualNickName']+'回复,'+msg['Content'], 'zh', 1, {  'vol': 5,'per':4})
    # 识别正确返回语音二进制 错误则返回dict 参照下面错误码
    if not isinstance(result, dict):
        with open('auido.mp3', 'wb') as f:
             f.write(result)
 
    subprocess.call('mpv auido.mp3', shell=True)
def after_login():
    # 获得完整的群聊列表
    print("完整的群聊列表如下：")
    print(itchat.get_chatrooms())
    # 查找特定群聊
    time.sleep(10)
    # 通过群聊名查找
    chat_rooms = itchat.search_chatrooms(name='我的1')
    if len(chat_rooms) > 0:
        itchat.send_msg('测试', chat_rooms[0]['UserName'])


if __name__ == '__main__':
    itchat.auto_login(hotReload=True)
    itchat.run()
