#-*-coding:utf-8
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

lock=Lock()
def __structurl(url,keyword):
	if url.endswith("/"):
		url=url+"stockpick/search?&"+keyword+"&source=data"
	else:
		url=url+"/stockpick/search?&"+keyword+"&source=data"
	return url

def run(queryQ,url):
	with lock:
		while queryQ.empty()==False:
			try:
				query=queryQ.get().strip("\n")
				if url.endswith("/"):
					queryurl= url + 'stockpick/search?w=' + urllib2.quote( query ) + "&source=data"
				else:
					queryurl= url + '/stockpick/search?w=' + urllib2.quote( query ) + "&source=data"
				sourcedata=json.loads(urllib2.urlopen(queryurl).read())
				if sourcedata["title"]==None:
					with open("Noparse.txt","a+") as f:
						f.write(query+"\n")
				elif len(sourcedata["result"])==0:
					with open("Noresult.txt","a+") as f:
						f.write(query+"\n")
				else:
					pass
			except Exception, e:
				raise e
			finally:
				pass


if __name__ == '__main__':
	url="http://x.10jqka.com.cn"
	threads=[]
	queryQ=Queue()
	with open("zhibiao.case","r") as f:
		for line in f.readlines():
			queryQ.put(line)
	print queryQ.qsize()

	threadnum=10
	for i in range(threadnum):
		thread=Thread(target=run,args=(queryQ,url))
		threads.append(thread)

	for thread in threads:
		thread.start()

	for thread in threads:
		thread.join()








