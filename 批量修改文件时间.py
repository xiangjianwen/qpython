0# -*- coding: utf-8 -*-
import os
import sys
import time

#reload(sys)
#sys.setdefaultencoding('utf8')


path = u"/storage/emulated/0/a/2020"
result = os.listdir(path)
result.sort()
for file in result:
        full_path = os.path.join(path, file)
        #print(full_path)
        #print(file)
        t=1330712292
        t=1330712292-1
        mtime = os.stat(full_path).st_mtime
        file_modify_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(mtime))
        print("{0} 修改时间是: {1}".format(full_path,file_modify_time))
        os.utime(full_path,(1330712280, t))
        print("{0} 修改时间是: {1}".format(full_path,file_modify_time))