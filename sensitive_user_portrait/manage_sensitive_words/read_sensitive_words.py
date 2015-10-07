# -*- coding:utf-8 -*-
from openpyxl import load_workbook
import redis

data = load_workbook('sensitive_words.xlsx')
table = data.sheets()[1]
nrows = table.nrows
ncols = table.ncols

print table.row_value(1)

