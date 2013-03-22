#-*-coding:utf-8-*-
import urllib2

import base64

method="method=quote&datetime=16384(-1-0)&append=Y&sortby=ZHANGDIEFU&sorttype=select&datatype=10&codelist=17()&formula=period:16384;ID:7615;NAME:默认名字;source:ZGlmZl8wPWVtYShjbG9zZSwxMikgLSBlbWEoY2xvc2UsMjYpO2RlYV8xPWVtYShkaWZmXzAsOSk7bWFjZF8yPTIqKGRpZmZfMC1kZWFfMSk7aWR4dmFsXzM9bWFjZF8yO1NFTEVDVCBoaHYobWEoYyw1KSwxMCk8O3JlZihjLDE1KSBhbmQgbGx2KG1hKGRpZmZfMCw1KSwxMCk+O3JlZihkaWZmXzAsMTUpIGFuZCBtYWNkXzI8O3JlZihtYWNkXzIsMTUp;&sortappend=Y&"

method1="method=quote&datetime=16384(20130320-20130320)&append=Y&&fuquan=Q&sortappend=Y&sortby=10&sorttype=select&datatype=10&codelist=17();33();21();22();&sortappend=Y&formula=period:16384;ID:7615;NAME:默认名字;source:ZGlmZl8wPWVtYShjbG9zZSwxMikgLSBlbWEoY2xvc2UsMjYpO2RlYV8xPWVtYShkaWZmXzAsOSk7bWFjZF8yPTIqKGRpZmZfMC1kZWFfMSk7aWR4dmFsXzM9bWFjZF8yO1NFTEVDVCBoaHYobWEoYyw1KSwxMCk8O3JlZihjLDE1KSBhbmQgbGx2KG1hKGRpZmZfMCw1KSwxMCk+O3JlZihkaWZmXzAsMTUpIGFuZCBtYWNkXzI+O3JlZihtYWNkXzIsMTUp;&sortappend=Y&"
req=urllib2.Request(url="http://172.20.200.190/hexin",data=method1)
a=urllib2.urlopen(req).read()
print a
print base64.b64decode("ZGlmZl8wPWVtYShjbG9zZSwxMikgLSBlbWEoY2xvc2UsMjYpO2RlYV8xPWVtYShkaWZmXzAsOSk7bWFjZF8yPTIqKGRpZmZfMC1kZWFfMSk7aWR4dmFsXzM9bWFjZF8yO1NFTEVDVCBoaHYobWEoYyw1KSwxMCk8O3JlZihjLDE1KSBhbmQgbGx2KG1hKGRpZmZfMCw1KSwxMCk+O3JlZihkaWZmXzAsMTUpIGFuZCBtYWNkXzI8O3JlZihtYWNkXzIsMTUp")

def __structurl(url,keyword):
	if url.endswith("/"):
		url=url+"stockpick/search?&w="+urllib.quote(keyword)+"&my=1"
	else:
		url=url+"/stockpick/search?&w="+urllib.quote(keyword)+"&my=1"
	return url