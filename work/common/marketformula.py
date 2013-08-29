#-*-coding:utf-8
import urllib2
import re
import urllib
import base64
# htmlcontent=urllib2.urlopen("http://x.10jqka.com.cn/stockpick/search?tid=stockpick&w=%E6%9C%88%E7%BA%BFmacd%E5%BA%95%E8%83%8C%E7%A6%BB%E7%9A%84%E8%82%A1%E7%A5%A8&qs=other&querytype=stock&my=1").read()

# pattern=re.compile(r"QUOTE:(.*)IsHistorical:false")
# formlua=re.findall(pattern,htmlcontent)[0].strip("\t").replace("&amp;amp;","&")
# source=re.findall(r"source:(.*)",formlua)[0]
# editsource=source.replace("&amp;","")
# symbol={"lt":"<","gt":">"}
# for k,v in symbol.iteritems():
# 	match=re.findall("%s;"%(k),editsource)
# 	if match:
# 		editsource=editsource.replace(k,v)
# editsource=base64.b64encode(editsource)
# formlua=formlua.replace(source,editsource)
# req=urllib2.Request(url="http://172.20.200.190/hexin",data=formlua)
# a=urllib2.urlopen(req).read()
# print a

def __structurl(url,keyword):
	if url.endswith("/"):
		url=url+"stockpick/search?&w="+urllib.quote(keyword)+"&my=1"
	else:
		url=url+"/stockpick/search?&w="+urllib.quote(keyword)+"&my=1"
	return url

def run(keywords):
	pattern=re.compile(r"QUOTE:(.*)IsHistorical:false")
	url="http://x.10jqka.com.cn"
	symbol={"&lt;":"<","&gt;":">"}
	urlerror=[]
	noformula=[]
	with open("formlua.txt","w+") as f:
		for keyword in keywords:
			keyword=keyword.strip("\n")
			url="http://x.10jqka.com.cn/stockpick/search?&w="+urllib.quote(keyword)+"&my=1"

			try:
				htmlcontent=urllib2.urlopen(url).read()
			except:
				print url
				urlerror.append(keyword)
				continue
			if re.findall(pattern,htmlcontent):
				formluastr=re.findall(pattern,htmlcontent)[0].strip("\t").replace("&amp;amp;","&")
			

			else:
				noformula.append(keyword)
				continue
			sourcestr=re.findall(r"source:(.*)",formluastr)[0]
			editsource=sourcestr.replace("amp;","")
			for k,v in symbol.iteritems():
				match=re.findall("%s"%(k),editsource)
				if match:
					editsource=editsource.replace(k,v)
				print editsource
			editsource=base64.b64encode(editsource)
			formluastr=formluastr.replace(sourcestr,editsource)
			f.write(keyword+"\t"+formluastr+"\n")
	return urlerror,noformula



if __name__=="__main__":
	# keywords=["月线macd底背离的股票"]
	# with open("400.txt","r") as f:
	# 	keywords=f.readlines()
	# (urlerror,noformula)=run(keywords)
	# if urlerror:
	# 	with open("urlerror.txt","w+") as f:
	# 		for line in urlerror:
	# 			f.write(line+"\n")
	# if noformula:
	# 	with open("noformula.txt","w+") as f:
	# 		for line in noformula:
	# 			f.write(line+"\n")
	with open("formlua.txt","r") as f:
		a={}
		for x in f.readlines():
			a[x.split("\t")[0]]=a[x.split("\t")[1]]
	for k,v in a.iteritems():
		req=urllib2.Request(url="http://172.20.200.190/hexin",data=v)
		text=urllib2.urlopen(req).read()
		if "<ErrorMsg>" in text:
			print k


	


