#!/usr/bin/python  
# -*- coding:utf-8 -*-
import io
import sys
from station import stations
#sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8') #改变标准输出的默认编码
import json
import re
from get_urltrain import d,f1,t1,f,t
import urllib
from urllib import request
import requests
from pprint import pprint
from get_urltrain import url
from prettytable import PrettyTable
from termcolor import colored, cprint

station_no=[]#车次代码
station_code=[]#车次
f2=""

def get_station(train_no,from_station,to_station,date):#获取列车各个站名
    station_names=[]
    station_train_url="https://kyfw.12306.cn/otn/czxx/queryByTrainNo?train_no="+train_no+"&from_station_telecode="+from_station+"&to_station_telecode="+to_station+"&depart_date="+date
    header={'User-Agent':   'Mozilla/5.0 (Windows NT 6.1; rv:45.0) Gecko/20100101 Firefox/45.0'}
    #print(station_train_url)
    r = requests.get(station_train_url, headers=header)
    rs=r.text
    rs=rs[:10]
    if rs.find("date")!=-1:#返回包含字符串“date”
    
        json_r=json.loads(r.text)
        station_names_json = json_r['data']['data']
        for station_name in station_names_json:
            station_names.append(station_name['station_name'])
    return station_names

def forword_to_station(from_station_name,to_station_name,station_code,station_names,date):#列车车次station_code指定站的前一站到目的站的信息
    findex=0
    #print(station_names)
    for i,s in enumerate(station_names):
        if from_station_name in s:
            findex=i
    #findex=station_names.index(from_station_name)
    #print(findex)
    if findex==0 :
       findex=findex+1 
    forword_station_name=station_names[findex-1]#开始-1前一站
    global stations
    global f2
    f2=forword_station_name
    #print(f2)
    f=stations[forword_station_name]
    t=stations[to_station_name]
    url = 'https://kyfw.12306.cn/otn/leftTicket/queryZ?leftTicketDTO.train_date='+date+'&leftTicketDTO.from_station='+f+'&leftTicketDTO.to_station='+t+'&purpose_codes=ADULT'
    header={'User-Agent':   'Mozilla/5.0 (Windows NT 6.1; rv:45.0) Gecko/20100101 Firefox/45.0'}
    r = requests.get(url, headers=header)
    #print(r.text)
    rs=r.text
    rs=rs[:10]
    #print(rs)
    if rs.find("data")!=-1:#返回包含字符串“data”
        json_r=json.loads(r.text)
        rows = json_r['data']['result']
        for row in rows :
            row_stations = row.split('|')
            if row_stations[3]==station_code:
               return row
               break
    
header={'User-Agent':   'Mozilla/5.0 (Windows NT 6.1; rv:45.0) Gecko/20100101 Firefox/45.0'}
r = requests.get(url, headers=header)
print(r.text)
rs=r.text
rs=rs[:10]

if rs.find("data")==-1:#返回包含字符串“data”
    print(rs[:30])
else:         
    json_r=json.loads(r.text)
    rows = json_r['data']['result']
    trains= PrettyTable()
    trains.field_names=["车次","车站","时间","历时","商务","一","二","硬","软 ","无","卧"]
    num = len(rows)
    for row1 in rows :
        row1_stations = row1.split('|')
        station_no.append(row1_stations[2])#车次代码
        station_code.append(row1_stations[3])#获取所有车次
        


    for i,row in enumerate(rows) :
        row_stations = row.split('|')
        cprint((str(i)+"--"+row_stations[3]+f1+"-"+t1),'green')
        trains.add_row([colored(row_stations[3],'green'),
                        colored(f1+"-"+t1,"green"),
                        colored(row_stations[8],'green'),
                        colored(row_stations[10],'green'),colored(row_stations[32],'green'),
                        colored(row_stations[31],'green'),colored(row_stations[30],'green'),
                        colored(row_stations[29],'green'),colored(row_stations[28],'green'),
                        colored(row_stations[26],'green'),colored(row_stations[23],'green')])
        trow=get_station(row_stations[2],f,t,d)
        #print(trow)
        if trow !=[] :
            if trow is not None:
                #print(trow)
                forward_row_stations_row=forword_to_station(f1,t1,row_stations[3],trow,d)
                #print(forward_row_stations_row)
                if forward_row_stations_row is not None:
                    #print(forward_row_stations_row)
                    forward_row_stations=forward_row_stations_row.split('|')
                    print(str(i)+"--"+forward_row_stations[3]+f2+"-"+t1)
                    trains.add_row([forward_row_stations[3],f2+"-"+t1,forward_row_stations[8],forward_row_stations[10],forward_row_stations[32],
                        forward_row_stations[31],forward_row_stations[30],forward_row_stations[29],forward_row_stations[28],forward_row_stations[26],forward_row_stations[23]])
        
    print ('查询结束，共有 %d 趟列车。'%num )
    print (trains)