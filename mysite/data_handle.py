def handle_price(price_list):
    data_list = {}
    for key in price_list:
        data= price_list[key]
        data_list[key]=[get_max(data)]
        data_list[key].append(get_avr(data))
        data_list[key].append(get_min(data))
    return data_list
            
def get_max(data):
    max = data[0];
    for price in data:
        if (max<=price):
            max=price
    return max

            
def get_min(data):
    min = data[0];
    for price in data:
        if (min>=price):
            min=price
    return min

def get_avr(data):
    count = len(data)
    result = 0;
    for price in data:
        try:
            result += price
        except Exception,ex:
            continue
    result = result / count
    return result


   
    
def split_category(all_category):
    category_dic = {}
    for each_category in all_category:
        each_spilit_category = each_category['name'].replace('&','$').split('>')
        has_first=False
        for key in category_dic:
            if each_spilit_category[0]==key:  
                first_category = category_dic[key] 
                has_first=True
                has_second=False
                for key in first_category:
                    if key==each_spilit_category[1]:
                        first_category[key].append(each_spilit_category[2])
                        has_second=True
                        break;
                if (has_second==False):
                    new_second=[each_spilit_category[2]]
                    first_category[each_spilit_category[1]]= new_second
    if (has_first==False):
            new_second = [each_spilit_category[2]]
            new_first = {}
            new_first[each_spilit_category[1]]=new_second
            category_dic[each_spilit_category[0]]=new_first
    return category_dic