#-*-coding:utf-8
#!/usr/bin/python
from lxml import etree
from urllib2 import urlopen
from urllib import urlencode
'''
spellcheck脚本
'''
class spelltest:
    def __init__(self):
        pass

    def getResult(self):
        f=open('recommond_result.txt','a+')
        lines=open('recommond_previous.txt','r').readlines()
        for Query in lines:
                Query=Query.split('\t')[0].lstrip('Query:')
                query=urlencode({'q':Query})
                spellurl="http://192.168.23.43:8888/search?%s&tid=spell&spt=1"%(query)
                spell=urlopen(spellurl).read()
                Parse=etree.HTML(spell)
                try:
                    spellresult=""
                    spellResultlist=Parse.xpath(r'.//result')
                    for spellResult in spellResultlist:
                        spellresult+=spellResult.text+"\t"
                    if spellresult=="":
                        pass
                    else:
                        f.write("Query:%s\tresult:%s\n"%(Query,spellresult.encode("utf-8")))
                except:
                    pass
        f.close()


if __name__=="__main__":
    a=spelltest()
    a.getResult()
