
'''
author:louhaibin
function:
To check whether the allocated Query been parsed or having result!
'''
from threading import Thread
import urllib2
import urllib
from threading import Lock
import  json 
from Queue import Queue
import hashlib
import sys
lock=Lock()
def __structurl(url,keyword):
	if url.endswith("/"):
		url=url+"stockpick/search?&w="+urllib.quote(keyword)+"&source=data"
	else:
		url=url+"/stockpick/search?&w="+urllib.quote(keyword)+"&source=data"
	return url


def getdataBysource(url):
	try:
		sourcedata=json.loads(urllib2.urlopen(url).read())
		return 0,sourcedata
	except Exception, e:
		return -1,e.message

def runindex(query,sourcedata):
	global noresultlist,noparserlist
	if sourcedata["title"]==None:
		noparserlist.append(query)
	elif len(sourcedata["result"])==0:
		noresultlist.append(query)
	else:
		pass


def run(queryQ ,url,jobtype):
	with lock:
		while queryQ.empty()==False:
			query=queryQ.get().strip("\n")
			queryurl=__structurl(url,query)
			status,sourcedata=getdataBysource(queryurl)
			if status==0:
				sourcedata=sourcedata
			else:
				sys.exit(1)
			if jobtype=="sameresult":
				runsameresultcase(query,sourcedata)
			elif jobtype=="index":
				runindex(query,sourcedata)
			else:
				pass

def runsameresultcase(query,sourcedata):
		if sourcedata["title"]==None or len(sourcedata["result"])==0:
			pass
		else:
			global resultmd5dic
			datadic={}
			datadic["title"]=sourcedata["title"]
			datadic["result"]=sourcedata["result"]
			datadicmd5=hashlib.md5(str(datadic)).hexdigest()
			resultmd5dic[query]=datadicmd5



if __name__ == '__main__':
	url="http://x.10jqka.com.cn"
	jobtype="index"
	threads=[]
	queryQ=Queue()
	resultmd5dic={}
	noresultlist=[]
	noparserlist=[]
	with open("zhibiao.case","r") as f:
		for line in f.readlines():
			queryQ.put(line)
	print "The Case Num:\t%s"%(queryQ.qsize())
	threadnum=10
	for i in range(threadnum):
		thread=Thread(target=run,args=(queryQ,url,jobtype))
		threads.append(thread)

	for thread in threads:
		thread.start()

	for thread in threads:
		thread.join()

	if jobtype=="sameresult":
		totalsamelist=[]
		if len(resultmd5dic)>0:
			for value in resultmd5dic.itervalues():
				samecaselist=[]
				for k,v in resultmd5dic.iteritems():
					if v==value:
						samecaselist.append(k)
				if len(samecaselist)>1:
					totalsamelist.append(samecaselist)
		finalresultlist=[]
		for x in totalsamelist:
			if x not in finalresultlist:
				finalresultlist.append(x)
		with open("a.txt","w+") as f:
			for line in finalresultlist:
				f.write("\t".join(line)+"\n")
	elif jobtype=="index":
		with open("Noparse.txt","w+") as f:
			for line in noparserlist:
				f.write(line+"\n")
		with open("Noresult.txt","w+")as f:
			for line in noresultlist:
				f.write(line+"\n")
	else:
		pass










