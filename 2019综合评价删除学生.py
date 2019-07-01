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
    url = "http://sr.qgjypt.com/ewms/login_login.action"
    params={"systemId":1,"backUrl":"http://www.qgjypt.com/login_ja.html","username":n,"password":p,"type":3}
    response=requests.post(url=url,params=params,headers=headers,allow_redirects=False)
    cookies=response.cookies
    c=requests.utils.dict_from_cookiejar(cookies)
    #c=response.headers
    print ("cookies:",c)
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
            #print(cell_value)
            if (cell_value=="A" and table.cell_value(i,0)!=StudentId) :
               itemA.append(table.cell_value(i,0))
            if (cell_value=="B" and table.cell_value(i,0)!=StudentId):
               itemB.append(table.cell_value(i,0))
            if (cell_value=="C" and table.cell_value(i,0)!=StudentId):
               itemC.append(table.cell_value(i,0))
        item5.append(';'.join(itemA)+'#'+';'.join(itemB)+'#'+';'.join(itemC)+'#')
    #print(len(item5))
    for i in  range(20):
        x=item5[ 5 if i==0 else (1 if (i>0 and i<5) else(1 if (i>=5 and i<8) else (2 if (i>=8 and i<15) else (3 if(i>=15 and i<18) else 4))))]
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
def getstudit(c,studentCode):#学籍号转删除stuId
    s=[]
    url="http://sr.qgjypt.com/ewms/enrollment/student_inf_qry.action"   
    
   # studentCode="L442000200301260114"
    params={"pageno":1,"classCode":"","schoolCode":"361121045","studentCode":studentCode,"name":"","sortName":"s.xsi_id","sortOper":"asc"}
    r=requests.post(url=url,headers=headers,data=params,cookies=c)
   # print(r.text)
    res_tr=r'<tr>(.*?)</tr>'#提取行内容
    m_tr =  re.findall(res_tr,r.text,re.S|re.M)
    res_td = r'<td[^>]*>(.*?)</td>'#提取列内容
    m_td = re.findall(res_td,m_tr[0],re.S|re.M)
    #print(m_td[1]+m_td[2])
    m=re.findall(r'[^()]+', m_td[9])#提
    m1=re.findall(r"'(.*?)'", m[1])
    #print(m1[0])
    s.append(m_td[1]+m_td[2])
    s.append(m1[0])
    return(s)
def delstudent(c,headers,stuId):
    url1="http://sr.qgjypt.com/ewms/enrollment/student_delete.action"
    params={"pageno":1,"classCode":"","schoolCode":"361121045","studentCode":"","name":"","sortName":"s.xsi_id","sortOper":"asc","stuId":stuId}
    r=requests.post(url=url1,headers=headers,data=params,cookies=c)
    #print(r.text)
    
c=getcookie("36112104501","123456",headers)    
#getstudit(c,"L442000200301260114")

#print(c)
f=input('请输入要删除学生学籍号xls：\n')
table=rxlsx(f)
nrows = table.nrows  
j=0                       # 获取table工作表总行数
studitlists=[]
#确认要所有要删除学生
for i in range(nrows):
  cell_value = table.cell_value(i,0) #获取第i行中第j列的值
  
  if(cell_value!=""):
   
    studitlist=getstudit(c,cell_value)
    studitlists.append(studitlist)
    j=j+1
    print(str(j)+studitlist[0])
#删除
f=input("要删除输入0，否则输入1\n")
if(f=="0"):
  for stutid in studitlists:
    delstudent(c,headers,stutid[1])
    print(stutid)
    

