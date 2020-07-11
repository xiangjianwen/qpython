import os;
def x(oldname,newname):
    newpath="/storage/emulated/0/a/n"#这里替换为你的文件夹的路径";
    path="/storage/emulated/0/a/Pictures"#这里替换为你的文件夹的路径";
    #path="/storage/emulated/0/a"#这里替换为你的文件夹的路径";
    filelist=os.listdir(path)#该文件夹下所有的文件（包括文件夹）
    i=0
    
    for files in filelist:#遍历所有文件
        i=i+1
        Olddir=os.path.join(path,files);#原来的文件路径
    
        if os.path.isdir(Olddir):#如果是文件夹则跳过
    
           continue;
    
        filename=os.path.splitext(files)[0];#文件名
        #newfilename=int(filename)+2
        #if(newfilename>=131 and newfilename<=373):
        if(filename==oldname):
        	
        #newfilename=2*int(filename[3:])-3
           filetype=os.path.splitext(files)[1];#文件扩展名
    
           Newdir=os.path.join(newpath,str(newname)+filetype);#新的文件路径
    
           os.rename(Olddir,Newdir);#重命名
    
 #   
def rename():
	page=28#
	startpage=29#
	f=0#0表示修改偶数页码
    for c in range(page) :
        oldname='2020师德_'+str(c+startpage)#原来文件名格式:某某_连续数字
        newname=2*(c+1)-f#新文件名
        x(oldname,newname)
        #os.rename(Olddir,Newdir);#重命名
    
    

rename();
#x()

