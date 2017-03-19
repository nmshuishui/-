#coding: utf-8

from flask import render_template, request
from . import app
from login_require import login_required
import db
from utils import util
import datetime, time
import json
import traceback
from tasks import celery


@app.route('/mongo_monitor/')
@login_required
def mongo_monitor():
    servers_columns = ['qufu', 'hostname', 'wan_ip', 'back_num', 'back_name', 'back_size','back_starttime','back_endtime', 'back_used_time', 'server_id', 'refresh_time']
    servers = db.get_list(servers_columns, 'virtuals')
    server_hostname_columns = ['id', 'hostname']
    server_hostname = db.get_list(server_hostname_columns, 'server')
    for hostname in server_hostname:
        for server in servers:
            if server['server_id'] == (hostname['id']):
                server['server_id'] = hostname['hostname']
    return render_template('monitor/mongo_monitor.html', servers=servers)

@app.route('/mongo_update/', methods=['POST'])
@login_required
@celery.task
def mongo_update():
    host = request.form.get('ip')
    back_num = 'ls /backup/mongodata/backup/full |wc -l'
    back_name = 'ls -rt /backup/mongodata/backup/full|tail -1'
    back_size = "ls -lrt --block-size=M /backup/mongodata/backup/full|tail -1|awk '{print $5}'"
    back_endtime = "ls -lrt /backup/mongodata/backup/full|tail -1|awk '{print $(NF-1)}'"
    try:
        # 如果页面没有设置备份时间，则默认设置05:05存入数据库
        if json.loads(db.get_one(['back_starttime'], "wan_ip='%s'" % host, 'virtuals'))['back_starttime'] is None:
            back_startTime = '05:05'
            data = dict({'back_startTime': back_startTime})
            where = 'wan_ip=' + "'%s'" % host
            db.update(data, where, 'virtuals')
        else:
            back_startTime = json.loads(db.get_one(['back_starttime'], "wan_ip='%s'" % host, 'virtuals'))['back_starttime']
        back_endTime = util.paramiko_command(host, back_endtime)
        back_startTime=datetime.datetime.strptime(back_startTime, "%M:%S")
        if back_endTime == 1:
            back_endTime = '00:00'
        back_endTime = datetime.datetime.strptime(back_endTime, "%M:%S")
        seconds = (back_endTime-back_startTime).seconds
        hours = seconds / 60
        second = seconds % 60
        back_used_time = '%s小时%s分' % (hours, second)
        referesh_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        data = dict({'back_num': util.paramiko_command(host, back_num), 'back_name': util.paramiko_command(host, back_name),
                    'back_size': util.paramiko_command(host, back_size), 'back_endtime': util.paramiko_command(host, back_endtime),
                     'back_used_time': back_used_time, 'refresh_time': referesh_time})
        if len(str(data['back_size'])) >= 5:
            data['back_size'] = str(round(float(float(data['back_size'][0:-1]) / 1024),2)) + 'G'
        where = 'wan_ip=' + "'%s'" % (host)
        db.update(data, where, 'virtuals')
    except:
        traceback.print_exc()
    return render_template('monitor/mongo_monitor.html')

def mongoback_info_auto_refresh_getip():
    ip_list = []
    [ ip_list.append(ip['wan_ip']) for ip in db.get_list(['wan_ip'], 'virtuals') ]
    for ip in ip_list:
        mongoback_info_auto_refresh(ip)

def mongoback_info_auto_refresh(ip):
    host = ip
    back_num = 'ls /backup/mongodata/backup/full |wc -l'
    back_name = 'ls -rt /backup/mongodata/backup/full|tail -1'
    back_size = "ls -lrt --block-size=M /backup/mongodata/backup/full|tail -1|awk '{print $5}'"
    back_endtime = "ls -lrt /backup/mongodata/backup/full|tail -1|awk '{print $(NF-1)}'"
    try:
        # 如果页面没有设置备份时间，则默认设置05:05存入数据库
        if json.loads(db.get_one(['back_starttime'], "wan_ip='%s'" % host, 'virtuals'))['back_starttime'] is None:
            back_startTime = '05:05'
            data = dict({'back_startTime': back_startTime})
            where = 'wan_ip=' + "'%s'" % host
            db.update(data, where, 'virtuals')
        else:
            back_startTime = json.loads(db.get_one(['back_starttime'], "wan_ip='%s'" % host, 'virtuals'))['back_starttime']
        back_endTime = util.paramiko_command(host, back_endtime)
        back_startTime=datetime.datetime.strptime(back_startTime, "%M:%S")
        if back_endTime == 1:
            back_endTime = '00:00'
        back_endTime = datetime.datetime.strptime(back_endTime, "%M:%S")
        seconds = (back_endTime-back_startTime).seconds
        hours = seconds / 60
        second = seconds % 60
        back_used_time = '%s小时%s分' % (hours, second)
        referesh_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        data = dict({'back_num': util.paramiko_command(host, back_num), 'back_name': util.paramiko_command(host, back_name),
                    'back_size': util.paramiko_command(host, back_size), 'back_endtime': util.paramiko_command(host, back_endtime),
                     'back_used_time': back_used_time, 'refresh_time': referesh_time})
        if len(str(data['back_size'])) >= 5:
            data['back_size'] = str(round(float(float(data['back_size'][0:-1]) / 1024),2)) + 'G'
        where = 'wan_ip=' + "'%s'" % (host)
        db.update(data, where, 'virtuals')
    except:
        traceback.print_exc()


@app.route('/update_mongo_starttime/', methods=['POST'])
def update_mongo_starttime():
    start_time = request.form.get('back_start_time').encode('utf8')
    data = {'back_starttime': start_time}
    where = "wan_ip='%s'" % request.form.get('wan_ip')
    try:
        time.strptime(start_time, '%H:%M')
        hour = time.strptime(start_time, '%H:%M').tm_hour
        min = time.strptime(start_time, '%H:%M').tm_min
        cmd = "echo 'xxxxx'|sudo -S sh -c" + ' "' + "echo '%s %s * * * op /home/op/mongo/mongo-admin-utils/bin/fullbackup.sh >/tmp/fullbackup.log 2>&1' > /etc/cron.d/mongo_fullback" % (min,hour) + '"'
        util.paramiko_command(request.form.get('wan_ip'), cmd)
        db.update(data, where, 'virtuals')
        data = {"code":0, 'errmsg':'备份开始时间修改成功'}
    except:
        data = {"code":1, 'errmsg':'时间格式不合法'}
    return json.dumps(data)


@app.route('/operating/')
@login_required
def operating():
    return render_template('monitor/operating.html', server_list = server_status())


@app.route('/manager/')
@login_required
def manager():
    return render_template('monitor/manager.html', server_list = server_status())


@app.route('/backupServer_monitor/')
@login_required
def backupServer_monitor():
    ip_list = db.get_list(['qufu','hostname','wan_ip','backNum','backName','backSize'], 'backupServerMonitor')
    return render_template('monitor/backupServer_monitor.html', infos=ip_list)


def backupServer_monitor_cron():
    ip_list = db.get_list(['wan_ip','qufu','hostname'], 'virtuals')
    for ip in ip_list:
        dirname = '/data/mongobackup/' + ip['wan_ip']
        backNum = util.paramiko_command('121.201.72.22', 'ls %s|wc -l' % dirname)
        ip['backNum'] = backNum
        backName = util.paramiko_command('121.201.72.22', 'ls -rt %s|tail -1' % dirname)
        ip['backName'] = backName
        backSize = util.paramiko_command('121.201.72.22', "ls -lrt --block-size=M %s |tail -1|awk '{print $5}'" % dirname)
        ip['backSize'] = backSize
        if len(ip['backSize']) >= 5:
            ip['backSize'] = str(round(float(float(ip['backSize'][0:-1]) / 1024), 2)) + 'G'
        if len(json.loads(db.get_one(['wan_ip'], "wan_ip='%s'" % str(ip['wan_ip']), 'backupServerMonitor'))) > 1:
            db.delete("wan_ip='%s'" % ip['wan_ip'], 'backupServerMonitor')
            db.create(ip, 'backupServerMonitor')
        elif len(json.loads(db.get_one(['wan_ip'], "wan_ip='%s'" % str(ip['wan_ip']), 'backupServerMonitor'))) == 1:
            db.update(ip, "wan_ip='%s'" % ip['wan_ip'], 'backupServerMonitor')
        elif len(json.loads(db.get_one(['wan_ip'], "wan_ip='%s'" % str(ip['wan_ip']), 'backupServerMonitor'))) == 0:
            db.create(ip, 'backupServerMonitor')


def server_status():
    collections = ('id','name','server','batt_t','match_t','enro_t','pvr_t','tran_t','ext_t','war_t','conf_t','start_batt','start_match',
                   'start_enro','start_pvr','start_state','start_trans','match_v','batt_v','pvr_v','state_v','trans_v','billingid')
    rt_list = db.get_list(collections, 'op_vertion')
    return rt_list

if __name__ == '__main__':
    mongo_monitor()