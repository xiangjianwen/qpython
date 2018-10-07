# -*- coding: utf-8 -*-


import requests
import time
import http.cookiejar
import re
import xlrd
import sys
import os
import time
# 模拟浏览器访问
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.109 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded',
    'X-Requested-With': 'XMLHttpRequest'
}
#home_url = "https://hfsjs.yunxiao.com/v1/overview/focus-students?classId=000000000000000180057039&subjects=%E6%95%B0%E5%AD%A6"
#base_login = "https://hfsjs.yunxiao.com/v1/auth/login"  # 一定不能写成http,否则无法登录

def rxlsx(xlsname):#读文件
    fname = xlsname+".xls"
    if not os.path.isfile(fname):
        print (u'不存在')
        sys.exit()
    data = xlrd.open_workbook(fname)            # 打开fname文件
    data.sheet_names()
    table = data.sheet_by_index(0)
    return table


def teacherPj(): #教师序号，教师账号文件   
    
    
    
    #studentId=numTOstudentId(i,table)#转换学籍号
    #c=getcookie(acount,"123456",headers)#获取登陆cookie
    url = "http://www.srjyyun.com/ModuleVote/SearchScore/Search"
    
    params={"searchId":"11211353' and '1=1","cardId":"18112133510420"}
    
    response=requests.post(url=url,params=params,headers=headers,allow_redirects=False)
    response.encoding = 'gbk'#网页中文乱码
    r=response.text
    #s=response.text.encode('utf-8').decode('unicode_escape')
    if len(r)>2000 :
       print(len(r))
    #res_tr=r'(?<\是否建档户)[\d\u4e00-\u9fa5]+'#提取行内容
    #res_tr=r'<span>(.*?)</span>(.*?)</div>'
    #m_tr =  re.findall(res_tr,r,re.S)
    #print(m_tr)
    #for a in m_tr:
      #a=re.findall(r'''[^-a-zA-Z<>',= "/\\]+''',str(a))
      #print(a)
    #fobj=open('/storage/emulated/0/88.txt','a')
    #fobj.write(r)


                     # 获取table工作表总行数
#ncols = jstable.ncols
for i in  range(1):
    print(i)
    teacherPj()
   

    
    
    
    



