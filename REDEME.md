# 2017.11
pip install --upgrade pip
pip install -r requirements.txt (sudo su - 以root用户执行)
pip freeze > requirements.txt(生成)

代码自动发布: 需将此机器(开发机)的公钥拷到tools.uc.ppweb.com.cn

flask开发模式下的启动方式:
    python run.py

gunicorn启动:
    第一个app： 表示app这个包名
    第二个app： 表示app包中 Flask(__name__)实例化的对象
    gunicorn -w4 -b0.0.0.0:9898 app:app -D
    项目部署在tools.uc.ppweb.com.cn:/data/oop下
    线上启动，直接运行run.sh即可(run.sh和cmdb目录同级)

nginx代理80端口:
    server {
            listen 80;
            server_name oop.lieyan.com.cn;

            access_log /var/log/nginx/oop.lieyan.com.cn/access.log;
            error_log /var/log/nginx/oop.lieyan.com.cn/error.log;
            client_max_body_size 2m;

            location / {
                    proxy_pass http://0.0.0.0:9898;
                    proxy_set_header X-Forwarded-For $remote_addr;
                    proxy_set_header Host $http_host;
            }
    }

stat_import.py 直接连fps6.uc的mongo,用于将 进入战斗统计,战斗帧率统计,鼠标移动统计,游戏加载统计,游戏内存统计,游戏卡顿统计 查到的数据传到此服务器的 statistics.py下的statapi,然后入库
path: oop.lieyan.com.cn 做定时任务 01 09 * * * python /data/oop/cmdb/stat_import.py


statistics.py下的stat_data_api 用于接收每个服务器上的定时任务脚本 new_report_html.py的数据:游戏数据日统计,游戏数据周统计,游戏数据月统计,游戏数据累计统计

查看服务器包的版本号:
    脚本路径:salt服务器,tools.uc.ppweb.com.cn
    每10分钟跑一次的定时任务: */10 * * * * /home/op/sh/server_status.sh >/home/op/sh/server_status.log 2>&1

服务器更新版本监控:
    crontab -l,每10分钟监控一次
    tools.uc.ppweb.com.cn:/home/op/sh/server_status.sh


Celery:
    /etc/init.d/rabbitmq-server start
    cd cmdb
    celery -A app.tasks worker --loglevel=info >/tmp/celery.log 2>&1 &  # 启动Celery处理任务,在tasks模块儿目录启动，最好用supervisor后台启动,如果只有tasks而不是app.tasks就会报一个KeyError

# pip安装不了任何包
    Could not find a version that satisfies the requirement virtualenv (from versions: )
    sudo pip install flask -vvvv
    解决办法:
        方法1、pip --trusted-host pypi.python.org install flask
        方法2、vim ~/.pip/pip.conf
            [global]
            index-url = http://pypi.douban.com/simple
            trusted-host = pypi.douban.com
            disable-pip-version-check = true
            timeout = 120

sudo apt-get install libssl-dev

# db.py
    sudo apt-get install python-mysqldb

# tasks.py
    sudo apt-get install rabbitmq-server

# code_release.py
    sudo apt-get install python-svn
