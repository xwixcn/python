#-*-coding:utf-8
#!/usr/bin/python
'''
相似问句检测脚本'
'''
import urllib2, urllib
import base64
import sys
import json
 
f=open('../testResult/Recommond_result.txt','w+')
p=open('../testResult/NOTRecommond_result.txt','w+')
for eachline_2 in open('../testCase/query.text').readlines():
    Query=eachline_2.strip('\n').split('\t')[1]
    line = "http://192.168.23.52:9992/solr/queans/queryrephase?querytype=stock&wt=json&indent=on&q=" + urllib.quote(Query)
    parseResult = urllib2.urlopen(line).read()
    jsonRes = json.loads(parseResult)
    uidata = ""
    try:
        for item in jsonRes["results"]:
            try:
                if item.has_key("qdata"):
                    uidata = item["qdata"]
                else:
                    continue
                decodeStr = base64.b64decode(uidata)
                decodeStr=eval(decodeStr)
                rawquery=decodeStr["rawQuery"].strip('\n')
                rpQuery=""
                for elem in decodeStr['rpQuery']:
                    rpQuery+=elem['choice']+'\t'
                f.write('Hanyu:%s\tresult:%s\n'%(Query,rpQuery))
            except Exception,e:
                p.write('Hanyu:%s\tNO RESULT!\n'%(Query))
    except Exception,e:
        print e
f.close()
p.close()
