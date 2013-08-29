#-*-coding:utf-8
from django.db import models
import datetime
import urllib
# Create your models here.
DefaultUrl="http://www.iwencai.com/stockpick/search?preParams=&ts=1\
	&f=1&qs=1&querytype=&tid=stockpick&w={0}&queryarea=all"

tagAlink="<a target='_blank' href='{0}'>{1}</a>"
#问句
class Case(models.Model):

	query=models.CharField(max_length=100)
	comparelist=models.TextField(help_text='多个数据,请用逗号分割')
	comparecolumnindex=models.IntegerField(help_text='选择数据的哪一列进行比较,比如问财结果里面,\
		股票代码一般为0列，股票简称为1列,默认为0',default=0)
	requesturl=models.CharField(max_length=300,default=DefaultUrl,blank=True)
	addtime=models.DateTimeField(auto_now_add=True)

	def getQuery(self,encodetype=None):
		return self.query if not encodetype else self.query.encode(encodetype)

	def getCompareList(self):
		return self.comparelist.split(",")

	def getCompareColumnIndex(self):
		return self.comparecolumnindex

	def getRequestUrl(self):
		return self.requesturl

	def getCaseLink(self):
		link="/verify/case/{0}/".format(self.id)
		link=tagAlink.format(link,self.getQuery("utf-8"))
		return link

	def __unicode__(self):
		return "query:%s,index:%s"%(self.query,self.comparecolumnindex)





#结果
class Result(models.Model):
	case=models.ForeignKey(Case)
	jobid=models.IntegerField(default=0,editable=False)
	def linktowencai(self):
		requesturl=DefaultUrl if not self.case.getRequestUrl() else self.case.getRequestUrl()
		queryurl=requesturl.format(urllib.quote(self.case.getQuery("utf-8")))
		html=tagAlink.format(queryurl,"link to wencai")
		return html
	linktowencai.allow_tags=True

class IncludeResult(Result):
	falseresult=models.TextField(help_text='不一致的原因',editable=False)




class Job(models.Model):
	starttime=models.DateTimeField(auto_now_add=True)
	endtime=models.DateTimeField(blank=True,null=True)
	runtime=models.IntegerField(blank=True,default=0)
	totalnum=models.IntegerField(default=0)
	successnum=models.IntegerField(default=0)
	errornum=models.IntegerField(default=0)
	result=models.ManyToManyField(IncludeResult)

	def __updateStatisticsNum(self,errornum):
		self.successnum=self.totalnum-errornum
		self.errornum=errornum

	def __updateRunTime(self):
		self.endtime=datetime.datetime.now()
		self.runtime=(self.endtime-self.starttime).seconds

	def __updateResults(self,resultslist):
		for result in resultslist:
			self.result.add(result)

	def executeUpdate(self,resultslist):
		self.__updateStatisticsNum(len(resultslist))
		self.__updateRunTime()
		self.__updateResults(resultslist)
		self.save()


	def run_time(self):
		return str(self.runtime)+u"秒"

	def fail_cases(self):
		fail_cases=[obj.case for obj in self.result.all()]
		return fail_cases


	def jobid(self):
		link="/verify/result/?jobid={0}".format(self.id)
		html=tagAlink.format(link,self.id)
		return html









