#-*- coding:utf-8 -*-

def weibo_sort_interface(username , time , sort_scope, sort_norm, arg=None, st=None, et=None, isall=False, task_number=0, number=100):
    task_number = int(task_number)
    print "user_interface:", number

    user_list = []
    during = ( datetime2ts(et) - datetime2ts(st) ) / DAY + 1
    time = 1
    if during > 3:
        time = 7
    elif during > 16:
        time = 30
    if isall:
        if sort_scope == 'all_limit_keyword':
            pass

    return []
