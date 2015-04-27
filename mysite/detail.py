
# -*- coding: utf-8 -*-

from django.shortcuts import render
import json
from django.http import HttpResponse
# from WindPy import w
import random
import models
import MySQLdb
import sys
sys.path.append("..")
import sae.const



import time


def get_id2(h ,m, s,code):
    db = MySQLdb.connect(user= sae.const.MYSQL_USER , db= sae.const.MYSQL_DB, passwd=sae.const.MYSQL_PASS , host=sae.const.MYSQL_HOST , port = sae.const.MYSQL_PORT)
    cursor = db.cursor()
    cursor.execute('select ID from '+ code +" where time = '" + "%02.d:%02.d:%02.d" % (h , m ,s) +"'")
    id = 0;
    result = cursor.fetchall();
    if ( len(result) >=1):
        id = int(result[0][0])
    else:
        if ( s > 0  ):
            id =  get_id2( h , m , s -1 , code)
        elif( m > 0 ):
            id =  get_id2( h , m -1 , s+59 , code)
        else :
            id =  get_id2( h - 1 , m+ 59 , s + 59 , code)
    return id;

def get_id( code ):
    h = int(time.strftime('%H',time.localtime(time.time())))
    m = int(time.strftime('%M',time.localtime(time.time())))
    s = int(time.strftime('%S',time.localtime(time.time())))
    

    t =  3600 * h + 60 * m + s

    low = 3600 * 9 + 60 * 15
    low2 = 3600 * 11 + 60 * 30

    high1 = 3600 * 13
    high = 3600 * 15 + 60 * 15

    id = 0
    if ( t <=  low ):
        id = -1
    elif ( t >= high ):
        db = MySQLdb.connect(user= sae.const.MYSQL_USER , db= sae.const.MYSQL_DB, passwd=sae.const.MYSQL_PASS , host=sae.const.MYSQL_HOST , port = sae.const.MYSQL_PORT)
        cursor = db.cursor()
        cursor.execute('select count(*) from '+ code +' where ID < 10000')
        id = int(cursor.fetchall()[0][0])
        cursor.close()
        db.close();
    elif ( t >= low2 and t <= high1 ):
        id = get_id2(11 , 30 ,0 , code )
    else:
        id = get_id2(h , m , s , code)
    
    return id

   

def get(request):
	# return HttpResponse(json.dumps(
 #        [{"RT_BID1": 93.44800000000001, "RT_AMT": 625934740.0, "RT_LAST_AMT": 1868960.0, "RT_DATE": 20140912.0, "RT_PRE_OI": 10390.0, "RT_OI": 10453.0, "RT_BSIZE1": 1.0, "RT_LOW_LIMIT": 0.0, "RT_ASK1": 93.45, "RT_ASIZE1": 11.0, "RT_OI_CHG": 63.0, "RT_LAST_VOL": 2.0, "RT_TURN": 0.0, "RT_HIGH": 93.46000000000001, "RT_UPWARD_VOL": 308.0, "RT_VOL_RATIO": 0.0, "RT_LAST": 93.44800000000001*(1+random.random()*0.1), "RT_LOW": 93.372, "RT_HIGH_LIMIT": 0.0, "RT_PRE_SETTLE": 93.42, "RT_LATEST": 93.44800000000001, "RT_DOWNWARD_VOL": 362.0, "RT_PRE_CLOSE": 93.406, "RT_OPEN": 93.404, "RT_CODE": "TF1412", "RT_VOL": 670.0, "RT_CHG": 0.028, "RT_SETTLE": 93.422, "RT_TIME": 162635.0, "RT_VWAP": 93.4231, "RT_SWING": 0.0009000000000000001, "RT_PCT_CHG": 0.00030000000000000003},
 #        {"RT_BID1": 93.858, "RT_AMT": 2815340.0, "RT_LAST_AMT": 938200.0, "RT_DATE": 20140912.0, "RT_PRE_OI": 55.0, "RT_OI": 54.0, "RT_BSIZE1": 1.0, "RT_LOW_LIMIT": 0.0, "RT_ASK1": 93.872, "RT_ASIZE1": 1.0, "RT_OI_CHG": -1.0, "RT_LAST_VOL": 1.0, "RT_TURN": 0.0, "RT_HIGH": 93.86, "RT_UPWARD_VOL": 1.0, "RT_VOL_RATIO": 0.0, "RT_LAST": 93.82000000000001*(1+random.random()*0.1), "RT_LOW": 93.82000000000001, "RT_HIGH_LIMIT": 0.0, "RT_PRE_SETTLE": 93.85000000000001, "RT_LATEST": 93.82000000000001, "RT_DOWNWARD_VOL": 2.0, "RT_PRE_CLOSE": 93.85000000000001, "RT_OPEN": 93.86, "RT_CODE": "TF1503", "RT_VOL": 3.0, "RT_CHG": -0.03, "RT_SETTLE": 93.82000000000001, "RT_TIME": 162635.0, "RT_VWAP": 93.8447, "RT_SWING": 0.0004, "RT_PCT_CHG": -0.00030000000000000003},
 #        {"RT_BID1": 0.0, "RT_AMT": 0.0, "RT_LAST_AMT": 0.0, "RT_DATE": 0.0, "RT_PRE_OI": 0.0, "RT_OI": 0.0, "RT_BSIZE1": 0.0, "RT_LOW_LIMIT": 0.0, "RT_ASK1": 0.0, "RT_ASIZE1": 0.0, "RT_OI_CHG": 0.0, "RT_LAST_VOL": 0.0, "RT_TURN": 0.0, "RT_HIGH": 0.0, "RT_UPWARD_VOL": 0.0, "RT_VOL_RATIO": 0.0, "RT_LAST": 0.0, "RT_LOW": 0.0, "RT_HIGH_LIMIT": 0.0, "RT_PRE_SETTLE": 0.0, "RT_LATEST": 0.0, "RT_DOWNWARD_VOL": 0.0, "RT_PRE_CLOSE": 0.0, "RT_OPEN": 0.0, "RT_CODE": "TF1506", "RT_VOL": 0.0, "RT_CHG": 0.0, "RT_SETTLE": 0.0, "RT_TIME": 0.0, "RT_VWAP": 0.0, "RT_SWING": 0.0, "RT_PCT_CHG": 0.0}]))
    
    db = MySQLdb.connect(user= sae.const.MYSQL_USER , db= sae.const.MYSQL_DB, passwd=sae.const.MYSQL_PASS , host=sae.const.MYSQL_HOST , port = sae.const.MYSQL_PORT)
    ####
    # cursor = db.cursor();
    # cursor.execute("select value from ids where name = 'id'");
    # id = int(cursor.fetchall()[0][0]);
    # cursor.execute("update ids set value = %d where name = 'id'" % ((id +1 )%3000) );
    # cursor.close();


    ####
    return_list = []
    codelist = ["TF1412","TF1503","TF1506"];
    i = 0;
    for code in codelist:
        cursor = db.cursor()

        id = get_id(code);
        if (id < 0):
            id = 1
        cursor.execute('select * from '+ code +' where ID = %d'%id)
        results = cursor.fetchall()
        result = results[0];

        h = int(time.strftime('%H',time.localtime(time.time())))
        m = int(time.strftime('%M',time.localtime(time.time())))
        s = int(time.strftime('%S',time.localtime(time.time())))
        

        return_list.append( {
            "MT_T":"%02.d:%02.d:%02.d" % (h , m ,s),
            "ID":id,
            "RT_CODE":result[0],
            "RT_DATE":result[1],
            "RT_LAST":result[2],
            "RT_CHG":result[3],
            "RT_PCT_CHG":result[4],
            "RT_BSIZE1":result[5],
            "RT_BID1":result[6],
            "RT_ASK1":result[7],
            "RT_ASIZE1":result[8],
            "RT_VOL":result[9], #成交量
            "RT_OI":result[10],#持仓量
            "RT_PRE_SETTLE":result[11],#前结算价
            "RT_OPEN":result[12],#今开
            "RT_HIGH":result[13],#最高
            "RT_LOW":result[14],#最低
            "RT_OI_CHG":result[15],#日增仓
            "RT_TIME":result[16],#时间
            "RT_PRE_CLOSE":result[17],#昨收
            "RT_SWING":result[18],#振幅
            "RT_AMT":result[19],#金额
            "RT_VWAP":result[20],#均价
            "RT_PRE_OI":result[21],#昨持仓
            "RT_HIGH_LIMIT":result[22],#涨停
            "RT_LOW_LIMIT":result[23]#跌停
                            }
                                );
        cursor.close();
    db.close()
    return HttpResponse(json.dumps(return_list));


def news(request):
    news_list = models.news().get()
    return HttpResponse(json.dumps(news_list,ensure_ascii=False))


def old(request):
    code = request.GET.get('CODE')
    db = MySQLdb.connect(user= sae.const.MYSQL_USER , db= sae.const.MYSQL_DB_2, passwd=sae.const.MYSQL_PASS , host=sae.const.MYSQL_HOST , port = sae.const.MYSQL_PORT)
    ####
    # id = int(cursor.fetchall()[0][0])
   
    
    
    ####
    return_list = []
   

    cursor = db.cursor()
    cursor.execute('select * from '+ code+ ' where TradingDay=' + time.strftime('%Y%m%d',time.localtime(time.time())) )
    
    results = cursor.fetchall()
    for result in results:
        return_list.append( {  
            # 'TradingDay':result[0],
            # 'InstrumentID':result[1],
            'LastPrice':result[4],
            # 'PreSettlementPrice':result[5],
            # 'PreClosePrice':result[6],
            # 'PreOpenInterest':result[7],
            # 'OpenPrice':result[8],
            # 'HighestPrice':result[9],
            # 'LowestPrice':result[10],
            # 'Volume':result[11],
            # 'Turnover':result[12],
            # 'OpenInterest':result[13],
            # 'ClosePrice':result[14],
            # 'SettlementPrice':result[15],
            # 'UpperLimitPrice':result[16],
            # 'LowerLimitPrice':result[17],
            # 'PreDelta':result[18],
            # 'CurrDelta':result[19],
            'Updatetime':result[20],
            # 'BidPrice1':result[22],
            # 'BidVolume1':result[23],
            # 'AskPrice1':result[24],
            # 'AskVolume1':result[25],

            # 'BidPrice2':result[26],
            # 'BidVolume2':result[27],
            # 'AskPrice2':result[28],
            # 'AskVolume2':result[29],

            # 'BidPrice3':result[30],
            # 'BidVolume3':result[31],
            # 'AskPrice3':result[32],
            # 'AskVolume3':result[33],

            # 'BidPrice4':result[34],
            # 'BidVolume4':result[35],
            # 'AskPrice4':result[36],
            # 'AskVolume4':result[37],

            # 'BidPrice5':result[38],
            # 'BidVolume5':result[39],
            # 'AskPrice5':result[40],
            # 'AskVolume5':result[41],

            # 'AveragePrice':result[42],

                            }
                                );
    cursor.close();
    db.close()
    return HttpResponse(json.dumps(return_list));
