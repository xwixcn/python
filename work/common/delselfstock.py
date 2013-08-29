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
# def delstock(stocknum):  
#     cj=cookielib.CookieJar()
#     opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
#     urllib2.install_opener(opener)
#     LOGINPARAMS={"act":"login_submit",
#                  "uname":"wdsrkj827",
#                  "passwd":"123456"
#                  }
#     data=urllib.urlencode(LOGINPARAMS)+"&submit=%B5%C7%A1%A1%C2%BC&longLogin=on"
#     req=urllib2.Request(url='http://pass.10jqka.com.cn/login',data=data)
#     urllib2.urlopen(req).read()
#     while stocknum:
#         data=urllib.urlencode({"code":stocknum})
#         header={"User-Agent":"Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1496.0 Safari/537.36 AlexaToolbar/alxg-3.1"}
#         req=urllib2.Request(url='http://i.10jqka.com.cn/ucenter/selfstock/del',data=data,headers=header)
#         response=json.loads(urllib2.urlopen(req).read())
#         print response
#         stocknum=response["result"]


class DelSelfStock():
    def __init__(self,uname,password):
        self.uname=uname
        self.password=password
    
    def run(self):
        cj=cookielib.CookieJar()
        opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        urllib2.install_opener(opener)
        LOGINDICT={"act":"login_submit",
                 "uname":"%s"%(self.uname),
                 "passwd":"%s"%(self.password)
                 }
        LOGINPARAMES=urllib.urlencode(LOGINDICT)+"&redir=http%3A%2F%2Fx.10jqka.com.cn%2Fstockpick&submit=%B5%C7%A1%A1%C2%BC&longLogin=on".encode("utf-8")
        req=urllib2.Request(url='http://pass.10jqka.com.cn/login',data=LOGINPARAMES)
        urllib2.urlopen(req).read()
        delflag=True
        while delflag:
            stocknum=raw_input("请输入第一页的股票代码，如果不想继续，请输入No:")
            if stocknum in ["No","N"]:
                break
            header={"User-Agent":"Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1496.0 Safari/537.36 AlexaToolbar/alxg-3.1"}
            while stocknum:
                data=urllib.urlencode({"code":stocknum})
                req=urllib2.Request(url='http://i.10jqka.com.cn/ucenter/selfstock/del',data=data,headers=header)
                response=json.loads(urllib2.urlopen(req).read())
                print response
                stocknum=response["result"]
                
    def startdel(self):
        self.run()

if __name__=="__main__":
    d=DelSelfStock("wdsrkj827","123456")
    d.startdel()
    