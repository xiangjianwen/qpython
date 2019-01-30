# -*- coding: utf-8 -*-


import requests
import time
import http.cookiejar
import re
import json

# 模拟浏览器访问
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.109 Safari/537.36'
}
home_url = "https://hfsjs.yunxiao.com/v1/exam/score-rates?cid=000000000000000180057039&pid=5a52c156000005a270605399"
base_login = "https://hfsjs.yunxiao.com/v1/auth/login"  # 一定不能写成http,否则无法登录

session = requests.session()
session.cookies = http.cookiejar.LWPCookieJar(filename='hfsCookies')
try:
    # 加载Cookies文件
    session.cookies.load(ignore_discard=True)
except:
    print("cookie未保存或cookie已过期")
    data = {"account":"17779376613","pass":"wo376613","rememberMe":2}

    print(data)

    # 第五步 登录
    response = session.post(base_login, data=data, headers=headers)
    print(response.content.decode("utf-8"))

    # 第六步 保存cookie
    session.cookies.save()

# 获取首页信息https://hfsjs.yunxiao.com/v1/exam/subject/compare?cid=000000000000000180057039&eid=000000000000000000147879&subject=%E6%95%B0%E5%AD%A6
def getdata(url,params):
    resp = session.get(url, headers=headers,params=params,allow_redirects=False)
    respjson=json.loads(resp.content)
    return respjson
hfsurl="https://hfsjs.yunxiao.com/v1/exam/score-rates"
getdatacs={"cid":"000000000000000180057039","pid":"5a52c156000005a270605399"}
for i in range(1,25):    
    getdatacs["cid"]="0000000000000001800570"+str(25+i)
    respjson=getdata(hfsurl,getdatacs)
    #print(respjson)
    j=8
    print(getdatacs["cid"]+"_"+str(respjson[j]["classTotalStudent"])+"  "+respjson[j]["name"]+"  "+str(respjson[j]["classTotalScore"]))
    j=j+1
    print(respjson[j]["name"]+"  "+str(respjson[j]["classTotalScore"])+respjson[j+1]["name"]+"  "+str(respjson[j+1]["classTotalScore"]))