
#-*-coding:utf-8

import urllib2
import json
import urllib
from verify.handler import jsonhandler
from verify.source import UrlSource
DefaultUrl="http://www.iwencai.com/stockpick/search?preParams=&ts=1&f=1&qs=1&querytype=&tid=stockpick&w={0}\
		+&queryarea=all&my=1&source=data"




class WenCai(object):

	def __init__(self,url=DefaultUrl):
		self.url=url
		


	def executeQuery(self,query,handler=jsonhandler):
		urlsource=UrlSource(self.url,query)
		data=handler(urlsource.getSource())
		resultset=WenCaiResultSet(data)
		return resultset




class ResultSet(object):

	def __init__(self,data):
		self.data=data

	def getNodeDataByIndex(self,index):
		pass



class WenCaiResultSet(ResultSet):

	def __init__(self,data):
		super(WenCaiResultSet,self).__init__(data)


	def getNodeDataByIndex(self,index):
		try:
			if index==0:
				#stockcode,去掉sz或者sh
				data=[data[index].split(".")[0] for data in self.data["result"]]
			else:
				data=[data[index] for data in self.data["result"]]
			nodedata=NodeData(data)
		except IndexError, e:
			raise IndexError("index error")
		return nodedata


class NodeData(object):

	def __init__(self,data):
		self.data=data


	def tolist(self):
		if isinstance(self.data,list):
			return self.data

	def torounddata(self,ndigits):
		if isinstance(self.data,list):
			rounddata=[round(float(data),ndigits) for data in self.data]
		else:
			rounddata=round(float(self.data),ndigits)

		return rounddata








