import time

import datetime
from django.test import TestCase

# Create your tests here.

class Test():
    def __init__(self,name):
        self.name = name
    def test(self):
        print('testing...')

test = Test('测试')
# 查看所有属性和方法
list1 = dir(test)
print(list1)
# 检查实例是否有这个属性
print(hasattr(test, 'name'),hasattr(test, 'test'),hasattr(test, 'tt'))
# 设置属性值
setattr(test,'name','测试2')
# 获取属性值
print(getattr(test, 'name'))






