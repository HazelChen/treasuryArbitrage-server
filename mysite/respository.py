__author__ = 'luck-mac'
# -*- coding: utf-8 -*-

#from django.http import HttpResponse
from django.shortcuts import render
import json
from django.http import HttpResponse
import time
import  models


def get_report(request):
    username = request.GET.get('username')
    reports = models.repertory()
    reports.uid = username
    reports = reports.get()
    return HttpResponse(json.dumps(reports))

def get_finance(request):
    username = request.GET.get('username')
    finance = models.finance()
    finance.uid = username
    # finance_list = finance.get()
    finance_list = finance.get()
    return  HttpResponse(json.dumps(finance_list))
    #return  HttpResponse(json.dumps([{'uid':'a'}]))


def trade(request):
    ret = models.ret()
    trade = models.repertory()
    trade.id = request.GET.get('Repo_Id')


    trade.sell()
    record = models.record()

    
    record.more_contract = trade.blank_contract
    record.blank_contract = trade.more_contract
    try :
        record.blank_price =  request.GET.get('blank_price')
        record.more_price = request.GET.get('more_price')
    except:
        return HttpResponse(json.dumps({"result":0}))

    record.time =  request.GET.get('time')
    record.hand = trade.hand
    record.bond = trade.bond
    record.state = 0
    record.uid = request.GET.get('username')
    record.add()

    finance = models.finance()
    finance.uid = record.uid



    last_finance = finance.getlast()[0]

    new_finance = models.finance()
    new_finance.uid = last_finance.uid
    new_finance.invest = last_finance.invest - trade.bond
    new_finance.total = last_finance.total + float(request.GET.get('profit'))
    new_finance.free = new_finance.total - new_finance.invest
    new_finance.time = trade.time
    new_finance.add()

    return HttpResponse(json.dumps({"result":1}))
