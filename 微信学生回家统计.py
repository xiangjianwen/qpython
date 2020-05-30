import itchat
import time
import sys
import re
import os
import xlsxwriter,xlrd
from aip import AipSpeech
import subprocess
from itchat.content import *
from playsound import playsound
def rxlsx(xlsname):#读文件
    fname = xlsname+".xlsx"
    if not os.path.isfile(fname):
        print (u'文件路径不存在')
        sys.exit()
    data = xlrd.open_workbook(fname)            # 打开fname文件
    data.sheet_names()
    table = data.sheet_by_index(0)
    return table
def wxlsx(table,datastr,xlsname):#保存文件
                              # 获取xls文件中所有sheet的名称
                  # 通过索引获取xls文件第0个sheet
    nrows = table.nrows                         # 获取table工作表总行数
    ncols = table.ncols                         # 获取table工作表总列数
    workbook = xlsxwriter.Workbook(xlsname+".xlsx")  #创建一个excel文件
    worksheet = workbook.add_worksheet()        #创建一个工作表对象
    worksheet.set_column(0,ncols,22)            #设定列的宽度为22像素
    #border：边框，align:对齐方式，bg_color：背景颜色，font_size：字体大小，bold：字体加粗
    red = workbook.add_format({'border':1,'align':'center','bg_color':'red','font_size':12})
    for i in range(nrows):
        worksheet.set_row(i,22)                 #设定第i行单元格属性，高度为22像素，行索引从0开始
        for j in  range(ncols):
            cell_value = table.cell_value(i,j,) #获取第i行中第j列的值
            #print(cell_value)                   
            format = red
            worksheet.write(i,j,cell_value)      #把获取到的值写入文件对应的行列
            format.set_align('vcenter')                 #设置单元格垂直对齐
    
    for i in range(nrows):
    	cell1_value = table.cell_value(i,0) 
    	if datastr.find(cell1_value)!=-1:
    		worksheet.write(i,1,datastr,format)
    		print('g'+table.cell_value(i,1))
    workbook.close()
    return "succss"
print(rxlsx("99").col_values(1))


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
       #fobj.write(msg_time_rec+':'+res4.group(0)+'的消息:'+msg['ActualNickName']+'回复,'+msg['Content']+'\n')
       info=msg_time_rec+':'+res4.group(0)+'的消息:'+msg['ActualNickName']+'回复,'+msg['Content']
       wxlsx(rxlsx("99"),info,'99')
       if not isinstance(result, dict):
          with open('auido.mp3', 'wb') as f:
               f.write(result)
       subprocess.call('mpv auido.mp3', shell=True)
    else:
        print(msg+'出错了')
    fobj.close()


if __name__ == '__main__':
    itchat.auto_login(hotReload=True)
    itchat.run()
