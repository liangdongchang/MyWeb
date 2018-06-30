import os
import re
import time

import datetime
from django.test import TestCase

# Create your tests here.
#
# class Test():
#     def __init__(self,name):
#         self.name = name
#     def test(self):
#         print('testing...')
#
# test = Test('测试')
# # 查看所有属性和方法
# list1 = dir(test)
# print(list1)
# # 检查实例是否有这个属性
# print(hasattr(test, 'name'),hasattr(test, 'test'),hasattr(test, 'tt'))
# # 设置属性值
# setattr(test,'name','测试2')
# # 获取属性值
# print(getattr(test, 'name'))
'''
timedalte 是datetime中的一个对象，该对象表示两个时间的差值

构造函数：datetime.timedelta(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0)
其中参数都是可选，默认值为0
1 millisecond = 1000 microseconds
1 minute = 60 seconds
1 hour = 3600 seconds
1 week = 7 days
'''
# # 获取当前时间
# now = datetime.datetime.now()
# # 获取今天零点
# zeroToday = now - datetime.timedelta(hours=now.hour, minutes=now.minute, seconds=now.second,microseconds=now.microsecond)
# # 获取23:59:59
# lastToday = zeroToday + datetime.timedelta(hours=23, minutes=59, seconds=59)
# # 获取前一天的当前时间
# yesterdayNow = now - datetime.timedelta(hours=23, minutes=59, seconds=59)
# # 获取明天的当前时间
# tomorrowNow = now + datetime.timedelta(hours=23, minutes=59, seconds=59)
#
# print('时间差',datetime.timedelta(hours=23, minutes=59, seconds=59))
# print('当前时间',now)
# print('今天零点',zeroToday)
# print('获取23:59:59',lastToday)
# print('昨天当前时间',yesterdayNow)
# print('明天当前时间',tomorrowNow)

#
# os.environ.__setattr__('MAIL_PASSWORD','123456')
#
# for k,v in os.environ.items():
#     print(k,v)
# # os.environ['MAIL_PASSWORD'] = '123456'
# # os.environ.__setitem__('MAIL_PASSWORD','123456')
# 验证中文
# pt = r'^[/u4E00-/u9A5]+$'
# ret = re.match(r'^[\u4e00-\u9fa5]+&','你好')
# print(ret)

from PIL import Image
import pytesseract

# 上面都是导包，只需要下面这一行就能实现图片文字识别
text = pytesseract.image_to_string(Image.open('15.jpg'), lang='chi_sim')
print(text)
