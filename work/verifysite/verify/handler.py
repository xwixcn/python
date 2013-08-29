
#-*-coding:utf-8
import json

'''
用来处理网页上的原数据
'''
def jsonhandler(initsource):
	data=json.loads(initsource)
	return data