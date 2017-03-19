# coding: utf-8

from flask import render_template, request, session, redirect
from . import app
from login_require import login_required
import os, json
from utils.util import paramiko_command, WriteLog
import datetime
import db
import pysvn
import shutil
import subprocess

svnurl = 'https://svn.lieyan.com.cn/repos/ppweb/webp2p/flashp2p/operations/Script/python/cmdb'
svnSavePath = '/home/oop/projects/svnCode'
svnExportPath = '/home/oop/projects/svnExport'
svnRoolBackPath = '/home/oop/projects/svnRoolBack'

def getLogin(realm, username, may_save):
    retcode = True    #True，如果需要验证；否则用False
    username = 'yongwei.zhang'
    password = 'webp2p33'
    save = True    #True，如果想之后都不用验证；否则用False
    return retcode, username, password, save


@app.route('/code_release/', methods=['POST','GET'])
@login_required
def code_release():
    sql = "create table if not exists codePublish(" \
          "id int auto_increment PRIMARY key not null," \
          "version int(10) not null comment '代码版本号'," \
          "introduction varchar(100) not null comment '发布说明'," \
          "username varchar(20) not null comment '发布人'," \
          "date varchar(30) not null comment '发布日期') " \
          "ENGINE=InnoDB AUTO_INCREMENT=69 DEFAULT CHARSET=utf8 COMMENT='代码发布版本说明'"
    db.createTable(sql)
    columns = ['id', 'version', 'introduction', 'username', 'date']
    history = db.get_list(columns, 'codePublish order by id desc')
    username = session['username']
    date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if request.method == 'GET':
        return render_template('code/code_release.html', username=username, infos=history)
    elif request.method == 'POST':
        info = request.form.to_dict()
        if info['introduction'] == '':
            return json.dumps({'code': 1, 'errmsg': '必须填写发布说明'})
        client = pysvn.Client()
        client.callback_get_login = getLogin
        if os.path.exists(svnSavePath):
            client.update(svnSavePath)
        else:
            client.checkout(svnurl, svnSavePath)

        entry = client.info(svnSavePath)
        svnLastVersion = entry.commit_revision.number
        if os.path.exists(svnExportPath):
            # os.rmdir(svnSavePath) #只能删除空目录
            # os.removedirs(svnSavePath)
            shutil.rmtree(svnExportPath)
        client.export(svnurl, svnExportPath)
        data = dict({'version': svnLastVersion, 'introduction': info['introduction'], 'username': info['username'], 'date': date})

        # 需将此机器的公钥拷到tools.uc.ppweb.com.cn
        cmd = 'rsync -avzLPq --delete %s/* op@tools.uc.ppweb.com.cn:/data/oop/cmdb' % svnExportPath
        try:
            subprocess.check_call(cmd, shell=True)
            paramiko_command('tools.uc.ppweb.com.cn', 'cd /data/oop;bash run.sh')
            paramiko_command('tools.uc.ppweb.com.cn', "sed -i '/代码发布/d' /data/oop/cmdb/app/templates/base.html")
            db.create(data, 'codePublish')
        except Exception,e:
            print e
            return json.dumps({'code':1, 'errmsg': '代码发布失败:rsync传输失败'})

        return json.dumps({'code':0})


@app.route('/roolBack/', methods=['POST'])
@login_required
def roolBack():
    verId = request.form.get('verId')
    columns = ['version']
    where = 'id=%s' % verId
    version = json.loads(db.get_one(columns, where, 'codePublish'))['version']
    client = pysvn.Client()
    client.callback_get_login = getLogin
    if os.path.exists(svnRoolBackPath):
        shutil.rmtree(svnRoolBackPath)
    rv = pysvn.Revision(pysvn.opt_revision_kind.number, version)
    client.export(svnurl, svnRoolBackPath, revision=rv)
    date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    data = dict({'version': version, 'introduction': '回滚到版本', 'username': session['username'], 'date': date})
    db.create(data, 'codePublish')

    cmd = 'rsync -avzLPq --delete %s/* op@tools.uc.ppweb.com.cn:/data/oop/cmdb' % svnRoolBackPath
    subprocess.call(cmd, shell=True)
    paramiko_command('tools.uc.ppweb.com.cn', 'cd /data/oop;bash run.sh')
    paramiko_command('tools.uc.ppweb.com.cn', "sed -i '/代码发布/d' /data/oop/cmdb/app/templates/base.html")
    return json.dumps({'code': 0, 'errmsg': '回滚成功'})


@app.route('/upload/', methods=['POST'])
@login_required
def upload():
    files = request.files.get('files')
    filename =  files.filename
    if not filename:
        return redirect('/gm_update/')
    filepath = os.path.join('/home/op/gm_wars/', filename)
    files.save(filepath)

    cmd = 'cd /home/op/gm_wars/;./update_war.pl %s' % filename
    cmd_result = paramiko_command('tools.uc.ppweb.com.cn', cmd)
    WriteLog('infoLogger').info(cmd_result)
    if cmd_result != 1:
        status = 0
    else:
        status = 1

    update_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    username = session['username']
    info = dict({'filename': filename, 'update_time': update_time, 'status': status, 'username': username})
    db.create(info, 'gm_update')
    return redirect('/gm_update/')


@app.route('/gm_update/', methods=['POST','GET'])
@login_required
def gm_update():
    sql = "create table if not exists gm_update(" \
          "id int auto_increment PRIMARY key not null," \
          "filename varchar(50) not null comment '更新文件名'," \
          "update_time varchar(30) not null comment '更新时间'," \
          "status varchar(10) not null comment '更新状态'," \
          "username varchar(20) not null comment '更新操作人') " \
          "ENGINE=InnoDB AUTO_INCREMENT=69 DEFAULT CHARSET=utf8 COMMENT='GM更新说明表'"
    db.createTable(sql)
    columns = ['filename', 'update_time', 'status', 'username']
    history = db.get_list(columns, 'gm_update order by id desc limit 5')
    return render_template('code/gm_update.html', infos=history)