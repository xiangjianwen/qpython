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
    params={"systemId":1,"backUrl":"http://www.qgjypt.com/login_ja.html","username":n,"password":p,"type":2}
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
        x=item5[ 5 if i==0 else (0 if (i>0 and i<5) else(1 if (i>=5 and i<8) else (2 if (i>=8 and i<15) else (3 if(i>=15 and i<18) else 4))))]
        sumitem20=sumitem20+itemOrder[i]+"#"+x+"@"
    #fobj=open('/storage/emulated/0/a黎.txt','a')
    #fobj.write(sumitem20)
    return sumitem20
    
def numTOstudentId(num,table):
       return table.cell_value(num,0)


def teacherPj(jsi,jsf): #教师序号，教师账号文件   
    
    jstable=rxlsx(jsf)#加载表
    nrows = jstable.nrows                         # 获取table工作表总行数
    #ncols = jstable.ncols
    
    acount=str(int(jstable.cell_value(jsi,0)))
     
    print(acount+jstable.cell_value(jsi,1))   
    num=0#第几个学生
    url = '''http://sr.qgjypt.com/ewms/school/teacherIndex.action'''
    
    #studentId=numTOstudentId(i,table)#转换学籍号
    c=getcookie(acount,"123456",headers)#获取登陆cookie
    r=requests.get(url=url,headers=headers,cookies=c)
    
    res_tr=r'<tr>(.*?)</tr>'#提取行内容
    m_tr =  re.findall(res_tr,r.text,re.S|re.M)
    classSub=[]#[[班级，未评价，[班级代码，科目代码，0]],[]]
    for line in m_tr:
        #print (line)
        #获取表格第列td 属性值
        res_td = r'<td[^>]*>(.*?)</td>'#提取列内容
        m_td = re.findall(res_td,line,re.S|re.M)
        #print(m_td)
        c1=[]
        for nn in m_td:
            #print(nn)
            
            allint=r'[\u4e00-\u9fa5,(\d,)]'#提取中文和数字
            x1=re.findall(allint,nn,re.S|re.M)
            x2=''.join(x1)
            c1.append(x2)
        classSub.append(c1)
    #print(classSub)
    for s in classSub:
       
       #print(s)
       m=re.findall(r'[^()]+', s[2])#提取括号的内容
       m1=m[0].split(",")
       s[2]=m1
       #print(m)  
    i=0    
    for s in classSub:    
        i=i+1
        print(i)
        print (s)
    #查找班级代码以及科目代码classCode=3611210450702006&subjectCode=0&userCode=36112104013
    classSubIndex=input('请输入评价的班级序号如，1,2，已评价输入0跳过,00重评:\n')
    if(classSubIndex=="0"):
       return 0
    if(classSubIndex=="00"):
       teacherPj(jsi,jsf)
    
    classCode=classSub[int(classSubIndex)-1][2][0]
    subjectCode=classSub[int(classSubIndex)-1][2][1]
    url1 = '''http://sr.qgjypt.com/ewms/school/addOrUpdateGradeDate.action'''
    f=input('请输入等级文件名：\n')
    table=rxlsx(f)

    hponeGradeData=getGradeData(table,"n")#构
    params={"flag":2,"gradeData":hponeGradeData,"classCode":classCode,"subjectCode":subjectCode,"userCode":acount}
    r=requests.post(url=url1,headers=headers,data=params,cookies=c)
    print(r.text)
    if(r.text=="success") :
       teacherPj(jsi,jsf)
jsf=input('请输入教师文件名：\n')

jstable=rxlsx(jsf)#加载表
nrows = jstable.nrows                        # 获取table工作表总行数
#ncols = jstable.ncols
for i in  range(nrows):
    
    teacherPj(i,jsf)

    
    
    
    



