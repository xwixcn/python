#-*-coding:utf-8
#!usr/bin/python
'''
python 元类
'''
from warnings import warn

class A(object):
    _a={}

    def __init__(self):
        pass
    
    @staticmethod
    def test1():
        pass

    @classmethod
    def test2(cls):
        pass

    def test3(self):
        pass

a=A()
b=A()
print id(a)
print id(b)
print a.test1
print A.test1
