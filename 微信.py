import itchat
import time
import sys
import re
from aip import AipSpeech
import subprocess
from itchat.content import *
from playsound import playsound
APP_ID = '19693595'
API_KEY = 'zgnl35SISRuSCd6WKnSSGzcF'
SECRET_KEY = 'KeDaWswzDa532gV6iKSr2YVW9smYaXnD'
client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
# 好友信息监听
@itchat.msg_register([TEXT, PICTURE, RECORDING, ATTACHMENT, VIDEO], isFriendChat=True)
def handle_friend_msg(msg):
    msg_id = msg['MsgId']
    msg_from_user = msg['User']['NickName']
    msg_content = msg['Content']
    print(msg_from_user+msg_content)
@itchat.msg_register(itchat.content.TEXT, isGroupChat=True)
def reply_msg(msg):
    fobj=open('/storage/emulated/0/微信群聊记录.txt','a')
    res2 = re.search(r"(?<=NickName).*?HeadImgUrl", str(msg))
    if res2:
       res3 = re.search(r"(?<=NickName':)(?!.*?NickName).*?HeadImgUrl", res2.group(0))
       res4 = re.search(r".*?(?=,)",res3.group(0))
       #print(msg)
       # 收到信息的时间
       msg_time_rec = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
       msg_create_time = msg['CreateTime']
       print("收到一条群信息：",msg_time_rec+':'+res4.group(0)+','+msg['ActualNickName'], msg['Content'])
       result  = client.synthesis('来自微信群,'+res4.group(0)+'的消息:'+msg['ActualNickName']+'回复,'+msg['Content'], 'zh', 1, {  'vol': 10,'per':4})
       # 识别正确返回语音二进制 错误则返回dict 参照下面错误码
       fobj.write(msg_time_rec+':'+res4.group(0)+'的消息:'+msg['ActualNickName']+'回复,'+msg['Content']+'\n')
       if not isinstance(result, dict):
          with open('auido.mp3', 'wb') as f:
               f.write(result)
       subprocess.call('mpv auido.mp3', shell=True)
    else:
        print(msg+'出错了')
    fobj.close()
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
