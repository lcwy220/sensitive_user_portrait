# -*- coding: utf-8 -*-

import time

def unix2hadoop_date(ts):
    return time.strftime('%Y_%m_%d', time.localtime(ts))

def ts2datetime(ts):
    return time.strftime('%Y-%m-%d', time.localtime(ts))

def ts2date(ts):
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(ts))

def datetime2ts(date):
    return int(time.mktime(time.strptime(date, '%Y-%m-%d')))

def window2time(window, size=24*60*60):
    return window*size

def datetimestr2ts(date):
    return time.mktime(time.strptime(date, '%Y%m%d'))

def ts2datetimestr(ts):
    return time.strftime('%Y%m%d', time.localtime(ts))

def ts2HourlyTime(ts, interval):
    # interval 取 Minite、Hour
    ts = ts - ts % interval
    return ts

def ts2datetime_full(ts):
    return time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(ts))

def date2ts(date):
    timeArray = time.strptime(date, '%Y-%m-%d %H:%M:%S')
    timestamp = int(time.mktime(timeArray))
    return timestamp

if __name__=='__main__':
    result = ts2date(int('1378397099'))
    print 'result:', result
    #date = '2013-10-10 23:40:00'
    #timestamp = date2ts(date)
    #print 'timestamp:', timestamp
