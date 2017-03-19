#!/bin/bash
# run.sh 要放在和cmdb同级目录，直接 bash run.sh 即可启动后台

# mysql: oop -> BHlog2016
cd /data/oop
sed -i "/def execute_sql/ s/10.0.12.254/localhost/" cmdb/app/db.py
sed -i "/def execute_sql/ s/user='root'/user='oop'/" cmdb/app/db.py
sed -i "/def execute_sql/ s/passwd='root'/passwd='BHlog2016'/" cmdb/app/db.py

ps -ef |grep gunicorn|grep -v grep|awk '{print $2}'|xargs kill
ps -ef |grep celery|grep -v grep|awk '{print $2}'|xargs kill
find /data/oop -name *.pyc -exec rm -rf {} \;

cd cmdb
celery -A app.tasks worker --loglevel=info >/tmp/celery.log 2>&1 &
gunicorn -w4 -b0.0.0.0:9898 app:app -D
