#-*-coding:utf-8
from difflib import HtmlDiff
import urllib2
import json
import os
proxy_Handle = urllib2.ProxyHandler( {"http": "http://172.20.23.205:80"} )
opener = urllib2.build_opener( proxy_Handle )
urllib2.install_opener( opener )
url="http://x.10jqka.com.cn/stockpick/search?preParams=&ts=1&f=1&qs=1&querytype=stock&tid=stockpick&w=%E7%83%AD%E9%97%A8%E6%A6%82%E5%BF%B5%E8%82%A1&queryarea=all&source=data"
testdata=urllib2.urlopen(url).read()
testdata=json.loads(testdata)
print testdata["result"]
print testdata["qid"]
# d=[]
# for x in testdata["result"]:
# 	p=""
# 	for z in x:
# 		if isinstance(z,list):
# 			p+="\t"+'\t'.join(z)
# 		else:
# 			p+="\t"+z
# 	d.append(p.strip("\t").encode("utf-8"))
# print d
# s = HtmlDiff.make_file(HtmlDiff(),d,['600519.SH\n\xe8\xb4\xb5\xe5\xb7\x9e\xe8\x8c\x85\xe5\x8f\xb0\n198.83', '600436.SH\n\xe7\x89\x87\xe4\xbb\x94\xe7\x99\x80\n108.34'],context=True)
# print s.find("ISO-8859-1")
# print s
# s=s.replace("ISO-8859-1","utf-8")
# if not os.path.exists("../datatest"):
# 	os.mkdir("../datatest")
# filename="../datatest"+"/%s.html"%("helloa")
# f=open(filename,"w")
# f.write(s)
# f.close
