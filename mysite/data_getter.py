#-*- coding:utf-8 -*-

import urllib
import string
import simplejson as json
import data_handle
from datetime import datetime

REQUEST_URL = 'http://112.124.1.3:8004'
global product_data	
'''获取所有的类别'''
def get_all_category():
	all_category_url = 'api/commodity'	
	#use json.loads to convert str to json obj
	#also can use eval() or other funcs
	data = json.loads(urllib.urlopen('/'.join([REQUEST_URL,
		all_category_url])).read())
	#for single_cate in data:
	#	print single_cate['name']
	return data;	

'''获取各个分类的商品信息'''
def get_products_info_each_cate():
    # 获取全部分类
	all_category = get_all_category()
	first_cat = data_handle.split_category(all_category).keys()
	all_category_url = 'api/commodity'
	cat_pro_data = {}
    # 对各个分类获取商品信息
	for category_name in all_category:
		name = category_name['name']
        # 获取分类对商品总数
		cate_commody_count= json.loads(urllib.urlopen('?'.join([
	    '/'.join([REQUEST_URL, all_category_url+'/count']),
		urllib.urlencode({
			'category_name': name,
			})])).read())
        # 获取大类名（此项功能针对对是大类）
		first_cat_name = name.split('>')[0]
		if (cat_pro_data.has_key(first_cat_name)):
			cat_pro_data[first_cat_name][0]=cate_commody_count['count']+cat_pro_data[first_cat_name][0]
		else:
			first_cat_data = [cate_commody_count['count'],0]
			cat_pro_data[first_cat_name]=first_cat_data
        # 获得总页数进而取得该分类所有商品
 		page = cate_commody_count['count']/20+1
        # 此处只需取道评论数，所以设置对field为stats_info
 		field = ['stats_info']
        # 该方法为根据类别名、页数、以及需要取得对field返回商品信息的list
 		specified_commody_data = get_product_data_of_each_cat(name,page,field)
 		if (specified_commody_data!=None):
 			for single_commody_data in specified_commody_data:
 			 	cat_pro_data[first_cat_name][1]+=single_commody_data['stats_info']['review_count']
	return cat_pro_data
	
def get_product_data(ASIN):
	'''获取Demo的商品信息'''
	target_url = 'http://112.124.1.3:8004/api/commodity/'+ASIN+'/'
	return json.loads(urllib.urlopen(target_url).read())


'''获取星级评分'''
def review_hist(product_data):
	star_info = product_data['stats_info']['star_info']
	star_list=[]
	star_keys= ['1','2','3','4','5']
	for i in star_keys:
		star_list.append(star_info[i])
	star_list.append(string.atof(product_data['stats_info']['avg_info']))
	star_list.append(product_data['stats_info']['review_count'])
	return star_list


def incre_list(origin_list):
    '''数组元素递加'''
    return [sum(origin_list[0: idx]) for idx,ele in enumerate(origin_list)]

def get_raw_review(product_data):
	count_list={}
	for review in product_data['review']:
	    time = (datetime.strptime(review['publishTime'],'%Y-%m-%d %H:%M:%S').strftime('%y %b %w'))
	    if (count_list.has_key(time)):
	    	count_list[time]=count_list[time]+1
	    else:
	    	count_list[time]=1
	return count_list

def get_review_time(product_data):
	time_list = []    
	for review in product_data['review']:
	    time_list.append(datetime.strptime(review['publishTime'],
                                           '%Y-%m-%d %H:%M:%S'))
	time_list = list(set(time_list))    
	review_count_dict = {}
	for single_date in time_list[::-1]:
		if review_count_dict.has_key(int(single_date.strftime('%Y%m'))):
			review_count_dict[int(single_date.strftime('%Y%m'))]=review_count_dict[int(single_date.strftime('%Y%m'))]+1
		else :
			review_count_dict[int(single_date.strftime('%Y%m'))] = 1
	review_count_list = sorted(review_count_dict.iteritems(), key=lambda x:x[0])
	count_data = incre_list(map(lambda x:x[1], review_count_list))
	date_data = map(lambda x:datetime.strptime(str(x[0]), '%Y%m'), review_count_list)	
	new_date_data=[]
	for date in date_data:
		new_date_data.append(date.strftime('%Y年%m月'))
	review_time_data={'date':new_date_data,'count':count_data,'each_count':review_count_list}
	return review_time_data

'''获取商品价格'''
def get_price(product_data):
	price_list={}
	date_list=[]
	for offer in product_data['offer']:
		for info in offer['info']:
			date = datetime.strptime(info['timestamp'],'%Y-%m-%d %H:%M:%S').strftime('%y %b %w')
			has_date= False
			for key in price_list:
				if (key==date):
					has_date=True
					price_list[key].append(info['price'])
					break
			if (has_date==False):
				splited_date = date.split(' ')
				date_list.append(splited_date[0]+" " + splited_date[1]+' '+splited_date[2])
				price_list[date]=[info['price']]
	context={'date':date_list,'price':price_list}
	return context



def get_img(product_data):
	return product_data['productInfo'][0]['img']

def get_product_name(product_data):
	return product_data['productInfo'][0]['name']
	
def get_avaliable_fields():
	output = open('fields.txt','w')
	fileds_url = 'api/commodity/field'
	data = json.loads(urllib.urlopen('/'.join([REQUEST_URL,
		fileds_url])).read())
	output.writelines(field for field in data)


'''根据类别名、页数、需要取得的内容获得商品的数据列表'''
def get_product_data_of_each_cat(category_name,page,field):
    specified_cate_data = []
    all_category_url = 'api/commodity'
    for page_num in xrange(page):
        print page_num
        specified_cate_data.extend(json.loads(urllib.urlopen('?'.join(['/'.join([REQUEST_URL, all_category_url]),urllib.urlencode({
			'category_name': category_name,
			'page':page_num+1,
			'field':field,
            })])).read()))
    return specified_cate_data

   # 获取具体类别下对所有商品对数据
def get_specified_commodity(category_name):
    all_category_url = 'api/commodity'
    cate_commody_count= json.loads(urllib.urlopen('?'.join(['/'.join([REQUEST_URL, all_category_url+'/count']),urllib.urlencode({
        'category_name': category_name,})])).read())
    print cate_commody_count['count']
    page =  cate_commody_count['count']/20+1
    print page
    field = ['ASIN', 'stats_info','productInfo','offer']
    specified_cate_data = get_product_data_of_each_cat(category_name,page,field)
    specified_cate_review_count = [];
    for single_commodity in specified_cate_data:
        specified_cate_review_count.append(single_commodity['stats_info']['review_count'])
    count = len(specified_cate_data)
    print count
    for j in range(count-1,-1,-1):
		for i in range(j):
			if specified_cate_review_count[i]<specified_cate_review_count[i+1]:
				specified_cate_review_count[i],specified_cate_review_count[i+1] = specified_cate_review_count[i+1],specified_cate_review_count[i]
				specified_cate_data[i],specified_cate_data[i+1] = specified_cate_data[i+1],specified_cate_data[i]
    return specified_cate_data

if __name__ == '__main__':
    get_specified_commodity('Clothing&Accessories>Luggage&Bags>Backpacks');
	#print "Hello";
	#get_products_info_each_cate()
	#all_category = get_all_category()
	#spilited_category = json.dumps( data_handle.split_category(all_category))
	#print spilited_category
	#return spilited_category
	#get_specified_commodity(all_category[0]['name'])	
		#splited_category.append(each_category['name'].spilt('>'))
	#for each_category in splited_category:
		#print each_category[0]	
	#get_specified_commodity()
	#get_avaliable_fields()
	# product_data = get_product_data('B0029DPGDW')
	# get_raw_review(product_data)
	#get_review_time(product_data)
	#review_hist(product_data)
	#price_list = get_price(product_data)
	#data_handle.handle_price(price_list)
	#get_img(product_data)