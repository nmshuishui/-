#coding: utf-8

import MySQLdb
from datetime import datetime
import hashlib
import json
salt='python'
from utils import util

def calc_md5(password):
    md5 = hashlib.md5()
    md5.update(password + 'salt')
    return md5.hexdigest()

def auth_user(username, password):
    sql = "select * from users where name='%s' and password='%s'" % (username, password)
    sql_count, rt_list = execute_sql(sql)
    if sql_count == 0:
        return False
    last_login = datetime.now()
    sql1 = "update users set last_time='%s' where name='%s'" % (last_login,username)
    execute_sql(sql1, fetch=False)
    return True


def user_list():
    columns = ('id', 'name', 'name_cn', 'password', 'email', 'mobile', 'role', 'status', 'create_time', 'last_time')
    sql = 'select %s from users' % ','.join(columns)
    sql_count, rt_list = execute_sql(sql)
    users = []
    for i in rt_list:
        users.append(dict(zip(columns, i)))
    return users


def user_regedit_check(user_data):
    for v in user_data.values():
        if v == '':
            error = {"status":1, "msg":"All msg can't be null"}
            return error
    if user_check(user_data['name']):
        error = {"status":1, "msg":'user %s exist' % (user_data['name'])}
        return error
    if user_data['password'] != user_data['repwd']:
        error = {"status":1, "msg":"password and repwd are not same"}
        return error
    error = {"status":0, "msg":'success'}
    return error


def user_check(name):
    sql = "select * from users where name='%s'" % (name)
    sql_cnt, rt_list = execute_sql(sql)
    if sql_cnt !=0:
        return True
    return False


def get_user_role(name):
    columns = ('id', 'name', 'name_cn', 'password', 'email', 'mobile', 'role', 'status', 'create_time', 'last_time')
    sql = "select %s from users where name='%s'" % (','.join(columns), name)
    sql_cnt, rt_list = execute_sql(sql)
    return dict(zip(columns,rt_list[0])).get('role','user')


def user_info(name):
    columns = ('id', 'name', 'name_cn', 'password', 'email', 'mobile', 'role', 'status', 'create_time', 'last_time')
    sql = "select %s from users where name='%s'" % (','.join(columns), name)
    sql_cnt, rt_list = execute_sql(sql)
    return dict(zip(columns,rt_list[0]))


def user_add(user_data):
    columns = ['name', 'password', 'name_cn', 'email', 'mobile', 'role', 'status', 'create_time', 'last_time']
    sql = "insert into users(%s) values(%s)" % (','.join(columns),','.join(['"%s"' % user_data[k] for k in columns]))
    execute_sql(sql, fetch=False)
    return True


def user_update(user_name, user_data):
    if len(user_data['mobile']) != 11:
        return {'code': 1, 'errmsg': '手机位数不正确'}
    data = ",".join(["%s='%s'" % (k, v) for k, v in user_data.items()])
    sql = "update users set %s where name='%s'" % (data, user_name)
    if execute_sql(sql, fetch=False):
        return {'code': 0, 'errmsg': '更新成功'}
    else:
        return {'code':1, 'errmsg':'更新失败'}



def user_update_oneself(user_name, user_data):
    if len(user_data['mobile']) != 11:
        return {'code': 1, 'errmsg': '手机位数不正确'}
    data = ",".join(["%s='%s'" % (k, v) for k, v in user_data.items()])
    sql = "update users set %s where name='%s'" % (data, user_name)
    if execute_sql(sql, fetch=False):
        return {'code': 0, 'errmsg': '更新成功'}
    else:
        return {'code':1, 'errmsg':'更新失败'}


def get_user_by_id(id):
    columns = ('id', 'name', 'name_cn', 'password', 'email', 'mobile', 'role', 'status', 'create_time', 'last_time')
    sql = 'select %s from users where id=%s' % (','.join(columns), id)
    sql_cnt, rt_list = execute_sql(sql)
    return dict(zip(columns,rt_list[0]))


def user_del(id):
    sql = 'delete from users where id=%s' % (id)
    sql_cnt, rt_list = execute_sql(sql, fetch=False)
    if sql_cnt != 0:
        return True
    return False

def change_pass_admin(name, new_pass):
    if new_pass == '':
        return {'code': 1, 'errmsg': '密码不能为空'}
    sql = "update users set password='%s' where name='%s'" % (calc_md5(new_pass), name)
    if execute_sql(sql, fetch=False):
        return {'code': 0, 'errmsg': '更新成功'}
    else:
        return {'code':1, 'errmsg':'更新失败'}


def change_pass(login_name, name,old_pass,new_pass):
    if old_pass == '' or new_pass == '':
        return {'code': 1, 'errmsg': '密码不能为空'}
    sql = "select password from users where name='%s'" % (name)
    sql_cnt, rt_list = execute_sql(sql)
    pass_in_db = ''.join(rt_list[0]).strip()
    if calc_md5(old_pass) != pass_in_db:
        return {'code': 1, 'errmsg': '原始密码输入错误'}
    sql = "update users set password='%s' where name='%s'" % (calc_md5(new_pass), name)
    if execute_sql(sql, fetch=False):
        return {'code': 0, 'errmsg': '更新成功'}
    else:
        return {'code':1, 'errmsg':'更新失败'}


def get_one(columns, where, table, list=False):
    sql = "select %s from %s where %s" % (",".join(columns), table ,where)
    rt_cnt,rt_list = execute_sql(sql, fetch=True)
    if list:
        return rt_list
    if len(rt_list) == 1:
        result = json.dumps(dict((columns[index],v) for index,v in enumerate(rt_list[0])), ensure_ascii=False)
    else:
        result = json.dumps(rt_list, ensure_ascii=False)
    return result


def get_list(columns, table, where=False, host=None, user=None, passwd=None, port=3306, db=None):
    columns = columns

    if where:
        sql = "select %s from %s where %s" % (",".join(columns), table, where)
    else:
        sql = "select %s from %s" % (",".join(columns), table)

    if host:
        sql_count, rt_list = execute_sql(sql, host, user, passwd, port, db)
    else:
        sql_count,rt_list = execute_sql(sql, fetch=True)

    result = [dict((columns[index],v) for index,v in enumerate(i)) for i in rt_list]
    return result


def create(data, table):
    columns, values = [],[]
    for k, v in data.items():
        columns.append(k)
        values.append("'%s'" % v)
        if v == '':
            return {'code':1, 'errmsg':'不能为空'}
    sql = "insert into %s (%s) values (%s)" % (table, ",".join(columns), ",".join(values))
    if execute_sql(sql, fetch=False):
        return {'code': 0, 'errmsg': '添加成功'}
    else:
        return {'code':1, 'errmsg':'添加失败'}


def delete(where, table):
    sql = "delete from %s where %s" % (table, where)
    if execute_sql(sql, fetch=False):
        return {'code': 0, 'errmsg': '修改成功'}
    else:
        return {'code':1, 'errmsg':'修改失败'}


def update(data, where, table):
    columns = ",".join([ "%s='%s'" % (k,v) for k,v in data.items() ])
    sql = "update %s set %s where %s" % (table, columns, where)
    if execute_sql(sql, fetch=False):
        return {'code': 0, 'errmsg': '修改成功'}
    else:
        return {'code':1, 'errmsg':'修改失败'}


def createTable(sql):
    # util.WriteLog('infoLogger').info(sql)
    if execute_sql(sql, fetch=False):
        return {'code': 0, 'errmsg': '创建成功'}
    else:
        return {'code':1, 'errmsg':'创建失败'}



def execute_sql(sql, host='10.0.12.254', user='root', passwd='root', port=3306, db='oop', fetch=True):
    conn = MySQLdb.connect(host=host, user=user, passwd=passwd, port=port, db=db, charset='utf8')
    cur = conn.cursor()
    sql_count = 0
    rt_list = []
    if fetch:
        sql_count = cur.execute(sql)
        rt_list = cur.fetchall()
    else:
        sql_count = cur.execute(sql)
        conn.commit()

    cur.close()
    conn.close()
    return sql_count, rt_list


if __name__ == '__main__':
    calc_md5('admin')
    a=["4399双线二", "7k7k双线一", "7k7k双线二"]
    print ",".join([ x for x in a ])


    print json.dumps(a, ensure_ascii=False)
