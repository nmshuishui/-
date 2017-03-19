#coding: utf-8
from app import app
import sys
from app import monitor
from apscheduler.schedulers.background import BackgroundScheduler


reload(sys)
sys.setdefaultencoding('utf8')

# 线下apscheduler执行，线上不执行的原因就是因为启动方式导致的,因为定时任务写在了run.py里，而线下是直接启动的run.py，所以定时任务也启动了.
# 而线上是用gunicorn启动的，就没有执行run.py这个脚本，所以定时任务也没有启动成功
if __name__ == '__main__':
    sched = BackgroundScheduler()
    # 任务调度的三种方式: interval, cron, date
    # sched.add_job(monitor.mongoback_info_auto_refresh_getip, 'interval', minutes=10)
    sched.add_job(monitor.mongoback_info_auto_refresh_getip, 'cron', hour='12', minute='00')
    sched.start()
    app.run(host='0.0.0.0', port=9898, debug=True, threaded=True)
