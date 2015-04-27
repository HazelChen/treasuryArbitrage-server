# -*- coding: utf-8 -*-

#from django.http import HttpResponse
from django.shortcuts import render
import json
from django.http import HttpResponse
import models
import time

def register(request):
    u = models.user()
    u.username = request.GET.get('username')
    u.password = request.GET.get('password')
    u.add()
    return HttpResponse(u.parse())



def changePaswd(request):
    u = models.user()
    r = models.ret()
    u.username = request.GET.get('username')
    u.password = request.GET.get('oldPassword')

    if u.check()==1:
        u.password = request.GET.get('newPassword')
        u.update()
        r.result = 1
    else :
        r.result = 0
    return HttpResponse(r.parse())



def login(request):
    r = models.ret()
    u = models.user()
    u.username = request.GET.get('username')
    u.password = request.GET.get('password')
    r.result = u.check()
    return HttpResponse(r.parse())

def logout(request):
    r = models.ret();
    return HttpResponse(r.parse());


def history(request):
    username = request.GET.get('username')
    record = models.record()
    record.uid =  username
    records = record.get()
    return HttpResponse(json.dumps(records))

def order(request):
    record = models.record()
    trade = models.repertory()
    trade.uid = request.GET.get('username')
    trade.blank_contract = request.GET.get('blank_contract')
    trade.more_contract = request.GET.get('more_contract')
    trade.hand = request.GET.get('hand')
    trade.more_price = request.GET.get('more_price')
    trade.blank_price = request.GET.get('blank_price')
    trade.bond = float(request.GET.get('bond'))
    trade.time = request.GET.get('time')
    trade.add()


    record.more_contract = trade.more_contract
    record.blank_contract = trade.blank_contract
    record.blank_price = trade.blank_price
    record.more_price = trade.more_price
    record.time = trade.time
    record.hand = trade.hand
    record.bond = trade.bond
    record.state = 0
    record.uid = trade.uid
    record.add()

    finance = models.finance()
    finance.uid = request.GET.get('username')




    
    last_finance = finance.getlast()[0]
	
   
    
    new_finance = models.finance()
    new_finance.uid = last_finance.uid
    new_finance.invest = last_finance.invest + trade.bond
    new_finance.total = last_finance.total
    new_finance.free = new_finance.total - new_finance.invest
    new_finance.time = trade.time
    new_finance.add()
    return HttpResponse(json.dumps({'result':1}))


def cancelOrder(request):
    id = int(request.GET.get('id'))
    record = models.record()
    record.id = id
    record.cancel()
    return HttpResponse(json.dumps({'result':1}))

