# -*- coding: utf-8 -*-

#from django.http import HttpResponse
from django.shortcuts import render
import json
from django.http import HttpResponse

def first_page(request):
    return render(request, 'home.html')

def returnDic(request):
    dic = { 'str': 'this is a string', 'list': [1, 2, 'a', 'b'], 'sub_dic': { 'sub_str': 'this is sub str', 'sub_list': [1, 2, 3] }, 'end': 'end' }
    return HttpResponse(json.dumps(dic))

def hello(request):
    cate_list = []
    cate_list.append('a');
    cate_list.append('b');
    return HttpResponse(json.dumps(cate_list))