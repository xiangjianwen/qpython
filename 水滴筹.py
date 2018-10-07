#!/usr/bin/python
# -*- coding: UTF-8 -*-
#import urllib.request
import requests
import json
import sys
import threading
import time  
import os
import urllib.parse 
#reload(sys)  
#sys.setdefaultencoding('utf8') 
def get_data(anchorId,pageNum,str_url):
    dic=urllib.parse.parse_qs(str_url)
    

    juan_dic=[]
    juanone_dic=""
    payload = {'size':'20','infoUuid':'989ae5d0-300e-47bd-a689-5fd23b847957','anchorId':'113636066','pageNum':'2','selfTag':'rPksrr4wG2PfeCHRrrj1514462782775','degree':'0'}
    payload['pageNum']=pageNum
    payload['anchorId']=anchorId
    payload['infoUuid']=dic["infoUuid"][0]
    payload['selfTag']=dic["selfTag"][0]
    payload['degree']=dic["degree"][0]
    #print(payload)
    #
    ret = requests.post("https://api.shuidichou.com/api/cf/v5/detail/get", data=payload)
   # print(ret.text)
    json_ret=json.loads(ret.text)
    for lst in json_ret["data"]["list"]:
        if lst["nickname"] is not None:
           juan_dic.append(lst["nickname"])
        else:
           juan_dic.append("n")
        if lst["userId"] is not None:
           juan_dic.append(str(lst["userId"]))
        else:
           juan_dic.append("n")
        if lst["amt"] is not None:
           juan_dic.append(str(lst["amt"]))
        else:
           juan_dic.append("n")
        if lst["comment"] is not None:
           juan_dic.append(lst["comment"])
           #input()
        else:
           juan_dic.append("n")
        if lst["time"] is not None:
           x = time.localtime(lst["time"])
           c=time.strftime('%Y-%m-%d %H:%M:%S',x)
           juan_dic.append(c)
        else:
           juan_dic.append("n")
        juanone_dic=juanone_dic+','.join(juan_dic)+"\n"
        juan_dic=[]
    list_anchorId_strjuan=[]   
    list_anchorId_strjuan.append(str(json_ret["data"]["anchorId"]))
    list_anchorId_strjuan.append(juanone_dic)
    return list_anchorId_strjuan
  
            #input()
#黎明    
s="size=20&infoUuid=813a7dee-4445-4777-ae17-61bbf4c8a230&anchorId=113736070&pageNum=2&selfTag=YXJCMCxrKf8TKSe65NM1514462946853&degree=2"
#王树欣
s2="size=20&infoUuid=989ae5d0-300e-47bd-a689-5fd23b847957&anchorId=&pageNum=1&selfTag=rPksrr4wG2PfeCHRrrj1514462782775&degree=0"
fobj=open('/storage/emulated/0/黎.txt','a')
idstr=[""]
for i in range(1,33):
    
    idstr=get_data(idstr[0],str(i),s)
    print(idstr[0])
    print(i)
    fobj.write(idstr[1])
fobj.close()
#while 1:
   #pass
