#-*-coding:utf-8
import urllib2




class Source(object):
	def __init__(self,*kwargs):
		pass

	def getSource(object):
		pass



class UrlSource(Source):

	def __init__(self,url,query=None):
		super(UrlSource,self).__init__()
		if query is not None:
			url=url.format(query.encode("utf-8"))
		self.requesturl=url

	def getSource(self):
		try:
			source=urllib2.urlopen(self.requesturl).read()
			return source
		except urllib2.URLError:
			raise urllib2.URLError,"{0}请求错误".format(self.requesturl)

