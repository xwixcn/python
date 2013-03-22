#-*-coding:utf-8
'''
Created on 2012-5-22
如果网站数据是JS生成的，那么需要找到js返回数据的地址，用火狐就可以找到，然后在下面添加一下。
格式为
"原网站地址":"Js数据地址"
@author: Administrator
'''

url_xpath ={'http://www.ctsec.com/ctzq/wsyyt/down.html?rjfx_id=1000176':'http://www.ctsec.com/ctzq/wsyyt/wsyyt_xzlb.jsp?menuId=000200020005&subId=0002000200050005&rjfx_id=1000176&hrefURL=&filter=MT0x',
            'http://www.chstock.com/html2/scsc/download.asp':'http://www.chstock.com/sc/downloadch1.asp',
            'http://www.dfzq.com.cn/dfzq/public/info_bqxx.jsp?classid=0002000100020006':'http://www.dfzq.com.cn/JSONService/rewinJsonInfoDetailByClass.jsp?classid=0002000100020006&hrefURL=&filter=',
            'http://www.cnht.com.cn/htzq/wsyyt/softdownload.html?classid=000100030003':'http://www.cnht.com.cn/htzq/wsyyt/rjList.jsp?flid=1000028&f=0.0026940892958574603&hrefURL=&filter=',
            'http://www.wanhesec.com.cn/whzq/wsyyt/down.html?classid=0002000100020009':'http://www.wanhesec.com.cn/whzq/wsyyt/down.jsp?pageIndex=1&hrefURL=&filter=',
            "http://tebon.com.cn/dbzq/fwzx/softdownload.html?classid=0001000100050007":"http://tebon.com.cn/JSONService/rewinJsonSoftListMore.jsp",
            "http://www.sywg.com/sywg/portal/portal_softdown.html":"http://www.sywg.com/sywg/rjxz.do?method=getSoftList",
            "http://www.west95582.com/jdw/wsyyt/rjxz/rjxz.jsp?classid=0002000200020005":"http://www.west95582.com/jdw/wsyyt/rjxz/rjList.jsp?flid=1027957&hrefURL=&filter=",
			"http://www.sczq.com.cn/Trade/TradeDownIndex/":"http://www.sczq.com.cn/Trade/GetSoftDownloads/?nodeid=169&_=1354613680651",
			"http://www.s10000.com/cdzq/wsyyt/rjxz.html?classid=00010002000400020001":"http://www.s10000.com/JSONService/rewinJsonSoftListMore.jsp",
			"http://www.gyzq.com.cn/gyzq/webpages/wsyyt/softdownload.html?curId=0001000200100004#this":"http://www.gyzq.com.cn/gyzq/wsyyt/rjxzList.jsp",
			"http://tebon.com.cn/dbzq/fwzx/softdownload.html?classid=0001000100050007":"http://tebon.com.cn/JSONService/rewinJsonSoftListMore.jsp?datalen=softList&filter=&hrefURL=&jsontype=json&softClassID=26",
            "http://www.95579.com/main/hall/software/index.html#hzb":"http://www.95579.com/main/hall/software/hzb.html",
			"http://www.dwjq.com.cn/info-product/economic/webTran.jsp":"http://www.dwjq.com.cn/info-product/getSoftList.do?pageSize=30"
			}

