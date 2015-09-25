# -*-coding:utf-8 -*-

import sys
import re
import csv
import json
import time

from weibo_api import read_user_weibo

reload(sys)
sys.path.append('../../../../../libsvm-3.17/python/')
from sta_ad import load_scws

EXTRA_WORD_WHITE_LIST_PATH = './one_word_white_list.txt'

def load_one_words():
    one_words = [line.strip('\r\n') for line in file(EXTRA_WORD_WHITE_LIST_PATH)]
    return one_words

single_word_whitelist = set(load_one_words())
single_word_whitelist |= set('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789')

BLACK_WORDS_PATH = './black.txt'
def load_black_words():
    black_words = set([line.strip('\r\n') for line in file(BLACK_WORDS_PATH)])
    return black_words

black_words = load_black_words()

def get_emoticon_dict():
    results = dict()
    f = open('./emoticons.txt','rb')
    for line in f:
        line_list = line.split(':')
        emoticon = line_list[0]
        emo_class = line_list[1]
        try:
            results[emo_class].append(emoticon.decode('utf-8'))
        except:
            results[emo_class] = [emoticon.decode('utf-8')]
    return results
