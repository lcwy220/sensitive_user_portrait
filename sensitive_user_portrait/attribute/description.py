# -*- coding: utf-8 -*-

def active_geo_description(ip_result, geo_result):
    active_city = {}
    active_ip = {}
    ip_count = 0
    city_count = 0
    ip_list = ip_result.values()
    geo_list = geo_result.values()

    for item in ip_list:
        for k,v in item.items():
            if active_ip.has_key(k):
                active_ip[k] += v
            else:
                active_ip[k] = v
                ip_count += 1
    for item in geo_list:
        for k,v in item.items():
            if active_city.has_key(k):
                active_city[k] += v
            else:
                active_city[k] = v
                city_count += 1


    active_city = sorted(active_city.items(), key=lambda asd:asd[1], reverse=True)
    city = active_city[0][0]

    if city_count == 1 and ip_count <= 4:
        description_text = '为该用户的主要活动地，且较为固定在同一个地方登陆微博'
        city_list = city.split('\t')
        city = city_list[len(city_list)-1]
        description = [city, description_text]
    elif city_count >1 and ip_count <= 4:
        description_text1 = '多为该用户的主要活动地，且经常出差，较为固定在'
        description_text2 = '个城市登陆微博'
        city_list = city.split('\t')
        city = city_list[len(city_list)-1]
        description = [city, description_text1, city_count, description_text2]
    elif city_count == 1 and ip_count > 4:
        description_text = '为该用户的主要活动地，且经常在该城市不同的地方登陆微博'
        city_list = city.split('\t')
        city = city_list[len(city_list)-1]
        description = [city, description_text]
    else:
        description_text = '多为该用户的主要活动地，且经常出差，在不同的城市登陆微博'
        city_list = city.split('\t')
        city = city_list[len(city_list)-1]
        description = [city, description_text]
    return description


def active_time_description(time_trend_list):
    # active category based on time
    count = 0
    for v in time_trend_list:
        count += v[1]
    average = count / 6.0
    time_result = {}
    for i in range(6):
        for j in range(7):
            try:
                time_result[i] += time_trend_list[i+j*6][1]
            except:
                time_result[i] = time_trend_list[i+j*6][1]
    active_time_order = sorted(time_result.items(), key=lambda asd:asd[1], reverse=True)
    active_time = {'0':'0-4', '1':'4-8','2':'8-12','3':'12-16','4':'16-20','5':'20-24'}
    v_list = []
    for k,v in time_result.items():
        if v > average:
            v_list.append(active_time[str(k)])
    definition = ','.join(v_list)
    segment = str(active_time_order[0][0])


    pd = {'0':'夜猫子','1':'早起刷微博','2':'工作时间刷微博','3':'午休时间刷微博','4':'上班时间刷微博','5':'下班途中刷微博','6':'晚间休息刷微博'}
 
    description = '用户属于%s类型，活跃时间主要集中在%s' % (pd[segment], definition)

    return description


def hashtag_description(result):
    hashtag_dict = {}
    hashtag_list = result.values()
    for item in hashtag_list:
        for k,v in item.items():
            if hashtag_dict.has_key(k):
                hashtag_dict[k] += v
            else:
                hashtag_dict[k] = v

    order_hashtag = sorted(hashtag_dict.items(), key=lambda asd:asd[1], reverse=True)
    count_hashtag = len(hashtag_dict)

    count = 0 
    if hashtag_dict:
        for v in hashtag_dict.values():
            count += v
        average = count / len(result)

        v_list = []
        like = order_hashtag[0][0]
        v_list = hashtag_dict.keys()
        definition = ','.join(v_list)

    if count_hashtag == 0:
        description = u'该用户不喜欢参与话题讨论，讨论数为0'
    elif count_hashtag >= 3:
        description = u'该用户热衷于参与话题讨论,热衷的话题是%s' % definition
    else:
        description = u'该用户不太热衷于参与话题讨论, 参与的话题是%s' % definition

    return description

if __name__ == "__main__":
    c = {'beijing':{'219.224.135.1': 5}}
    b = {0:2, 14400:1,28800:3, 43200:5, 57600:2, 72000:3}
    a = {'花千骨':4}
    k = active_time_description(b)
    m = active_geo_description(c)
    n = hashtag_description(a)
    print m
    print k
    print n
