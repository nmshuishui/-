#coding: utf-8
from datetime import datetime
from flask import render_template, redirect, request, session
from . import app
from login_require import login_required
import db
import json
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from utils import util
from tasks import send_mail
#from flask_socketio import SocketIO, emit
# from flask.ext.login import current_user, logout_user


# app.secret_key=os.urandom(32)
app.secret_key='111'

@app.route('/')
def index():
    return redirect('/login/')


@app.route('/logout/')
def logout():
    util.WriteLog('infoLogger').info('%s logout' % (session['username']))
    session.clear()
    return redirect('/')


@app.route('/login/', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = db.calc_md5(request.form.get('password'))
        if db.auth_user(username, password):
            session['username'] = username
            session['role'] = db.get_user_role(username)
            util.WriteLog('infoLogger').info('%s is login' % (session['username']))
            return redirect('/user_center/')
        return render_template('login.html', errormsg='Account or passowrd error!')
    return render_template('login.html')


@app.route('/users/')
@login_required
def user_list():
    user_list = db.user_list()
    return render_template('users/users.html', users=user_list)

@app.route('/user_center/')
@login_required
def user_center():
    user = db.user_info(session.get('username'))
    return render_template('users/user_center.html', user=user)

@app.route('/users/regedit/')
@login_required
def user_regedit():
    user_login = {'user':session.get('username')}
    return render_template('users/user_create.html', session = user_login)


@app.route('/users/chpwdadmin/', methods=['POST'])
@login_required
def chpwdadmin():
    userinfo = request.form.to_dict()
    data = db.change_pass_admin(userinfo['username'], userinfo['newpasswd'])
    util.WriteLog('infoLogger').info('%s changed %s passowrd' % (session['username'], userinfo['username']))
    return json.dumps(data)

@app.route('/users/chpwdoneself/', methods=['POST'])
@login_required
def chpwdoneself():
    userinfo = request.form.to_dict()
    data = db.change_pass(session['username'],userinfo['username'], userinfo['oldpasswd'], userinfo['newpasswd'])
    user_email = json.loads(db.get_one(['email'], 'name="%s"' % session['username'], 'users'))['email']
    if data['code'] == 1:
        send_mail.delay([user_email], '个人密码修改失败', data['errmsg'])
    elif data['code'] == 0:
        send_mail.delay([user_email], '个人密码修改成功', data['errmsg'])
    util.WriteLog('infoLogger').info('%s changed his password' % (session['username']))
    return json.dumps(data)


@app.route('/users/add/', methods=['POST','GET'])
@login_required
def users_add():
    user_data = request.form.to_dict()
    user_data['create_time'] = datetime.now()
    user_data['last_time'] = datetime.now()
    user_data['password'] = db.calc_md5(user_data['password'])
    user_data['repwd'] = db.calc_md5(user_data['repwd'])
    error = db.user_regedit_check(user_data)
    if error['status'] == 0:
        db.user_add(user_data)
        util.WriteLog('infoLogger').warning('%s add user %s' % (session['username'], user_data['name']))
    return json.dumps(error)


@app.route('/users/update/', methods=['GET', 'POST'])
@login_required
def users_update():
    if request.method == 'GET':
        id = request.args.get('id')
        user = db.get_user_by_id(id)
        user.pop('create_time')
        user.pop('last_time')
        return json.dumps(dict(user))
    else:
        userinfo = request.form.to_dict()
        data = db.user_update(userinfo['name'], userinfo)
        util.WriteLog('infoLogger').info('%s changed userinfo %s' % (session['username'], userinfo['name']))
        return json.dumps(data)


@app.route('/users/updateoneself/', methods=['GET', 'POST'])
@login_required
def updateoneself():
    userinfo = request.form.to_dict()
    user_data = dict({'name_cn': userinfo['name_cn'], 'email':userinfo['email'], 'mobile': userinfo['mobile']})
    data = db.user_update_oneself(userinfo['name'], user_data)
    if data['code'] == 0:
        send_mail.delay(userinfo['email'], '个人资料修改成功', '您的个人资料已修改')
    elif data['code'] == 1:
        send_mail.delay(userinfo['email'], '个人资料修改失败', '您的个人资料修改失败')
    util.WriteLog('infoLogger').info('%s changed his userinfo' % (session['username']))
    return json.dumps(data)


@app.route('/users/delete/', methods=['GET'])
@login_required
def users_delete():
    id = request.args.get('id')
    columns=['id', 'name']
    where = "id=" + id
    user = db.get_one(columns,where,'users')
    if db.user_del(id):
        util.WriteLog('infoLogger').warning('%s delete user %s' % (session['username'], user['name']))
        return redirect('/users/')
    return 'del user failed!'