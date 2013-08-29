#-*-coding:utf-8
from verify.source import UrlSource
from verify.data import WenCai
from verify.asserts import IncludeAssert
from verify.models import Case
from verify.models import IncludeResult
from verify.models import Job
import warnings
warnings.filterwarnings("ignore")
import datetime
import logging

log=logging.getLogger(__name__)


def runCase():
	caselist=Case.objects.all()
	resultobjlist=[]
	wencai=WenCai()
	try:
		job=Job.objects.create(totalnum=len(caselist))
		log.info("jobid:%s"%(job.id))
		for case in caselist:
			console=Console(case,IncludeAssert)
			console.setDataList(wencai)
			diffresult=console.getDiffResult()
			if diffresult:
				resultobj=IncludeResult.objects.create(case=case,\
					falseresult=diffresult,jobid=job.id)
				resultobjlist.append(resultobj)
		job.executeUpdate(resultobjlist)
	except Exception,e:
		log.error(e.message)
		job.delete()
	return job.id





class Console(object):

	def __init__(self,case,assertclass,comparelist=None):
		self.case=case
		self.query=case.getQuery()
		self.comparecolumnindex=case.getCompareColumnIndex()
		self.comparelist=case.getCompareList() if not comparelist else comparelist
		self.assertclass=assertclass


	def setDataList(self,wencaiobj):
		nodedata=wencaiobj.executeQuery(self.query).getNodeDataByIndex(\
			self.comparecolumnindex)
		self.datalist=nodedata.tolist()
		log.info("datalist:%s"%(self.datalist))

	def getDiffResult(self):
		assertobj=self.assertclass(self.datalist,self.comparelist)
		equalflag=assertobj.execute()
		if not equalflag:
			falseresult=assertobj.getFalseResult()
			return falseresult
		return None



'''
def createOrupdateResult(resulttable,case,falseresult,jobid):
	result=resulttable.objects.filter(case=case,jobid=jobid)
	if result.exists():
		result=result.update(falseresult=falseresult,jobid=jobid)
	else:
		result=resulttable.objects.create(case=case,\
			falseresult=falseresult,jobid=jobid)
	return result
'''








		
