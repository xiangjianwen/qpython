# -*- coding: utf-8 -*-	
import json
import requests
import time
import http.cookiejar
import re
import urllib
import os, sys
headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.109 Safari/537.36'
        }
     
def login():
    # 模拟浏览器访问
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.109 Safari/537.36'
        }
        home_url = "https://hfsjs.yunxiao.com/v1/user/info"
        base_login = "https://hfsjs.yunxiao.com/v1/auth/login"  # 一定不能写成http,否则无法登录
        
        session = requests.session()
        session.cookies = http.cookiejar.LWPCookieJar(filename='ZhiHuCookies')
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
        return session
session=login()
#根据班级id获取考试名称返回考试eid,考试名称name，考试时间timeStr
def getexamlist(cid,url_km):
    headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.109 Safari/537.36'
        }
    home_url="https://hfsjs.yunxiao.com/v1/exam/list?cid=000000000000000"+str(cid)+"&subject="+url_km
    resp = session.get(home_url, headers=headers, allow_redirects=False)
    json_content=json.loads(resp.content)
    #print(json_content)
    examdic={}
    for exam in json_content:
      #print(exam["id"]+" "+exam["name"]+" "+exam["timeStr"])
      #examdic.append({"id":exam["id"],"name":exam["name"],"timeStr":exam["timeStr"]})
      examdic={"id":exam["id"],"name":exam["name"],"timeStr":exam["timeStr"]}
      break
    return examdic
def getclassid(headers,session):
    # 获取考试与试卷id信息
        home_url = "https://hfsjs.yunxiao.com/v1/user/info"
  
        cid=[]
        resp = session.get(home_url, headers=headers, allow_redirects=False)
        json_content=json.loads(resp.content)
        #print(json_content)
        try:
           if json_content["message"]=="未授权访问":
              os.remove("ZhiHuCookies")
              print("重新运行程序")
        except:
          
    
            i=0
            for c in json_content["classes"]:
                
                cid.append([c["id"],c["grade"],c["name"]])
                print(str(i)+" "+c["id"]+" "+c["grade"]+" "+c["name"])
                i=i+1
            #print(cid)
            a=input("sect as 0,1,2..:" )
            sect_index_cid=cid[int(a)][0]
            return sect_index_cid #包含试卷id，年级，班级
id=getclassid(headers,session)
def lastexam(session,id):#最近考试 examId，paperId
    print("当前班级classid:"+str(id))#五班id
    a=input("输入范围例如 10 在当前班级+-10:")
    examinfo=[]
    i=0
    km=input("输入要查的科目例如数学:")
    #url_km=urllib.quote(km.decode(sys.stdin.encoding).encode('utf8'))
    url_km= urllib.parse.quote(km)
  
    for cid in range(int(id)-int(a),int(id)+int(a)):  #其他班id  
        lastexam_url="https://hfsjs.yunxiao.com/v1/overview/last-exam/subject?classId=000000000000000"+str(cid)+"&className=5&subject="+url_km
        
        resp = session.get(lastexam_url, headers=headers, allow_redirects=False)
        print(len(resp.content))
        
        if len(resp.content)<50:
           continue
        json_content=json.loads(resp.content)
        #print(str(cid)+" examId"+json_content["examId"]+" paperId "+json_content["paperId"]+" "+json_content["subject"])
        examdic=getexamlist(cid,url_km)
        t={"cid":"000000000000000"+str(cid),"examId":json_content["examId"],"paperId":json_content["paperId"],"subject":json_content["subject"],"id":examdic["id"],"name":examdic["name"],"timeStr":examdic["timeStr"]}
        print(str(i)+"  "+str(cid))
        i=i+1
        print(examdic)
        #t=[json_content["examId"],json_content["paperId"],json_content["subject"],examdic["id"],examdic["name"],examdic["timeStr"]]
        examinfo.append(t)
      
    return examinfo
examinfo=lastexam(session,id)#examinfo
def getallclass(examinfo):
    
    a=input("选择 examid index 0,1,2..: ")
    eid=examinfo[int(a)]["examId"]
    print(eid)
    i=0
    t=[]
    for e in examinfo:
       #print(e["examId"])
       if(e["examId"]==eid):
         i=i+1
         print(str(i)+"  "+e["cid"]+" "+e["examId"]+" "+e["name"]+"paperId "+e["paperId"]+" "+e["timeStr"])
         t.append({"cid":e["cid"],"examId":e["examId"],"paperId":e["paperId"],"timeStr":e["timeStr"]})
    return t

t=getallclass(examinfo)#get cid eid pid

def get_score_info(t,session):
    i=0
    headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.109 Safari/537.36'
        }
    for dic_eid_cid_pid in t:
       i=i+1
       cid=dic_eid_cid_pid["cid"]
       eid=dic_eid_cid_pid["examId"]
       pid=dic_eid_cid_pid["paperId"]
       home_url = "https://hfsjs.yunxiao.com/v1/paper/review/base?cid="+cid+"&pid="+pid+"&eid="+eid+"000000000000000000195293/v1/user/info"
       resp = session.get(home_url, headers=headers, allow_redirects=False)
       json_content=json.loads(resp.content)
       oneclass_scoreinfo=""
       for json_content_item in json_content:
           oneclass_scoreinfo=oneclass_scoreinfo+json_content_item["name"]+","+str(json_content_item["currScoringRate"])[0:5]+","
       s=cid+","+str(i)+","+oneclass_scoreinfo+"\n"
       print(s)
       fobj=open('/storage/emulated/0/好分数数据.csv','a')

       fobj.write(s)
       fobj.close()
get_score_info(t,session)


