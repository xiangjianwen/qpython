#最后，把以上整理成一个.sh文件，在命令行运行bash termux_python.sh一键安装
#执行termux-setup-storage(注意：这个命令只能在手机上执行才能弹出授权对话框
#Termux安装python所需要的一些库
#第一步1.termux_python.sh复制到/data/data/com.termux/files/home才能运行
#/data/data/com.termux/files/home/storage/shared/azhihu
#第二步2.Permission denied 更改权限chmod 764 termux_python.sh
apt update

apt upgrade

apt install -y python python-dev python2 python2-dev

apt-get install -y clang

apt-get install -y libxml2 libxml2-dev libxslt libxslt-dev 

apt install -y openssl libffi libffi-dev libcrypt-dev

apt install -y openssl openssl-tool openssl-dev

apt install -y clang g++  libxml2-dev libxslt-dev python python-dev

apt install -y clang python python-dev

apt install -y fftw libzmq libzmq-dev

apt install -y freetype freetype-dev libpng libpng-dev pkg-config
pip install  --upgrade pip

pip install BeautifulSoup4 requests

pip install  lxml

pip install  scrapy



