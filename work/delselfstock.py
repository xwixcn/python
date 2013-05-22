#!-*-coding:utf-8
#===============================================================================
# author:Haibin
#删除自选股
#===============================================================================

import urllib
import urllib2
import cookielib
import json
import sys
def delstock(stocknum):  
    cj=cookielib.CookieJar()
    opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    urllib2.install_opener(opener)
    req=urllib2.Request(url='http://pass.10jqka.com.cn/login',data='act=login_submit&redir=http%3A%2F%2Fx.10jqka.com.cn%2Fstockpick%2Fsearch%3FpreParams%3D%26ts%3D1%26f%3D1%26qs%3Dsl_1%26querytype%3D%26tid%3Dstockpick%26w%3D%25E4%25BB%258A%25E5%25B9%25B4%25E8%25B7%258C%25E5%25B9%2585%253E20%2525%25EF%25BC%258C%25E8%2582%25A1%25E4%25BB%25B7%25E5%25A4%25A7%25E4%25BA%258E10%25E5%2585%2583%26queryarea%3Dall&uname=wdsrkj827&passwd=123456&submit=%B5%C7%A1%A1%C2%BC&longLogin=on')
    urllib2.urlopen(req).read()
    while stocknum:
        data=urllib.urlencode({"code":stocknum})
        header={"User-Agent":"Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1496.0 Safari/537.36 AlexaToolbar/alxg-3.1"}
        req=urllib2.Request(url='http://i.10jqka.com.cn/ucenter/selfstock/del',data=data,headers=header)
        response=json.loads(urllib2.urlopen(req).read())
        print response
        stocknum=response["result"]
if __name__=="__main__":
    stocknum=raw_input("please input stocknum:")
    delstock(stocknum)