import os;
def x():
    newpath="/storage/emulated/0/Pictures"#这里替换为你的文件夹的路径";
    path="/storage/emulated/0/a"#这里替换为你的文件夹的路径";
    #path="/storage/emulated/0/a"#这里替换为你的文件夹的路径";
    filelist=os.listdir(path)#该文件夹下所有的文件（包括文件夹）
    i=0
    
    for files in filelist:#遍历所有文件
        i=i+1
        Olddir=os.path.join(path,files);#原来的文件路径
    
        if os.path.isdir(Olddir):#如果是文件夹则跳过
    
           continue;
    
        filename=os.path.splitext(files)[0];#文件名
        newfilename=int(filename)+2
        if(newfilename>=131 and newfilename<=373):
        
        #newfilename=2*int(filename[3:])-3
           filetype=os.path.splitext(files)[1];#文件扩展名
    
           Newdir=os.path.join(newpath,str(newfilename)+filetype);#新的文件路径
    
           os.rename(Olddir,Newdir);#重命名
    
    
def rename():

    #path="/storage/emulated/0/Pictures"#这里替换为你的文件夹的路径";
    newpath="/storage/emulated/0/a"#这里替换为你的文件夹的路径";
    path="/storage/emulated/0/a"#这里替换为你的文件夹的路径";
    filelist=os.listdir(path)#该文件夹下所有的文件（包括文件夹）
    i=0
    ss=[]
    for files in filelist:#遍历所有文件
        i=i+1
        Olddir=os.path.join(path,files);#原来的文件路径
    
        if os.path.isdir(Olddir):#如果是文件夹则跳过
    
           continue;
    
        filename=os.path.splitext(files)[0];#文件名
        #newfilename=2*int(filename[3:])+152#改偶数
        newfilename=int(filename)
        #print(newfilename)
        ss.append(newfilename)
          #input()
        #newfilename=2*int(filename[3:])-3
        filetype=os.path.splitext(files)[1];#文件扩展名
    
        Newdir=os.path.join(newpath,str(newfilename)+filetype);#新的文件路径
    nss=sorted(ss)
    j=1
    for c in nss:
        j=j+1
        if(c!=j):
          print(c)
        #os.rename(Olddir,Newdir);#重命名
    
    

rename();
#x()

