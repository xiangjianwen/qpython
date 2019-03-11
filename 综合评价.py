# -*- coding: utf-8 -*-


import requests
import time
import http.cookiejar
import re
import xlrd
import sys
import os
# 模拟浏览器访问
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.109 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded',
    'X-Requested-With': 'XMLHttpRequest'
}
#home_url = "https://hfsjs.yunxiao.com/v1/overview/focus-students?classId=000000000000000180057039&subjects=%E6%95%B0%E5%AD%A6"
#base_login = "https://hfsjs.yunxiao.com/v1/auth/login"  # 一定不能写成http,否则无法登录

def getcookie(n,p,headers):
    url = "http://sr.qgjypt.com/login_login.action"
    params={"systemId":1,"backUrl":"http://www.qgjypt.com/login_sr.html","username":n,"password":p,"type":1}
    response=requests.post(url=url,params=params,headers=headers,allow_redirects=False)
    cookies=response.cookies
    c=requests.utils.dict_from_cookiejar(cookies)
    #c=response.headers
    #print ("cookies:",c)
    return cookies
def rxlsx(xlsname):#读文件
    fname = xlsname+".xls"
    if not os.path.isfile(fname):
        print (u'文件路径不存在')
        sys.exit()
    data = xlrd.open_workbook(fname)            # 打开fname文件
    data.sheet_names()
    table = data.sheet_by_index(0)
    return table
def getGradeData(table,StudentId):
    itemOrder=['SZ23633982','SZ953407340','SZ912310849','SZ1105658220','SZ1690500495','SZ1573027611','SZ2061325740','SZ1587667510','SZ566995990','SZ1129177966','SZ458681618','SZ1015873975','SZ1315393802','SZ187283717','SZ760028129','SZ602006065','SZ152157395','SZ332352831','SZ922672564','SZ694138407',]
    item5=[]
    sumitem20=""
    nrows = table.nrows                         # 获取table工作表总行数
    ncols = table.ncols
    for j in range(1, ncols):
        itemA=[]   
        itemB=[]
        itemC=[]
        for i in  range(nrows):
            cell_value = table.cell_value(i,j) #获取第i行中第j列的值
            print(cell_value)
            if (cell_value=="A" and table.cell_value(i,0)!=StudentId) :
               itemA.append(table.cell_value(i,0))
            if (cell_value=="B" and table.cell_value(i,0)!=StudentId):
               itemB.append(table.cell_value(i,0))
            if (cell_value=="C" and table.cell_value(i,0)!=StudentId):
               itemC.append(table.cell_value(i,0))
        item5.append(';'.join(itemA)+'#'+';'.join(itemB)+'#'+';'.join(itemC)+'#')
    #print(len(item5))
    for i in  range(20):
        x=item5[ 5 if i==0 else (0 if (i>0 and i<5) else(1 if (i>=5 and i<8) else (2 if (i>=8 and i<15) else (3 if(i>=15 and i<18) else 4))))]
        sumitem20=sumitem20+itemOrder[i]+"#"+x+"@"
    #fobj=open('/storage/emulated/0/a黎.txt','a')
    #fobj.write(sumitem20)
    #print(sumitem20)
    #sf=input('暂停：\n')
    
    return sumitem20
def numTOstudentId(num,table):
       return table.cell_value(num,0)
def zpGetGradeData(table,Id):
    itemOrder=['SZ23633982','SZ953407340','SZ912310849','SZ1105658220','SZ1690500495','SZ1573027611','SZ2061325740','SZ1587667510','SZ566995990','SZ1129177966','SZ458681618','SZ1015873975','SZ1315393802','SZ187283717','SZ760028129','SZ602006065','SZ152157395','SZ332352831','SZ922672564','SZ694138407',]
    item5=[]
    sumitem20=""
    nrows = table.nrows                         # 获取table工作表总行数
    ncols = table.ncols
  
    for j in  range(1,ncols):
            cell_value = table.cell_value(Id,j) #获取第i行中第j列的值
            #print(cell_value)
            if (cell_value=="A" ) :
               item5.append('#'+table.cell_value(Id,0)+'###')
            if (cell_value=="B" ) :
               item5.append('##'+table.cell_value(Id,0)+'##') 
            if (cell_value=="C" ) :
               item5.append('###'+table.cell_value(Id,0)+'#')
            
    for i in  range(20):
        x=item5[ 5 if i==0 else (1 if (i>0 and i<5) else(1 if (i>=5 and i<8) else (2 if (i>=8 and i<15) else (3 if(i>=15 and i<18) else 4))))]
        sumitem20=sumitem20+itemOrder[i]+x+"@"
    #print(sumitem20)
    #sf=input('暂停：\n')
    return sumitem20
    #print(sumitem20)      
    
    
f=input('请输入等级文件名：\n')
table=rxlsx(f)
num=0#第几个学生
url = '''http://sr.qgjypt.com/school/addOrUpdateGradeDate.action'''
for i in  range(0,table.nrows):
    studentId=numTOstudentId(i,table)#转换学籍号
    print(studentId)
    hponeGradeData=getGradeData(table,studentId)#构造一个学生提交数据
    zponeGradeData=zpGetGradeData(table,i)
    c=getcookie(studentId,"123456",headers)#获取登陆cookie
    params={"flag":1,"gradeData":hponeGradeData,"userCode":studentId}
    zparams={"flag":0,"gradeData":zponeGradeData,"userCode":studentId}
    r=requests.post(url=url,headers=headers,data=params,cookies=c)
    zr=requests.post(url=url,headers=headers,data=zparams,cookies=c)
    print(str(i)+" "+table.cell_value(i,8)+studentId+" "+r.text+'\n'+"zp"+" "+zr.text) 



