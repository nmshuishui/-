#encoding:utf-8

from flask import render_template, jsonify, request, session
from . import app
from login_require import login_required
import json
import datetime
import db


def get_idc_info_date(now_year):
    #now_year = datetime.datetime.now().strftime('%Y')
    # now_year = '2016'
    # _sql_all = 'select sum(combined) from idc_data where date like %s group by date order by date;'
    # _sql_alone = 'select date,idcname,combined from idc_data where date like %s order by date'
    # _args = (now_year+'%',)
    rt_list_all = db.get_one(['sum(combined)'],"date like '%s%s' group by date order by date" % (now_year,'%'),'idc_bill', list=True)
    rt_list = db.get_one(['date','idcname','combined'],"date like '%s%s' order by date" % (now_year,'%'),'idc_bill', list=True)
    '''
    计算每月总收入-------------
    '''
    rt = []
    for x in rt_list_all:
        rt.append(float(x[0]))
    all_date = []
    all_date.append({'data': rt ,'name': '总支出'})
    '''
    计算每个机房每个月的收入
    '''
    rs = []
    for x in rt_list:
        # print 'rs',rs
        # print 'x:',x
        if len(rs) != 0:
            for y in rs:
                # print 'y:',y
                if y['name'] == x[1]:
                    months = x[0].split('-')[1]
                    y['data'][int(months)-1] = (float(x[2]))
                    status = 0
                    break
                else:
                    status = 1
        else:
            status = 1
        if status == 1:
            rs.append({"name": x[1], 'data': [0] * 12})
            num = x[0].split('-')[1]
            rs[-1]['data'][int(num)-1] = float(x[2])
        # if status == 1:
        #     rs.append({"name": x[1], 'data': [0] * 12})


        # if len(rs) != 0:
        #     for y in rs:
        #         if y['name'] == x[1]:
        #             y['data'].append(float(x[2]))
        #             status = 0
        #             break
        #         else:
        #             status = 1
        # else:
        #     status = 1
        # if status == 1:
        #     rs.append({'name': x[1], 'data': [float(x[2])]})

    # 返回总支出和单机房月支持的列表
    return all_date + rs

def month_get():
    d = datetime.datetime.now()
    dayscount = datetime.timedelta(days=d.day)
    dayto = d - dayscount
    date_from = datetime.datetime(dayto.year, dayto.month, 1)
    # date_to = datetime.datetime(dayto.year, dayto.month, dayto.day, 23, 59, 59)
    return '-'.join(str(date_from).split('-')[:2])

def get_new_idcinfo(_local_date=month_get()):
    colloens = ('id', 'date', 'idcname', 'cabinet', 'cabinet_price','host_amount','bandwidth','bandwidth_price','bandwidth_amount','combined','status','info')
    # _sql  = 'select * from idc_data where date = %s'
    # _args = (_local_date,)
    rt = []
    rt_list = db.get_one(['*'],"date = '%s'" % (_local_date,),'idc_bill', list=True)
    for i in rt_list:
        rt.append(dict(zip(colloens,i)))
    return _local_date,rt

def add_new_before_select(params):
    idcname = params.get('idcname')
    date = params.get('date')
    # _sql = 'select * from idc_data where idcname = %s and date = %s'
    # _args = (idcname,date)
    rt_list = db.get_one(['*'],"idcname = '%s' and date = '%s'" % (idcname,date),'idc_bill', list=True)
    return True,'进行入库操作'

def add_new_idcinfo(params):
    new_params = {}
    new_params['idcname'] = params.get('idcname')
    new_params['date'] = params.get('date')
    new_params['cabinet'] = params.get('cabinet')
    new_params['cabinet_price'] = params.get('cabinet_price')
    new_params['host_amount'] = params.get('host_amount')
    new_params['bandwidth'] = params.get('bandwidth')
    new_params['bandwidth_price'] = params.get('bandwidth_price')
    new_params['bandwidth_amount'] = float(params.get('bandwidth')) * float(params.get('bandwidth_price'))
    new_params['combined'] = float(params.get('host_amount')) + float(new_params['bandwidth_amount'])
    new_params['status'] = params.get('status')
    new_params['info'] = params.get('info')

    # idcname =  params.get('idcname')
    # date = params.get('date')
    # cabinet = params.get('cabinet')
    # cabinet_price = params.get('cabinet_price')
    # host_amount = params.get('host_amount')
    # bandwidth = params.get('bandwidth')
    # bandwidth_price = params.get('bandwidth_price')
    # bandwidth_amount = float(bandwidth) * float(bandwidth_price)
    # combined = float(host_amount) + float(bandwidth_amount)
    # status = params.get('status')
    # info = params.get('info')
    # print date,idcname,cabinet,cabinet_price,host_amount,bandwidth,bandwidth_price,bandwidth_amount,combined,status,info
    # _sql = 'insert into idc_data(date,idcname,cabinet,cabinet_price,host_amount,bandwidth,bandwidth_price,bandwidth_amount,combined,status,info) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
    # _args = (date,idcname,cabinet,cabinet_price,host_amount,bandwidth,bandwidth_price,bandwidth_amount,combined,status,info)
    _sql_count,rt_list = db.create(new_params,'idc_bill')
    if _sql_count != 0:
        return True ,'添加成功'
    return False ,'添加失败'

def update_idcinfo(params):
    new_params = {}
    new_params = {}
    new_params['id'] = params.get('id')
    new_params['idcname'] = params.get('idcname')
    new_params['date'] = params.get('date')
    new_params['cabinet'] = params.get('cabinet')
    new_params['cabinet_price'] = params.get('cabinet_price')
    new_params['host_amount'] = params.get('host_amount')
    new_params['bandwidth'] = params.get('bandwidth')
    new_params['bandwidth_price'] = params.get('bandwidth_price')
    new_params['bandwidth_amount'] = float(params.get('bandwidth')) * float(params.get('bandwidth_price'))
    new_params['combined'] = float(params.get('host_amount')) + float(new_params['bandwidth_amount'])
    new_params['status'] = params.get('status')
    new_params['info'] = params.get('info')

    # id = params.get('id')
    # idcname = params.get('idcname')
    # date = params.get('date')
    # cabinet = params.get('cabinet')
    # cabinet_price = params.get('cabinet_price')
    # host_amount = params.get('host_amount')
    # bandwidth = params.get('bandwidth')
    # bandwidth_price = params.get('bandwidth_price')
    # bandwidth_amount = float(bandwidth) * float(bandwidth_price)
    # combined = float(host_amount) + float(bandwidth_amount)
    # status = params.get('status')
    # info = params.get('info')
    # _sql = 'update idc_data set date = %s, idcname = %s , cabinet = %s , cabinet_price = %s, host_amount = %s, ' \
    #        'bandwidth = %s, bandwidth_price = %s, bandwidth_amount = %s,combined = %s,status = %s,info = %s where id = %s'
    # _args = (date,idcname,cabinet,cabinet_price,host_amount,bandwidth,bandwidth_price,bandwidth_amount,combined,status,info,id)
    # _sql_count, rt_list = SQL.excute_sql(_sql, _args, fetch=False)
    _sql_count, rt_list = db.update(new_params,'id = %s' % new_params['id'],'idc_bill')
    if _sql_count != 0:
        return True ,'更新成功'
    return False ,'更新失败'

def delete_idcinfo(params):
    id = params.get('id')
    idcname = params.get('idcname')
    date = params.get('date')
    # _sql = 'delete from idc_data where id = %s and date = %s and idcname = %s'
    # _args = (id,date,idcname)
    _sql_count, rt_list = db.delete("id = '%s' and date = '%s' and idcname = '%s'" % (id,date,idcname) ,'idc_bill')
    if _sql_count != 0:
        return True, '删除成功'
    return False, '删除失败'


@app.route('/idc_trend/', methods=['POST', 'GET'])
@login_required
def idc_trend():
    params = request.args if request.method == 'GET' else request.form
    now_year = params.get('years')
    if now_year is None:
        now_year = datetime.datetime.now().strftime('%Y')
    return render_template('cost/idc_trend.html',years=now_year)

@app.route('/idc_trend/data/', methods= ['POST', 'GET'])
@login_required
def idc_trend_data():
    params = request.args if request.method == 'GET' else request.form
    now_year = params.get('dates')
    if not now_year:
        now_year = datetime.datetime.now().strftime('%Y')
    all_data = get_idc_info_date(now_year)
    return jsonify(all_data=all_data)

@app.route('/idc_bill/', methods=['POST', 'GET'])
@login_required
def idc_bill():
    params = request.args if request.method == 'GET' else request.form
    date = params.get('dates')
    if not date:
        dates, access_list = get_new_idcinfo()
    else:
        dates, access_list = get_new_idcinfo(_local_date=date)
    all_combined = 0
    for i in access_list:
        all_combined += i.get('combined')
    return render_template('cost/idc_bill.html', idc_list=access_list, all_combined=all_combined, dates=dates)

@app.route('/idc_bill/add/', methods=['POST', 'GET'])
@login_required
def idc_bill_add():
    params = request.args if request.method == 'GET' else request.form
    _is_ok, _error = add_new_before_select(params)
    if not _is_ok:
        return jsonify({'is_ok': _is_ok, 'error': _error})
    _is_ok, _error = add_new_idcinfo(params)
    return jsonify({'is_ok': _is_ok, 'error': _error})

@app.route('/idc_bill/delete/', methods=['POST', 'GET'])
@login_required
def idc_bill_delete():
    params = request.args if request.method == 'GET' else request.form
    _is_ok, _error = delete_idcinfo(params)
    return jsonify({'is_ok': _is_ok, 'error': _error})

@app.route('/idc_bill/update/', methods=['POST', 'GET'])
@login_required
def idc_bill_update():
    params = request.args if request.method == 'GET' else request.form
    _is_ok, _error = update_idcinfo(params)
    return jsonify({'is_ok': _is_ok, 'error': _error})

