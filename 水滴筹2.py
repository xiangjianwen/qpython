import urllib.parse 
dic=urllib.parse.parse_qs("size=20&infoUuid=989ae5d0-300e-47bd-a689-5fd23b847957&anchorId=&pageNum=1&selfTag=rPksrr4wG2PfeCHRrrj1514462782775&degree=0")
print(type(dic["degree"][0]))