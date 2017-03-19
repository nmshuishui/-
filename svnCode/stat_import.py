#encoding:utf-8
#by 2016-09-26
import ordereddict
import pymongo
import datetime
import time
import requests
import json
import os
import logging
import traceback



def server_dict(ptname):
    if ptname == '4399':
    #4399平台
        server_4399 = ordereddict.OrderedDict()
        server_4399["3"] = {"Chinese":"4399双线1区", "English":"fps4.uc.ppweb.com.cn"}
        server_4399["10"] = {"Chinese": "4399双线2区", "English": "fps2.uc.ppweb.com.cn"}
        server_4399["18"] = {"Chinese": "4399双线3区", "English": "fps3.uc.ppweb.com.cn"}
        server_4399["2"] = {"Chinese": "4399联通1区", "English": "fps21.uc.ppweb.com.cn"}
        server_4399["5"] = {"Chinese": "4399联通2区", "English": "fps22.uc.ppweb.com.cn"}
        server_4399["7"] = {"Chinese": "4399联通3区", "English": "fps15.uc.ppweb.com.cn"}
        server_4399["11"] = {"Chinese": "4399联通4区", "English": "fps16.uc.ppweb.com.cn"}
        server_4399["12"] = {"Chinese": "4399联通5区", "English": "fps17.uc.ppweb.com.cn"}
        server_4399["15"] = {"Chinese": "4399联通6区", "English": "fps18.uc.ppweb.com.cn"}
        server_4399["20"] = {"Chinese": "4399联通7区", "English": "fps23.uc.ppweb.com.cn"}
        server_4399["22"] = {"Chinese": "4399联通8区", "English": "fps24.uc.ppweb.com.cn"}
        server_4399["25"] = {"Chinese": "4399联通9区", "English": "fps25.uc.ppweb.com.cn"}
        server_4399["1"] = {"Chinese": "4399电信1区", "English": "fps2.bd.ppweb.com.cn"}
        server_4399["4"] = {"Chinese": "4399电信2区", "English": "fps4.hy.ppweb.com.cn"}
        server_4399["6"] = {"Chinese": "4399电信3区", "English": "fps5.hy.ppweb.com.cn"}
        server_4399["8"] = {"Chinese": "4399电信4区", "English": "fps9.hy.ppweb.com.cn"}
        server_4399["9"] = {"Chinese": "4399电信5区", "English": "fps11.hy.ppweb.com.cn"}
        server_4399["13"] = {"Chinese": "4399电信6区", "English": "fps13.hy.ppweb.com.cn"}
        server_4399["14"] = {"Chinese": "4399电信7区", "English": "fps15.hy.ppweb.com.cn"}
        server_4399["16"] = {"Chinese": "4399电信8区", "English": "fps17.hy.ppweb.com.cn"}
        server_4399["17"] = {"Chinese": "4399电信9区", "English": "fps7.hy.ppweb.com.cn"}
        server_4399["19"] = {"Chinese": "4399电信10区", "English": "fps1.hy.ppweb.com.cn"}
        server_4399["21"] = {"Chinese": "4399电信11区", "English": "fps20.hy.ppweb.com.cn"}
        server_4399["23"] = {"Chinese": "4399电信12区", "English": "fps21.hy.ppweb.com.cn"}
        server_4399["24"] = {"Chinese": "4399电信13区", "English": "fps23.hy.ppweb.com.cn"}
        server_4399["26"] = {"Chinese": "4399电信14区", "English": "fps19.hy.ppweb.com.cn"}
        return server_4399

    elif ptname == '7k7k':
    #7k7k平台
        server_7k7k = ordereddict.OrderedDict()
        server_7k7k["1"] = {"Chinese": "7k7k双线1区", "English": "fps1.uc.ppweb.com.cn"}
        server_7k7k["32"] = {"Chinese": "7k7k双线2区", "English": "fps8.uc.ppweb.com.cn"}
        server_7k7k["33"] = {"Chinese": "7k7k双线3区", "English": "fps9.uc.ppweb.com.cn"}
        server_7k7k["38"] = {"Chinese": "7k7k双线7区", "English": "fps13.uc.ppweb.com.cn"}
        server_7k7k["39"] = {"Chinese": "7k7k双线8区", "English": "fps14.uc.ppweb.com.cn"}
        server_7k7k["5"] = {"Chinese": "7k7k联通1区", "English": "fps26.uc.ppweb.com.cn"}
        server_7k7k["11"] = {"Chinese": "7k7k电信6区", "English": "fps8.hy.ppweb.com.cn"}
        server_7k7k["12"] = {"Chinese": "7k7k电信7区", "English": "fps10.hy.ppweb.com.cn"}
        server_7k7k["3"] = {"Chinese": "7k7k电信1区", "English": "fps6.hy.ppweb.com.cn"}
        server_7k7k["19"] = {"Chinese": "7k7k电信12区", "English": "fps12.hy.ppweb.com.cn"}
        server_7k7k["22"] = {"Chinese": "7k7k电信15区", "English": "fps2.hy.ppweb.com.cn"}
        server_7k7k["25"] = {"Chinese": "7k7k电信18区", "English": "fps14.hy.ppweb.com.cn"}
        server_7k7k["28"] = {"Chinese": "7k7k电信21区", "English": "fps0.hy.ppweb.com.cn"}
        server_7k7k["29"] = {"Chinese": "7k7k电信22区", "English": "fps16.hy.ppweb.com.cn"}
        server_7k7k["30"] = {"Chinese": "7k7k电信23区", "English": "fps18.hy.ppweb.com.cn"}
        server_7k7k["31"] = {"Chinese": "7k7k电信24区", "English": "fps22.hy.ppweb.com.cn"}
        server_7k7k["34"] = {"Chinese": "7k7k电信25区", "English": "fps24.hy.ppweb.com.cn"}
        server_7k7k["35"] = {"Chinese": "7k7k电信26区", "English": "fps25.hy.ppweb.com.cn"}
        server_7k7k["36"] = {"Chinese": "7k7k电信27区", "English": "fps26.hy.ppweb.com.cn"}
        server_7k7k["37"] = {"Chinese": "7k7k电信28区", "English": "fps27.hy.ppweb.com.cn"}
        return server_7k7k
    else:
        return 'other error dict'

#向接口发送数据并入库
def send(msg):
    try:
        _reponse = requests.post(server_url,data=json.dumps(msg),headers={"Content-Type":"application/json",'app_key':App_key,'app_secret':App_secret})
        if not _reponse.ok:
            logger.error('Error Send Msg: %s',msg)
        else:
            _json = _reponse.json()
            if _json.get('code') != 200:
                logger.error('error send msg:%s ,result:%s',msg,_json)
    except BaseException as e:
        logger.error(traceback.format_exc())

#mongo# 数据库连接
def conn_mongo(ptname):
    client = pymongo.MongoClient('106.75.50.177',27017)
    db = client.datamine
    if ptname == '4399':
        coll = db.p4399v0224
    elif ptname == '7k7k':
        coll = db.p7k7kv0224
    else:
        print 'error db'
    return coll

#mysql数据库连接

#鼠标统计导入
def mouse_import(ptname,_server,collection,month,day,today):
    _totol_mouse = 0
    _totol_mouse_20 = 0
    _totol_mouse_30 = 0
    _totol_mouse_50 = 0
    _totol_mouse_75 = 0
    _totol_mouse_new = 0
    _totol_mouse_20_new = 0
    _totol_mouse_30_new = 0
    _totol_mouse_50_new = 0
    _totol_mouse_75_new = 0
    for server_id, server_name in _server.items():
        mouse_20 = {}
        cursor = collection.find({"_id": "1042"}, {server_id: 1, "_id": 0})
        for result_object in cursor:
            try:
                mouse_20[server_id] = result_object.get(server_id).get(str(month)).get(str(day), 0)
                _totol_mouse += mouse_20[server_id]
                _totol_mouse_20 += mouse_20[server_id]
            except BaseException as e:
                print '20---'
                print e
        mouse_30 = {}
        cursor = collection.find({"_id": "1043"}, {server_id: 1, "_id": 0})
        for result_object in cursor:
            try:
                mouse_30[server_id] = result_object.get(server_id).get(str(month)).get(str(day), 0)
                _totol_mouse += mouse_30[server_id]
                _totol_mouse_30 += mouse_30[server_id]
            except BaseException as e:
                print '30---'
                print e
        mouse_50 = {}
        cursor = collection.find({"_id": "1044"}, {server_id: 1, "_id": 0})
        for result_object in cursor:
            try:
                mouse_50[server_id] = result_object.get(server_id).get(str(month)).get(str(day), 0)
                _totol_mouse += mouse_50[server_id]
                _totol_mouse_50 += mouse_50[server_id]
            except BaseException as e:
                print '50---'
                print e
        mouse_75 = {}
        cursor = collection.find({"_id": "1045"}, {server_id: 1, "_id": 0})
        for result_object in cursor:
            try:
                mouse_75[server_id] = result_object.get(server_id).get(str(month)).get(str(day), 0)
                _totol_mouse += mouse_75[server_id]
                _totol_mouse_75 += mouse_75[server_id]
            except BaseException as e:
                print '75---'
                print e
        mouse_20_new = {}
        cursor = collection.find({"_id": "1088"}, {server_id: 1, "_id": 0})
        for result_object in cursor:
            try:
                mouse_20_new[server_id] = result_object.get(server_id).get(str(month)).get(str(day), 0)
                _totol_mouse_new += mouse_20_new[server_id]
                _totol_mouse_20_new += mouse_20_new[server_id]
            except BaseException as e:
                print 'new 20---'
                print e
        mouse_30_new = {}
        cursor = collection.find({"_id": "1089"}, {server_id: 1, "_id": 0})
        for result_object in cursor:
            try:
                mouse_30_new[server_id] = result_object.get(server_id).get(str(month)).get(str(day), 0)
                _totol_mouse_new += mouse_30_new[server_id]
                _totol_mouse_30_new += mouse_30_new[server_id]
            except BaseException as e:
                print 'new 30---'
                print e
        mouse_50_new = {}
        cursor = collection.find({"_id": "1090"}, {server_id: 1, "_id": 0})
        for result_object in cursor:
            try:
                mouse_50_new[server_id] = result_object.get(server_id).get(str(month)).get(str(day), 0)
                _totol_mouse_new += mouse_50_new[server_id]
                _totol_mouse_50_new += mouse_50_new[server_id]
            except BaseException as e:
                print 'new 50---'
                print e
        mouse_75_new = {}
        cursor = collection.find({"_id": "1091"}, {server_id: 1, "_id": 0})
        for result_object in cursor:
            try:
                mouse_75_new[server_id] = result_object.get(server_id).get(str(month)).get(str(day), 0)
                _totol_mouse_new += mouse_75_new[server_id]
                _totol_mouse_75_new += mouse_75_new[server_id]
            except BaseException as e:
                print 'new 75---'
                print e

    #Debug
    # print _totol_mouse
    # print _totol_mouse_20
    # print _totol_mouse_30
    # print _totol_mouse_50
    # print _totol_mouse_75
    # print _totol_mouse_new
    # print _totol_mouse_20_new
    # print _totol_mouse_30_new
    # print _totol_mouse_50_new
    # print _totol_mouse_75_new
    return [ptname,today.strftime('%Y-%m-%d'),round(_totol_mouse_20*100.0/_totol_mouse,2),round(_totol_mouse_30*100.0/_totol_mouse,2),round(_totol_mouse_50*100.0/_totol_mouse,2),round(_totol_mouse_75*100.0/_totol_mouse,2)
        , round(_totol_mouse_20_new * 100.0 / _totol_mouse_new, 2), round(_totol_mouse_30_new * 100.0 / _totol_mouse_new, 2), round(_totol_mouse_50_new * 100.0 / _totol_mouse_new, 2)
        , round(_totol_mouse_75_new * 100.0 / _totol_mouse_new, 2)]



#内存统计导入
def memory_import(ptname,_server,collection,month,day,today):
    _totol_memory = 0
    _totol_memory_500 = 0
    _totol_memory_700 = 0
    _totol_memory_900 = 0
    _totol_memory_1100 = 0
    for server_id, server_name in _server.items():
        memory_500 = {}
        cursor = collection.find({"_id": "1093"}, {server_id: 1, "_id": 0})
        for result_object in cursor:
            try:
                memory_500[server_id] = result_object.get(server_id).get(str(month)).get(str(day), 0)
                _totol_memory += memory_500[server_id]
                _totol_memory_500 += memory_500[server_id]
            except BaseException as e:
                print '500---'
                print e
        memory_700 = {}
        cursor = collection.find({"_id": "1094"}, {server_id: 1, "_id": 0})
        for result_object in cursor:
            try:
                memory_700[server_id] = result_object.get(server_id).get(str(month)).get(str(day), 0)
                _totol_memory += memory_700[server_id]
                _totol_memory_700 += memory_700[server_id]
            except BaseException as e:
                print '700---'
                print e
        memory_900 = {}
        cursor = collection.find({"_id": "1095"}, {server_id: 1, "_id": 0})
        for result_object in cursor:
            try:
                memory_900[server_id] = result_object.get(server_id).get(str(month)).get(str(day), 0)
                _totol_memory += memory_900[server_id]
                _totol_memory_900 += memory_900[server_id]
            except BaseException as e:
                print '900---'
                print e
        memory_1100 = {}
        cursor = collection.find({"_id": "1096"}, {server_id: 1, "_id": 0})
        for result_object in cursor:
            try:
                memory_1100[server_id] = result_object.get(server_id).get(str(month)).get(str(day), 0)
                _totol_memory += memory_1100[server_id]
                _totol_memory_1100 += memory_1100[server_id]
            except BaseException as e:
                print '1100---'
                print e
        memory_1300 = {}
        cursor = collection.find({"_id": "1097"}, {server_id: 1, "_id": 0})
        for result_object in cursor:
            try:
                memory_1300[server_id] = result_object.get(server_id).get(str(month)).get(str(day), 0)
                _totol_memory += memory_1300[server_id]
                _totol_memory_1100 += memory_1300[server_id]
            except BaseException as e:
                print '1300---'
                print e
        memory_1400 = {}
        cursor = collection.find({"_id": "1098"}, {server_id: 1, "_id": 0})
        for result_object in cursor:
            try:
                memory_1400[server_id] = result_object.get(server_id).get(str(month)).get(str(day), 0)
                _totol_memory += memory_1400[server_id]
                _totol_memory_1100 += memory_1400[server_id]
            except BaseException as e:
                print '1400---'
                print e
    #Debug
    # print _totol_memory
    # print _totol_memory_500
    # print _totol_memory_700
    # print _totol_memory_900
    # print _totol_memory_1000
    return [ptname,today.strftime('%Y-%m-%d'),round(_totol_memory_500*100.0/_totol_memory,2),round(_totol_memory_700*100.0/_totol_memory,2),round(_totol_memory_900*100.0/_totol_memory,2)
        , round(_totol_memory_1100*100.0/_totol_memory, 2)]

#卡顿比统计导入
def caton_import(ptname,_server,collection,month,day,today):
    _totol_caton = 0
    _totol_caton_5 = 0
    _totol_caton_15 = 0
    _totol_caton_30 = 0
    _totol_caton_50 = 0
    _totol_caton_70 = 0
    _totol_caton_95 = 0
    _totol_caton_100 = 0
    _totol_caton_new = 0
    _totol_caton_5_new = 0
    _totol_caton_15_new = 0
    _totol_caton_30_new = 0
    _totol_caton_50_new = 0
    _totol_caton_70_new = 0
    _totol_caton_95_new = 0
    _totol_caton_100_new = 0
    for server_id, server_name in _server.items():
        caton_5 = {}
        cursor = collection.find({"_id": "1200"}, {server_id: 1, "_id": 0})
        for result_object in cursor:
            try:
                caton_5[server_id] = result_object.get(server_id).get(str(month)).get(str(day), 0)
                _totol_caton += caton_5[server_id]
                _totol_caton_5 += caton_5[server_id]
            except BaseException as e:
                print '5---'
                print e

        caton_15 = {}
        cursor = collection.find({"_id": "1201"}, {server_id: 1, "_id": 0})
        for result_object in cursor:
            try:
                caton_15[server_id] = result_object.get(server_id).get(str(month)).get(str(day), 0)
                _totol_caton += caton_15[server_id]
                _totol_caton_15 += caton_15[server_id]
            except BaseException as e:
                print '15---'
                print e

        caton_30 = {}
        cursor = collection.find({"_id": "1202"}, {server_id: 1, "_id": 0})
        for result_object in cursor:
            try:
                caton_30[server_id] = result_object.get(server_id).get(str(month)).get(str(day), 0)
                _totol_caton += caton_30[server_id]
                _totol_caton_30 += caton_30[server_id]
            except BaseException as e:
                print '30---'
                print e

        caton_50 = {}
        cursor = collection.find({"_id": "1203"}, {server_id: 1, "_id": 0})
        for result_object in cursor:
            try:
                caton_50[server_id] = result_object.get(server_id).get(str(month)).get(str(day), 0)
                _totol_caton += caton_50[server_id]
                _totol_caton_50 += caton_50[server_id]
            except BaseException as e:
                print '50---'
                print e

        caton_70 = {}
        cursor = collection.find({"_id": "1204"}, {server_id: 1, "_id": 0})
        for result_object in cursor:
            try:
                caton_70[server_id] = result_object.get(server_id).get(str(month)).get(str(day), 0)
                _totol_caton += caton_70[server_id]
                _totol_caton_70 += caton_70[server_id]
            except BaseException as e:
                print '70---'
                print e

        caton_85 = {}
        cursor = collection.find({"_id": "1205"}, {server_id: 1, "_id": 0})
        for result_object in cursor:
            try:
                caton_85[server_id] = result_object.get(server_id).get(str(month)).get(str(day), 0)
                _totol_caton += caton_85[server_id]
                _totol_caton_70 += caton_85[server_id]
            except BaseException as e:
                print '85---'
                print e

        caton_95 = {}
        cursor = collection.find({"_id": "1206"}, {server_id: 1, "_id": 0})
        for result_object in cursor:
            try:
                caton_95[server_id] = result_object.get(server_id).get(str(month)).get(str(day), 0)
                _totol_caton += caton_95[server_id]
                _totol_caton_95 += caton_95[server_id]
            except BaseException as e:
                print '95---'
                print e

        caton_100 = {}
        cursor = collection.find({"_id": "1207"}, {server_id: 1, "_id": 0})
        for result_object in cursor:
            try:
                caton_100[server_id] = result_object.get(server_id).get(str(month)).get(str(day), 0)
                _totol_caton += caton_100[server_id]
                _totol_caton_100 += caton_100[server_id]
            except BaseException as e:
                print '100---'
                print e

        caton_5_new = {}
        cursor = collection.find({"_id": "1216"}, {server_id: 1, "_id": 0})
        for result_object in cursor:
            try:
                caton_5_new[server_id] = result_object.get(server_id).get(str(month)).get(str(day), 0)
                _totol_caton_new += caton_5_new[server_id]
                _totol_caton_5_new += caton_5_new[server_id]
            except BaseException as e:
                print 'new 5---'
                print e

        caton_15_new = {}
        cursor = collection.find({"_id": "1217"}, {server_id: 1, "_id": 0})
        for result_object in cursor:
            try:
                caton_15_new[server_id] = result_object.get(server_id).get(str(month)).get(str(day), 0)
                _totol_caton_new += caton_15_new[server_id]
                _totol_caton_15_new += caton_15_new[server_id]
            except BaseException as e:
                print 'new 15---'
                print e

        caton_30_new = {}
        cursor = collection.find({"_id": "1218"}, {server_id: 1, "_id": 0})
        for result_object in cursor:
            try:
                caton_30_new[server_id] = result_object.get(server_id).get(str(month)).get(str(day), 0)
                _totol_caton_new += caton_30_new[server_id]
                _totol_caton_30_new += caton_30_new[server_id]
            except BaseException as e:
                print 'new 30---'
                print e

        caton_50_new = {}
        cursor = collection.find({"_id": "1219"}, {server_id: 1, "_id": 0})
        for result_object in cursor:
            try:
                caton_50_new[server_id] = result_object.get(server_id).get(str(month)).get(str(day), 0)
                _totol_caton_new += caton_50_new[server_id]
                _totol_caton_50_new += caton_50_new[server_id]
            except BaseException as e:
                print 'new 50---'
                print e

        caton_70_new = {}
        cursor = collection.find({"_id": "1220"}, {server_id: 1, "_id": 0})
        for result_object in cursor:
            try:
                caton_70_new[server_id] = result_object.get(server_id).get(str(month)).get(str(day), 0)
                _totol_caton_new += caton_70_new[server_id]
                _totol_caton_70_new += caton_70_new[server_id]
            except BaseException as e:
                print 'new 70---'
                print e

        caton_85_new = {}
        cursor = collection.find({"_id": "1221"}, {server_id: 1, "_id": 0})
        for result_object in cursor:
            try:
                caton_85_new[server_id] = result_object.get(server_id).get(str(month)).get(str(day), 0)
                _totol_caton_new += caton_85_new[server_id]
                _totol_caton_70_new += caton_85_new[server_id]
            except BaseException as e:
                print 'new 85---'
                print e

        caton_95_new = {}
        cursor = collection.find({"_id": "1222"}, {server_id: 1, "_id": 0})
        for result_object in cursor:
            try:
                caton_95_new[server_id] = result_object.get(server_id).get(str(month)).get(str(day), 0)
                _totol_caton_new += caton_95_new[server_id]
                _totol_caton_95_new += caton_95_new[server_id]
            except BaseException as e:
                print 'new 95---'
                print e

        caton_100_new = {}
        cursor = collection.find({"_id": "1223"}, {server_id: 1, "_id": 0})
        for result_object in cursor:
            try:
                caton_100_new[server_id] = result_object.get(server_id).get(str(month)).get(str(day), 0)
                _totol_caton_new += caton_100_new[server_id]
                _totol_caton_100_new += caton_100_new[server_id]
            except BaseException as e:
                print 'new 100---'
                print e
    #Debug
    # print _totol_caton
    # print _totol_caton_5
    # print _totol_caton_15
    # print _totol_caton_30
    # print _totol_caton_50
    # print _totol_caton_70
    # print _totol_caton_95
    # print _totol_caton_100
    #
    # print _totol_caton_new
    # print _totol_caton_5_new
    # print _totol_caton_15_new
    # print _totol_caton_30_new
    # print _totol_caton_50_new
    # print _totol_caton_70_new
    # print _totol_caton_95_new
    # print _totol_caton_100_new
    if _totol_caton == 0:
        _totol_caton = 1
    if _totol_caton_new == 0:
        _totol_caton_new =1

    return [ptname,today.strftime('%Y-%m-%d'),round(_totol_caton_5*100.0/_totol_caton,2),round(_totol_caton_15*100.0/_totol_caton,2),round(_totol_caton_30*100.0/_totol_caton,2),round(_totol_caton_50*100.0/_totol_caton,2)
        , round(_totol_caton_70 * 100.0 / _totol_caton, 2),round(_totol_caton_95*100.0/_totol_caton,2),round(_totol_caton_100*100.0/_totol_caton,2),round(_totol_caton_5_new*100.0/_totol_caton_new,2)
        , round(_totol_caton_15_new * 100.0 / _totol_caton_new, 2),round(_totol_caton_30_new*100.0/_totol_caton_new,2),round(_totol_caton_50_new*100.0/_totol_caton_new,2)
        , round(_totol_caton_70_new * 100.0 / _totol_caton_new, 2),round(_totol_caton_95_new*100.0/_totol_caton_new,2),round(_totol_caton_100_new*100.0/_totol_caton_new,2)]


#游戏加载统计导入
def load_import(ptname,_server,collection,month,day,today):
    _totol_load = 0
    _totol_config_load = 0
    _totol_res_load = 0
    for server_id, server_name in _server.items():
        load = {}
        cursor = collection.find({"_id": "2006"}, {server_id: 1, "_id": 0})
        for i in cursor:
            try:
                load[server_id] = i[server_id][str(month)][str(day)]
                _totol_load += load[server_id]
            except BaseException as e:
                print e
        load_config = {}
        cursor = collection.find({"_id": "2007"}, {server_id: 1, "_id": 0})
        for i in cursor:
            try:
                load_config[server_id] = i[server_id][str(month)][str(day)]
                _totol_config_load += load_config[server_id]
            except BaseException as e:
                print e
        load_res = {}
        cursor = collection.find({"_id": "2008"}, {server_id: 1, "_id": 0})
        for i in cursor:
            try:
                load_res[server_id] = i[server_id][str(month)][str(day)]
                _totol_res_load += load_res[server_id]
            except BaseException as e:
                print e

    #Debug
    # print _totol_load
    # print _totol_config_load
    # print _totol_res_load

    return [ptname,today.strftime('%Y-%m-%d'),round(_totol_config_load*100.0/_totol_load,2),round(_totol_res_load*100.0/_totol_load,2)]

#进入战斗成功比例
def enter_game(ptname,collection,month,day,today):
    _totol_enter_game = [ptname,today.strftime('%Y-%m-%d')]
    ENTER_GAME_FIELD = {
        1: ["3031", "3033"],  # total game
        2: ["3038", "3039"],  # team
        3: ["3040", "3041"],  # enter room
        4: ["3042", "3043"],  # enter hall
        5: ["3044", "3045"],  # enter room first time
        6: ["3046", "3047"],  # enter hall first time
        7: ["3048", "3049"],  # enter battle first time
        8: ["3033", "3050"],  # battle lost connection
        9: ["3049", "3051"],  # battle lost connection first time
        10: ["3053", "3052"],  # ladder battle lost connection
        11: ["3055", "3054"],  # ladder battle lost connection first tim
        12: ["3033", "3056"],  # trans lost connection
        13: ["3033", "3057"],  # invalid speed lost connection
        14: ["3085", "3086"],  # invalid speed lost connection
        15: ["2200", "2201"],  # zhandou jiazai res
    }
    for _tp in [1,15]+range(2,15):
        cursor = collection.find({"_id": ENTER_GAME_FIELD[_tp][0]}, {"_id": 0})
        for result in cursor:
            try:
                battle_begin = result.get(str(month)).get(str(day),0)
            except BaseException as e:
                print "Error:battle_begin"
                print e
        cursor = collection.find({"_id": ENTER_GAME_FIELD[_tp][1]}, {"_id": 0})
        for result in cursor:
            try:
                player_enter = result.get(str(month)).get(str(day),0)
            except:
                print "Error:player_enter"
                print e
        if battle_begin == 0:
            proption = 0
        else:
            proption = round(player_enter * 100.0 / battle_begin,2)
        _totol_enter_game.append(proption)
    return _totol_enter_game

#帧率统计导入
def frame_import(ptname,_server,collection,month,day,today):
    _totol_frame = 0
    _totol_frame_49 = 0
    _totol_frame_55 = 0
    _totol_frame_60 = 0
    _totol_frame_new = 0
    _totol_frame_new_49 = 0
    _totol_frame_new_55 = 0
    _totol_frame_new_60 = 0
    for server_id,server_name in _server.items():
        #统计
        frame_25 = {}
        cursor = collection.find({"_id": "1009"}, {server_id:1, "_id": 0})
        for i in cursor:
            try:
                frame_25[server_id] = i[server_id][str(month)][str(day)]
                _totol_frame += frame_25[server_id]
                _totol_frame_49 += frame_25[server_id]
            except BaseException as e:
                print e

        frame_39 = {}
        cursor = collection.find({"_id": "1010"}, {server_id: 1, "_id": 0})
        for i in cursor:
            try:
                frame_39[server_id] = i[server_id][str(month)][str(day)]
                _totol_frame += frame_39[server_id]
                _totol_frame_49 += frame_39[server_id]
            except BaseException as e:
                print e

        frame_49 = {}
        cursor = collection.find({"_id": "1011"}, {server_id: 1, "_id": 0})
        for i in cursor:
            try:
                frame_49[server_id] = i[server_id][str(month)][str(day)]
                _totol_frame += frame_49[server_id]
                _totol_frame_49 += frame_49[server_id]
            except BaseException as e:
                print e

        frame_55 = {}
        cursor = collection.find({"_id": "1101"}, {server_id: 1, "_id": 0})
        for i in cursor:
            try:
                frame_55[server_id] = i[server_id][str(month)][str(day)]
                _totol_frame += frame_55[server_id]
                _totol_frame_55 += frame_55[server_id]
            except BaseException as e:
                print e

        frame_60 = {}
        cursor = collection.find({"_id": "1102"}, {server_id: 1, "_id": 0})
        for i in cursor:
            try:
                frame_60[server_id] = i[server_id][str(month)][str(day)]
                _totol_frame += frame_60[server_id]
                _totol_frame_60 += frame_60[server_id]
            except BaseException as e:
                print e

        #新手统计
        frame_new_25 = {}
        cursor = collection.find({"_id": "1084"}, {server_id: 1, "_id": 0})
        for i in cursor:
            try:
                frame_new_25[server_id] = i[server_id][str(month)][str(day)]
                _totol_frame_new += frame_new_25[server_id]
                _totol_frame_new_49 += frame_new_25[server_id]
            except BaseException as e:
                print e

        frame_new_39 = {}
        cursor = collection.find({"_id": "1085"}, {server_id: 1, "_id": 0})
        for i in cursor:
            try:
                frame_new_39[server_id] = i[server_id][str(month)][str(day)]
                _totol_frame_new += frame_new_39[server_id]
                _totol_frame_new_49 += frame_new_39[server_id]
            except BaseException as e:
                print e

        frame_new_49 = {}
        cursor = collection.find({"_id": "1086"}, {server_id: 1, "_id": 0})
        for i in cursor:
            try:
                frame_new_49[server_id] = i[server_id][str(month)][str(day)]
                _totol_frame_new += frame_new_49[server_id]
                _totol_frame_new_49 += frame_new_49[server_id]
            except BaseException as e:
                print e

        frame_new_55 = {}
        cursor = collection.find({"_id": "1099"}, {server_id: 1, "_id": 0})
        for i in cursor:
            try:
                frame_new_55[server_id] = i[server_id][str(month)][str(day)]
                _totol_frame_new += frame_new_55[server_id]
                _totol_frame_new_55 += frame_new_55[server_id]
            except BaseException as e:
                print e

        frame_new_60 = {}
        cursor = collection.find({"_id": "1100"}, {server_id: 1, "_id": 0})
        for i in cursor:
            try:
                frame_new_60[server_id] = i[server_id][str(month)][str(day)]
                _totol_frame_new += frame_new_60[server_id]
                _totol_frame_new_60 += frame_new_60[server_id]
            except BaseException as e:
                print e

    #debug
    # print _totol_frame
    # print _totol_frame_49
    # print _totol_frame_55
    # print _totol_frame_60
    # print _totol_frame_new
    # print _totol_frame_new_49
    # print _totol_frame_new_55
    # print _totol_frame_new_60
    # print '-------------end-------------'

    return [ptname,today.strftime('%Y-%m-%d'),round(_totol_frame_49*100.0/_totol_frame,2),round(_totol_frame_55*100.0/_totol_frame,2),round(_totol_frame_60*100.0/_totol_frame,2),round(_totol_frame_new_49*100.0/_totol_frame_new,2)
        , round(_totol_frame_new_55 * 100.0 / _totol_frame_new, 2),round(_totol_frame_new_60*100.0/_totol_frame_new,2)]

if __name__ == '__main__':
    logger = logging.getLogger(__name__)
    App_key = 'c370af0f89fe66f06d1b70025d6a84c2'
    App_secret = 'a458f162b35f53343750e885ea9b6f73'
    server_url = 'http://localhost:9898/statapi/'
    logging.basicConfig(Level=logging.DEBUG,
                        format="%(asctime)s %(name)s %(pathname)s %(levelname)s %(message)s",
                        filename='/tmp/stat_import.log')
    #注意这里定义的range(1,2),默认只读取一天,如需获取其他时间段,可修改2为指定的天数即可
    for x in range(1,2):
        year, month, day, hour, minutes = time.localtime(time.time() - 86400*x)[:5]
        today = datetime.date.today() - datetime.timedelta(days=1*x)
        #-----------------------------------
        frame_4399_list = frame_import('4399',server_dict('4399'),conn_mongo('4399'),month,day,today)
        # print frame_4399_list
        frame_7k7k_list = frame_import('7k7k',server_dict('7k7k'), conn_mongo('7k7k'), month, day, today)
        # print frame_7k7k_list
        # -----------------------------------
        caton_4399_list = caton_import('4399',server_dict('4399'),conn_mongo('4399'),month,day,today)
        # print caton_4399_list
        caton_7k7k_list = caton_import('7k7k',server_dict('7k7k'), conn_mongo('7k7k'), month, day, today)
        # print caton_7k7k_list
        # -----------------------------------
        mouse_4399_list = mouse_import('4399',server_dict('4399'),conn_mongo('4399'),month,day,today)
        # print mouse_4399_list
        mouse_7k7k_list = mouse_import('7k7k',server_dict('7k7k'),conn_mongo('7k7k'),month,day,today)
        # print mouse_7k7k_list
        # -----------------------------------
        memory_4399_list = memory_import('4399',server_dict('4399'),conn_mongo('4399'),month,day,today)
        # print memory_4399_list
        memory_7k7k_list = memory_import('7k7k',server_dict('7k7k'),conn_mongo('7k7k'),month,day,today)
        # print memory_7k7k_list
        # -----------------------------------
        load_4399_list = load_import('4399',server_dict('4399'),conn_mongo('4399'),month,day,today)
        # print load_4399_list
        load_7k7k_list = load_import('7k7k',server_dict('7k7k'),conn_mongo('7k7k'),month,day,today)
        # print load_7k7k_list
        # -----------------------------------
        enter_game_4399_list = enter_game('4399',conn_mongo('4399'),month,day,today)
        # print enter_game_4399_list
        enter_game_7k7k_list = enter_game('7k7k',conn_mongo('7k7k'),month,day,today)
        # print enter_game_7k7k_list
        result = {}
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
        # print result
        try:
            send(result)
            logger.debug(time.strftime('%Y-%m-%d %H:%M:%S'))
        except BaseException as e:
            logger.error(traceback.format_exc())










