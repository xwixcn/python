#-*-coding:utf-8-*-
import urllib, urllib2, cookielib 
import os, time
from lxml import etree
from datetime import datetime

def login():
        cj = cookielib.CookieJar()
        opener = urllib2.build_opener( urllib2.HTTPCookieProcessor( cj ) )  
        login_url = r'http://epaper.cs.com.cn/dnis/client/zzb/ggtz.jsp?url=/dnis/TRSIdSSSOProxyServlet?username=hzhexin%26password=456123&state=3'   
        opener.addheaders = [( 'Host', 'www.google.com.hk' ),
                            ( 'User-Agent', 'Mozilla/5.0 (Ubuntu; X11; Linux i686; rv:8.0) Gecko/20100101 Firefox/8.0' ),
                            ( 'Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8' ),
                            ( 'Accept-Language', 'en-us,en;q=0.5' ),
                            ( 'Accept-Encoding', 'gzip, deflate' ),
                                                                                                                                               ( 'Accept-Charset', 'ISO-8859-1,utf-8;q=0.7,*;q=0.7' ),
                                                                                                                                                                      ( 'Connection', 'keep-alive' ),
                                                                                                                                                                                             ( 'Referer', 'http://www.google.com.hk' ), ]  
        opener.open( login_url )
        print cj
        return opener
                                
opener = login()
time=datetime.now().strftime("%Y-%m/%d")
print time
url="http://epaper.cs.com.cn/html/2012-08/06/nw.D110000zgzqb_20120806_1-A12.htm?div=-1"
try:
    text = opener.open( url ).read()
    f = open( 'test.txt', "w" ).write( text )
except Exception,e:
    print e
page=etree.HTML(text)
hrefs=page.xpath(u"//a")
i=0
href_text={}
for href in hrefs:
    if href.attrib["href"].startswith("nw"):
        if href.text:
            href_text[href.attrib["href"]]=href.text
for x,y in href_text.items():
    print x,y 
print len(href_text)




