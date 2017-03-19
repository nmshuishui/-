#encoding:utf-8
#by 2016-09-26
from flask import render_template, request, session, send_file, send_from_directory, make_response
from login_require import login_required
from . import app
from login_require import login_required
import db
import json
import datetime,time
import csv
from StringIO import StringIO
from utils import util
import calendar

'''
    result['4399frame'] = frame_4399_list
    result['7k7kframe'] = frame_7k7k_list
    result['4399caton'] = caton_4399_list
    result['7k7kcaton'] = caton_7k7k_list
    result['4399mouse'] = mouse_4399_list
    result['7k7kmouse'] = mouse_7k7k_list
    result['4399memory'] = memory_4399_list
    result['7k7kmemory'] = memory_7k7k_list
    result['4399load'] = load_4399_list
    result['7k7kload'] = load_7k7k_list
    result['4399enter'] = enter_game_4399_list
    result['7k7kenter'] = enter_game_7k7k_list
'''

columns_day_column = ['qufu','platform','serverid','data_date','new_reg_user_num','login_user_num','user_login_num',
                   'pay_user_num','pay_num','pay_user_ARPU','avg_online','mountain_online','avg_online_ARPU',
                   'login_user_pay_trans_rate','new_reg_user_pay_transe_rate','pay_money','new_pay_user_num']
data_total_column = ['qufu','platform','serverid','data_date','new_reg_user_num','login_user_num','user_login_num',
                 'pay_user_num','pay_num','pay_user_ARPU','mountain_online','login_user_pay_trans_rate','total_reg_user_pay_transe_rate','pay_money']
yestoday = datetime.date.today() + datetime.timedelta(days=-1)


@app.route('/data_day/', methods=['GET'])
@login_required
def data_day():
    day = datetime.date.today() + datetime.timedelta(days=-1)
    if request.args.get('date'):
        date = request.args.get('date')
        platform = request.args.get('platform')
    else:
        date = day
        platform = 7
    where = "data_date=" + "'" + str(date) + "'" + ' and platform=' + str(platform) + ' order by qufu'
    datas = db.get_list(columns_day_column, 'data_day', where)
    return render_template('statistics/data_day.html', datas=datas, date=date, platform=platform)


@app.route('/data_download/')
@login_required
def data_download():
    columns_day_headers = ['区服','日期', '新增注册用户数', '登录用户数','用户登录次数','付费用户数', '付费次数',
                            '付费用户ARPU', '平均在线', '峰值在线','平均在线ARPU','登录用户付费转化率',
                            '新增注册用户付费转化率', '充值金额', '新增付费用户数']
    columns_day_download = ['qufu','data_date', 'new_reg_user_num', 'login_user_num','user_login_num','pay_user_num', 'pay_num',
                            'pay_user_ARPU', 'avg_online', 'mountain_online','avg_online_ARPU','login_user_pay_trans_rate',
                            'new_reg_user_pay_transe_rate', 'pay_money', 'new_pay_user_num']
    s = StringIO()
    s.write('\xEF\xBB\xBF')   #写入BOM，解决EXCEL中文显示乱码
    csv_writer = csv.writer(s)
    csv_writer.writerow(columns_day_headers)
    date = request.args.get('date')
    platform = request.args.get('platform')
    where = "data_date=" + "'" + str(date) + "'" + ' and platform=' + str(platform)
    datas = db.get_list(columns_day_column, 'data_day', where)
    for data in datas:
        data.pop('platform')
        data.pop('serverid')
        tmp_list = []
        [ tmp_list.append(data[x]) for x in columns_day_download ]
        csv_writer.writerow(tmp_list)
    cxt = s.getvalue()
    s.close()
    return cxt,200,{'Content-Type':'text/csv,charset=utf-8','Content-disposition':'attachment;filename=%s.csv' % (date)}
    # CSV文件用excel打开是乱码,从网页导出的CSV文件， 用Excel打开，中文会是乱码。 CSV文件乱码问题主要是文件编码引起的。
    # 临时解决(utf-8附件.csv): 右键编辑，用txt打开，另存为excel(下面的编码要选成UTF-8)，就可以看到正常的中文了


@app.route('/kai_gua_list/')
@login_required
def kai_gua():
    columns_gua_headers = [ '开挂时间', '大区', 'UID', '昵称', '封禁天数', '封禁原因' ]
    date = request.args.get('date')
    year = date[0:4]
    month = date[4:6]
    day = date[6:8]
    date = year + '_' + month + '_' + day
    table = 'cheat_log_' + date
    host_column = ['wan_ip']
    host_list = db.get_list(host_column, 'virtuals')
    hosts = []
    [ hosts.append(str(host['wan_ip'])) for host in host_list ]
    gua_column = ['platform_id', 'server_id', 'uid', 'nick_name', 'param']
    rows = []
    for host in hosts:
        try:
            gua_list = db.get_list(gua_column, table, where='reason=3', host=host, user='bhgame', passwd='cygamebh2014', db='bh_log')
        except BaseException,e:
            print e
        for data in gua_list:
            gua_lists = []
            param = data['param'].split('|')
            start_kaigua = time.localtime(float(param[8].split('=')[1].replace(',','')[:-3]))
            start_kaigua = time.strftime('%Y-%m-%d %H:%M:%S', start_kaigua)
            long_fengjin = float(param[10].split('=')[1].replace(',','')) / 60 / 24
            data['start_kaigua'] = start_kaigua
            data['long_fengjin'] = long_fengjin
            gua_lists.append(data['start_kaigua'])
            platform_id = data['platform_id']
            server_id = data['server_id']
            where = 'platform=' + str(platform_id) + ' and serverid=' + str(server_id)
            qufu = json.loads(db.get_one(['qufu'], where, 'virtuals'))['qufu']
            gua_lists.append(qufu)
            gua_lists.append(data['uid'])
            gua_lists.append(data['nick_name'])
            gua_lists.append(data['long_fengjin'])
            gua_lists.append('透视')
            rows.append(gua_lists)
    cxt = str(util.write_csv(columns_gua_headers, rows))
    return cxt,200,{'Content-Type':'text/csv,charset=utf-8','Content-disposition':'attachment;filename=%s.csv' % (date)}

    # 注释的部分是导出txt文件，但在导出的时候，总是502，需要多点几次按钮才会成功

    # date_month = date[0:6]
    # cmd1 = "salt -N 'groupall' cmd.run 'cat /data/logs/BattleServer/%s/%s/server.log*|grep low_low_low' > /tmp/gua.log1" % (date_month, date)
    # util.paramiko_command('tools.uc.ppweb.com.cn',cmd1)
    # cmd2 = "cat /tmp/gua.log1 |awk '{print $2,$4,$5,$6,$7}'|awk -F']' '{print $1,$3}' > /tmp/gua.log2"
    # util.paramiko_command('tools.uc.ppweb.com.cn',cmd2)
    # cmd3 = "awk '!a[$5]++' /tmp/gua.log2> /tmp/%s.txt" % date
    # util.paramiko_command('tools.uc.ppweb.com.cn',cmd3)
    #
    # util.paramiko_download('tools.uc.ppweb.com.cn','/tmp','/tmp', '%s-开挂列表.txt' % date)
    # strio = StringIO()
    # try:
    #     with open('/tmp/%s.txt' % date) as f:
    #         for i in f.readlines():
    #             strio.write(i)
    # except Exception,e:
    #     print e
    # strio.seek(0)
    # return send_file(strio,attachment_filename='%s-开挂列表.txt' % date,as_attachment=True)

@app.route('/data_week/')
@login_required
def data_week():
    day = datetime.date.today() + datetime.timedelta(days=-1)
    if request.args.get('date'):
        date = str(request.args.get('date'))
        platform = request.args.get('platform')

        dt = datetime.datetime.strptime(date, '%Y-%m-%d')
        start = (dt - datetime.timedelta(days=dt.weekday())) - datetime.timedelta(days=7)
        end = (start + datetime.timedelta(days=6))
        week_end = datetime.datetime.strftime(end, '%Y/%m/%d')
        day = week_end
        week_start = datetime.datetime.strftime(start, '%Y/%m/%d')
        week = []
        week.append(week_start)
        week.append(week_end)
        week_dates = '--'.join(week)
    else:
        date = day
        platform = 7

        today = datetime.datetime.today()
        start_delta = datetime.timedelta(days=today.weekday(), weeks=1)
        start_of_week = (today - start_delta)
        end_of_week = (start_of_week + datetime.timedelta(days=6))
        start_of_week = start_of_week.strftime('%Y/%m/%d')
        end_of_week = end_of_week.strftime('%Y/%m/%d')
        last_week = []
        last_week.append(start_of_week)
        last_week.append(end_of_week)
        week_dates = '--'.join(last_week)


    where = "data_date=" + "'" + str(day) + "'" + ' and platform=' + str(platform) + ' order by qufu'
    datas = db.get_list(columns_day_column, 'data_week', where)

    for data in datas:
        data['data_date'] = week_dates
    return render_template('statistics/data_week.html', datas=datas, date=date, platform=platform)


# 月统计是上个月一月的统计数据，查询方法就是查询月统计表中最后一天的数据即可
@app.route('/data_month/')
@login_required
def data_month():
    day = datetime.date.today() + datetime.timedelta(days=-1)
    today = datetime.date.today()
    firt_day = today.replace(day=1)
    lastMonth = (firt_day - datetime.timedelta(days=1)).strftime('%Y-%m')

    if request.args.get('date'):
        date = str(request.args.get('date'))
        year = date[0:4]
        month = date[5:7]
        platform = request.args.get('platform')
    else:
        date = lastMonth
        year = date[0:4]
        month = date[5:7]
        platform = 7

    last_day_month = calendar.monthrange(int(year), int(month))[1]
    where = "data_date=" + "'" + year + '-' + month + '-' + str(last_day_month) + "'" + ' and platform=' + str(platform) + ' order by qufu'
    datas = db.get_list(columns_day_column, 'data_month', where)

    if len(datas) == 0 and date == lastMonth:
        where = "data_date=" + "'" + str(day) + "'" + ' and platform=' + str(platform) + ' order by qufu'
        datas = db.get_list(columns_day_column, 'data_month', where)

    for data in datas:
        data['data_date'] = lastMonth
    return render_template('statistics/data_month.html', datas=datas, date=date, platform=platform)

@app.route('/data_total/')
@login_required
def data_total():
    day = datetime.date.today() + datetime.timedelta(days=-1)
    where = "data_date=" + "'" + str(day) + "'"
    datas = db.get_list(data_total_column, 'data_total', where)
    return render_template('statistics/data_total.html', datas=datas)

@app.route('/data_trend/')
@login_required
def data_trend():
    return render_template('statistics/data_trend.html')

@app.route('/data_trend/data/', methods=['POST','GET'])
@login_required
def data_trend_data():
    params = request.args if request.method == 'GET' else request.form
    platform = params.get('ptname','all')
    data_trend_column = ['data_date','sum(pay_money)']
    '''
    select data_date,sum(pay_money) from data_day where platform = 7 group by data_date  limit 1000;
    select data_date,sum(pay_money) from data_day where platform = 7 and DATE_SUB(CURDATE(), INTERVAL 30 DAY) <= data_date group by data_date;
    '''
    if platform == 'all':
        where = 'id > 0 group by data_date'
    else:
        where = 'platform = ' + str(platform) + ' group by data_date'
    dates = db.get_one(data_trend_column, where, 'data_day', list=True)
    data_day_money = []
    for x in dates:
        if platform == '13':
            data_day_money.append((int(time.mktime(x[0].timetuple()) * 1000),float(x[1]/10)))
        elif platform == '27':
            data_day_money.append((int(time.mktime(x[0].timetuple()) * 1000), float(x[1])/10))
        else:
            data_day_money.append((int(time.mktime(x[0].timetuple()) * 1000), float(x[1])/10))
    return json.dumps(data_day_money)

def stat_data_import(params):
    platform = params['platform']
    serverid = params['serverid']
    qufu_columns = ['qufu']
    date = params['date'].split(' ')[0]
    where = 'platform=' + platform + ' and ' + 'serverid=' + serverid
    try:
        qufu = json.loads(db.get_one(qufu_columns, where, 'virtuals'))['qufu']
    except Exception as e:
        print e
    columns_day = ['qufu','platform','serverid','data_date','new_reg_user_num','login_user_num','user_login_num',
                   'pay_user_num','pay_num','pay_user_ARPU','avg_online','mountain_online','avg_online_ARPU',
                   'login_user_pay_trans_rate','new_reg_user_pay_transe_rate','pay_money','new_pay_user_num']
    columns_total = ['qufu','platform','serverid','data_date','new_reg_user_num','login_user_num','user_login_num',
                     'pay_user_num','pay_num','pay_user_ARPU','mountain_online','login_user_pay_trans_rate','total_reg_user_pay_transe_rate','pay_money']
    value_day = []
    for x in qufu,platform,serverid,date:
        value_day.append(x)
    for y in params['data_day']:
        value_day.append(y)
    data=dict(zip(columns_day, value_day))
    data['pay_user_ARPU'] = round(data['pay_user_ARPU'], 2)
    data['avg_online'] = round(data['avg_online'], 2)
    data['avg_online_ARPU'] = round(data['avg_online_ARPU'], 2)
    data['login_user_pay_trans_rate'] = round(data['login_user_pay_trans_rate'], 2)
    data['new_reg_user_pay_transe_rate'] = round(data['new_reg_user_pay_transe_rate'], 2)
    where1 =  'platform=' + platform + ' and ' + 'serverid=' + serverid + ' and ' + "data_date='%s'" % date
    result = db.get_one(columns_day, where1, 'data_day', list=True)
    if len(result) > 0:
        db.update(data, where1, 'data_day')
    else:
        db.create(data, 'data_day')


    value_week = []
    for x in qufu,platform,serverid,date:
        value_week.append(x)
    for y in params['data_week']:
        value_week.append(y)
    data=dict(zip(columns_day, value_week))
    data['pay_user_ARPU'] = round(data['pay_user_ARPU'], 2)
    data['avg_online'] = round(data['avg_online'], 2)
    data['avg_online_ARPU'] = round(data['avg_online_ARPU'], 2)
    data['login_user_pay_trans_rate'] = round(data['login_user_pay_trans_rate'], 2)
    data['new_reg_user_pay_transe_rate'] = round(data['new_reg_user_pay_transe_rate'], 2)
    where1 =  'platform=' + platform + ' and ' + 'serverid=' + serverid + ' and ' + "data_date='%s'" % date
    result = db.get_one(columns_day, where1, 'data_week', list=True)
    if len(result) > 0:
        db.update(data, where1, 'data_week')
    else:
        db.create(data, 'data_week')


    value_month = []
    for x in qufu,platform,serverid,date:
        value_month.append(x)
    for y in params['data_month']:
        value_month.append(y)
    data=dict(zip(columns_day, value_month))
    data['pay_user_ARPU'] = round(data['pay_user_ARPU'], 2)
    data['avg_online'] = round(data['avg_online'], 2)
    data['avg_online_ARPU'] = round(data['avg_online_ARPU'], 2)
    data['login_user_pay_trans_rate'] = round(data['login_user_pay_trans_rate'], 2)
    data['new_reg_user_pay_transe_rate'] = round(data['new_reg_user_pay_transe_rate'], 2)
    where1 =  'platform=' + platform + ' and ' + 'serverid=' + serverid + ' and ' + "data_date='%s'" % date
    result = db.get_one(columns_day, where1, 'data_month', list=True)
    if len(result) > 0:
        db.update(data, where1, 'data_month')
    else:
        db.create(data, 'data_month')


    value_total = []
    for x in qufu,platform,serverid,date:
        value_total.append(x)
    for y in params['data_totol']:
        value_total.append(y)
    data=dict(zip(columns_total, value_total))
    data['pay_user_ARPU'] = round(data['pay_user_ARPU'], 2)
    data['login_user_pay_trans_rate'] = round(data['login_user_pay_trans_rate'], 2)
    data['total_reg_user_pay_transe_rate'] = round(data['total_reg_user_pay_transe_rate'], 2)
    where1 =  'platform=' + platform + ' and ' + 'serverid=' + serverid + ' and ' + "data_date='%s'" % date
    result = db.get_one(columns_total, where1, 'data_total', list=True)
    if len(result) > 0:
        db.update(data, where1, 'data_total')
    else:
        db.create(data, 'data_total')


def stat_import(params):

    frame_key = ('ptname','date','frame_49','frame_55','frame_60','frame_49_new','frame_55_new','frame_60_new')
    caton_key = ('ptname','date','caton_5','caton_15','caton_30','caton_50','caton_70','caton_95','caton_100','caton_5_new','caton_15_new','caton_30_new',
                 'caton_50_new','caton_70_new','caton_95_new','caton_100_new')
    load_key = ('ptname','date','load_config','load_res')
    mem_key = ('ptname','date','memory_500','memory_700','memory_900','memory_1100')
    mouse_key = ('ptname','date','mouse_20','mouse_30','mouse_50','mouse_75','mouse_20_new','mouse_30_new','mouse_50_new','mouse_75_new')
    enter_battle_key = ('ptname','date','success','battle_res_load','army_success','room_success','lobby_success','frist_root_success','frist_lobby_success',
                        'frist_battle_success','fighting_drop','frist_fighting_drop','ladder_drop','frist_ladder_drop','trans_drop','browser','ladder_match')

    for frame in params['4399frame'],params['7k7kframe']:
        db.create(dict(zip(frame_key,frame)),'battle_frame_rate')

    for caton in params['4399caton'],params['7k7kcaton']:
        db.create(dict(zip(caton_key,caton)),'game_kadun')

    for load in params['4399load'],params['7k7kload']:
        db.create(dict(zip(load_key,load)),'game_load')

    for mouse in params['4399mouse'],params['7k7kmouse']:
        db.create(dict(zip(mouse_key,mouse)),'game_mouse')

    for mem in params['4399memory'],params['7k7kmemory']:
        db.create(dict(zip(mem_key,mem)),'game_mem')

    for enter_battle in params['4399enter'],params['7k7kenter']:
        db.create(dict(zip(enter_battle_key,enter_battle)),'enter_battle')



def stat_export(collections,tablename,ptname,date):
    rt_list = db.get_one(['*'],"ptname = '%s' order by date" % ptname,tablename,list=True)
    rt = []
    for i in rt_list:
        rt.append(dict(zip(collections,i)))
    return rt

def stat_day_up_down(info,rt_dict):
    a = 0
    b = 0
    for x in range(len(rt_dict)):
        if info == 'frame':
            frame_60_day_tmp = rt_dict[x]['frame_60'] - a
            frame_60_day_new_tmp = rt_dict[x]['frame_60_new'] - b
            if x == 0:
                rt_dict[x]['frame_60_day'] = 0
                rt_dict[x]['frame_60_new_day'] = 0
            else:
                rt_dict[x]['frame_60_day'] = str(round(frame_60_day_tmp,2))+'%'+' <span class="jiantou_up">↑</span>' if round(frame_60_day_tmp,2) > 0 else str(round(frame_60_day_tmp,2))+'%'+' <span class="jiantou_down">↓</span>'
                rt_dict[x]['frame_60_new_day'] = str(round(frame_60_day_new_tmp,2))+'%'+' <span class="jiantou_up">↑</span>' if round(frame_60_day_new_tmp,2) > 0 else str(round(frame_60_day_new_tmp,2))+'%'+' <span class="jiantou_down">↓</span>'
            a = rt_dict[x]['frame_60']
            b = rt_dict[x]['frame_60_new']
        elif info == 'mouse':
            mouse_20_day_tmp = rt_dict[x]['mouse_20'] - a
            mouse_20_day_new_tmp = rt_dict[x]['mouse_20_new'] - b
            if x == 0 :
                rt_dict[x]['mouse_20_day'] = 0
                rt_dict[x]['mouse_20_new_day'] = 0
            else:
                rt_dict[x]['mouse_20_day'] = str(round(mouse_20_day_tmp,2))+'%'+' <span class="jiantou_up">↑</span>' if round(mouse_20_day_tmp,2) > 0 else str(round(mouse_20_day_tmp,2))+'%'+' <span class="jiantou_down">↓</span>'
                rt_dict[x]['mouse_20_new_day'] = str(round(mouse_20_day_new_tmp,2))+'% '+' <span class="jiantou_up">↑</span>' if round(mouse_20_day_new_tmp,2) > 0 else str(round(mouse_20_day_new_tmp,2))+'%'+' <span class="jiantou_down">↓</span>'
            a = rt_dict[x]['mouse_20']
            b = rt_dict[x]['mouse_20_new']
        elif info == 'load':
            load_config_day_tmp = rt_dict[x]['load_config'] - a
            load_res_day_tmp = rt_dict[x]['load_res'] - b
            if x == 0:
                rt_dict[x]['load_config_day'] = 0
                rt_dict[x]['load_res_day'] = 0
            else:
                rt_dict[x]['load_config_day'] = str(round(load_config_day_tmp,2))+'%'+' <span class="jiantou_up">↑</span>' if round(load_config_day_tmp,2) > 0 else str(round(load_config_day_tmp,2))+'%'+' <span class="jiantou_down">↓</span>'
                rt_dict[x]['load_res_day'] = str(round(load_res_day_tmp,2))+'%'+' <span class="jiantou_up">↑</span>' if round(load_res_day_tmp,2) > 0 else str(round(load_res_day_tmp,2))+'%'+' <span class="jiantou_down">↓</span>'
            a = rt_dict[x]['load_config']
            b = rt_dict[x]['load_res']
    return rt_dict

def stat_month_up_down(info,rt_dict):
    tmp_list = []
    for x in range(len(rt_dict)):
        if info == 'frame':
            tmp_list.append((rt_dict[x]['frame_60'],rt_dict[x]['frame_60_new']))
            if x > 30:
                a = round(rt_dict[x]['frame_60'] - tmp_list[x-30][0],2)
                b = round(rt_dict[x]['frame_60_new'] - tmp_list[x-30][1],2)
                rt_dict[x]['frame_60_month'] = str(a)+'%'+' <span class="jiantou_up">↑</span>' if a > 0 else str(a)+'%'+' <span class="jiantou_down">↓</span>'
                rt_dict[x]['frame_60_new_month'] = str(b)+'%'+' <span class="jiantou_up">↑</span>' if b > 0 else str(b)+'%'+' <span class="jiantou_down">↓</span>'
        elif info == 'mouse':
            tmp_list.append((rt_dict[x]['mouse_20'], rt_dict[x]['mouse_20_new']))
            if x > 30:
                a = round(rt_dict[x]['mouse_20'] - tmp_list[x - 30][0],2)
                b = round(rt_dict[x]['mouse_20_new'] - tmp_list[x - 30][1],2)
                rt_dict[x]['mouse_20_month'] = str(a)+'%'+' <span class="jiantou_up">↑</span>' if a > 0 else str(a)+'%'+' <span class="jiantou_down">↓</span>'
                rt_dict[x]['mouse_20_new_month'] = str(b)+'%'+' <span class="jiantou_up">↑</span>' if b > 0 else str(b)+'%'+' <span class="jiantou_down">↓</span>'
        elif info == 'load':
            tmp_list.append((rt_dict[x]['load_config'], rt_dict[x]['load_res']))
            if x > 30:
                a = round(rt_dict[x]['load_config'] - tmp_list[x - 30][0],2)
                b = round(rt_dict[x]['load_res'] - tmp_list[x - 30][1],2)
                rt_dict[x]['load_config_month'] = str(a)+'%'+' <span class="jiantou_up">↑</span>' if a > 0 else str(a)+'%'+' <span class="jiantou_down">↓</span>'
                rt_dict[x]['load_res_month'] = str(b)+'%'+' <span class="jiantou_up">↑</span>' if b > 0 else str(b)+'%'+' <span class="jiantou_down">↓</span>'
    return rt_dict

def stat_week_up_down(info,rt_dict):
    tmp_list = []
    for x in range(len(rt_dict)):
        if info == 'frame':
            tmp_list.append((rt_dict[x]['frame_60'], rt_dict[x]['frame_60_new']))
            if x > 6 :
                a = round(rt_dict[x]['frame_60'] - tmp_list[x - 7][0],2)
                b = round(rt_dict[x]['frame_60_new'] - tmp_list[x - 7][1],2)
                rt_dict[x]['frame_60_week'] = str(a)+'%'+' <span class="jiantou_up">↑</span>' if a > 0 else str(a)+'%'+' <span class="jiantou_down">↓</span>'
                rt_dict[x]['frame_60_new_week'] = str(b)+'%'+' <span class="jiantou_up">↑</span>' if b > 0 else str(b)+'%'+' <span class="jiantou_down">↓</span>'
        elif info == 'mouse':
            tmp_list.append((rt_dict[x]['mouse_20'], rt_dict[x]['mouse_20_new']))
            if x > 6:
                a = round(rt_dict[x]['mouse_20'] - tmp_list[x - 7][0],2)
                b = round(rt_dict[x]['mouse_20_new'] - tmp_list[x - 7][1],2)
                rt_dict[x]['mouse_20_week'] = str(a)+'%'+' <span class="jiantou_up">↑</span>' if a > 0 else str(a)+'%'+' <span class="jiantou_down">↓</span>'
                rt_dict[x]['mouse_20_new_week'] = str(b)+'%'+' <span class="jiantou_up">↑</span>' if b > 0 else str(b)+'%'+' <span class="jiantou_down">↓</span>'
        elif info == 'load':
            tmp_list.append((rt_dict[x]['load_config'], rt_dict[x]['load_res']))
            if x > 6:
                a = round(rt_dict[x]['load_config'] - tmp_list[x - 7][0],2)
                b = round(rt_dict[x]['load_res'] - tmp_list[x - 7][1],2)
                rt_dict[x]['load_config_week'] = str(a)+'%'+' <span class="jiantou_up">↑</span>' if a > 0 else str(a)+'%'+' <span class="jiantou_down">↓</span>'
                rt_dict[x]['load_res_week'] = str(b)+'%'+' <span class="jiantou_up">↑</span>' if b > 0 else str(b)+'%'+' <span class="jiantou_down">↓</span>'
    return rt_dict


@app.route('/battle_frame_rate/',methods=['POST','GET'])
@login_required
def battle_frame_rate():
    params = request.args if request.method == 'GET' else request.form
    ptname = params.get('ptname', '4399')
    collections = (
    'id', 'ptname', 'date', 'frame_49', 'frame_55', 'frame_60', 'frame_49_new', 'frame_55_new', 'frame_60_new')
    rt_dict = stat_export(collections, 'battle_frame_rate', ptname, '2016-09')
    for x in rt_dict:
        new_date = x['date'].strftime('%Y-%m-%d')
        x['date'] = new_date
    new_dict = stat_day_up_down('frame', rt_dict)
    new_dict = stat_week_up_down('frame', new_dict)
    new_dict = stat_month_up_down('frame', new_dict)
    return render_template('statistics/battle_frame_rate.html', frame_list=new_dict[::-1])


@app.route('/enter_battle/',methods=['POST','GET'])
@login_required
def enter_battle():
    params = request.args if request.method == 'GET' else request.form
    ptname = params.get('ptname', '4399')
    collections = (
        'id', 'ptname', 'date', 'success', 'battle_res_load', 'army_success', 'room_success', 'lobby_success',
        'frist_root_success', 'frist_lobby_success', 'frist_battle_success', 'fighting_drop' \
            , 'frist_fighting_drop', 'ladder_drop', 'frist_ladder_drop', 'trans_drop', 'browser', 'ladder_match')
    rt_dict = stat_export(collections, 'enter_battle', ptname, '2016-09')
    for x in rt_dict:
        new_date = x['date'].strftime('%Y-%m-%d')
        x['date'] = new_date
    return render_template('statistics/enter_battle.html', enter_list=rt_dict[::-1])


@app.route('/game_kadun/',methods=['POST','GET'])
@login_required
def game_kadun():
    params = request.args if request.method == 'GET' else request.form
    ptname = params.get('ptname', '4399')
    collections = (
        'id', 'ptname', 'date', 'caton_5', 'caton_15', 'caton_30', 'caton_50', 'caton_70',
        'caton_95', 'caton_100', 'caton_5_new', 'caton_15_new' \
            , 'caton_30_new', 'caton_50_new', 'caton_70_new', 'caton_95_new', 'caton_100_new')
    rt_dict = stat_export(collections, 'game_kadun', ptname, '2016-09')
    for x in rt_dict:
        new_date = x['date'].strftime('%Y-%m-%d')
        x['date'] = new_date
    return render_template('statistics/game_kadun.html', caton_list=rt_dict[::-1])

@app.route('/game_load/',methods=['POST','GET'])
@login_required
def game_load():
    params = request.args if request.method == 'GET' else request.form
    ptname = params.get('ptname', '4399')
    collections = (
        'id', 'ptname', 'date', 'load_config', 'load_res')
    rt_dict = stat_export(collections, 'game_load', ptname, '2016-09')
    for x in rt_dict:
        new_date = x['date'].strftime('%Y-%m-%d')
        x['date'] = new_date
    new_dict = stat_day_up_down('load', rt_dict)
    new_dict = stat_week_up_down('load', new_dict)
    new_dict = stat_month_up_down('load', new_dict)
    return render_template('statistics/game_load.html', load_list=new_dict[::-1])

@app.route('/game_mem/',methods=['POST','GET'])
@login_required
def game_mem():
    params = request.args if request.method == 'GET' else request.form
    ptname = params.get('ptname', '4399')
    collections = (
        'id', 'ptname', 'date', 'memory_500', 'memory_700', 'memory_900', 'memory_1100')
    rt_dict = stat_export(collections, 'game_mem', ptname, '2016-09')
    for x in rt_dict:
        new_date = x['date'].strftime('%Y-%m-%d')
        x['date'] = new_date
    return render_template('statistics/game_mem.html', memory_list=rt_dict[::-1])

@app.route('/game_mouse/',methods=['POST','GET'])
@login_required
def game_mouse():
    params = request.args if request.method == 'GET' else request.form
    ptname = params.get('ptname', '4399')
    collections = (
    'id', 'ptname', 'date', 'mouse_20', 'mouse_30', 'mouse_50', 'mouse_75', 'mouse_20_new', 'mouse_30_new',
    'mouse_50_new', 'mouse_75_new')
    rt_dict = stat_export(collections, 'game_mouse', ptname, '2016-09')
    for x in rt_dict:
        new_date = x['date'].strftime('%Y-%m-%d')
        x['date'] = new_date
    new_dict = stat_day_up_down('mouse', rt_dict)
    new_dict = stat_week_up_down('mouse', new_dict)
    new_dict = stat_month_up_down('mouse', new_dict)
    return render_template('statistics/game_mouse.html', mouse_list=new_dict[::-1])


# 帧率统计那些
@app.route('/statapi/',methods=['POST'])
def statapi():
    keys = 'c370af0f89fe66f06d1b70025d6a84c2'
    secrets = 'a458f162b35f53343750e885ea9b6f73'
    app_key = request.headers.get('App-Key')
    app_secret = request.headers.get('App-Secret')
    if app_key != keys and app_secret != secrets:
        return json.dumps({'code': 400, 'text': 'error app_key'})
    params = request.get_json()
    # print params
    stat_import(params)
    return json.dumps({'code': 200, 'text': 'success'})


# 用于接收每个服务器上的定时任务脚本 new_report_html.py的数据:游戏数据日统计,游戏数据周统计,游戏数据月统计,游戏数据累计统计
@app.route('/stat_data_api/',methods=['POST'])
def stat_data_api():
    keys = 'c370af0f89fe66f06d1b70025d6a84c2'
    secrets = 'a458f162b35f53343750e885ea9b6f73'
    app_key = request.headers.get('App-Key')
    app_secret = request.headers.get('App-Secret')
    if app_key != keys and app_secret != secrets:
        return json.dumps({'code': 400, 'text': 'error app_key'})
    params = request.get_json()
    stat_data_import(params)
    return json.dumps({'code': 200, 'text': 'success'})
