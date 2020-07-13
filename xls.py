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
info='墨周洲hhh迹'
wxlsx(rxlsx("99"),info,'99')

