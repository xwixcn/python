 #-*-coding:utf-8-*-
from urllib2 import urlopen
from bs4 import BeautifulSoup
import re
class Parsehtml():
    def __init__( self):
        pass
                    
    def __getdata( self,soup ):
        tr = soup.findAll( 'tr', attrs = {'class':re.compile( '^biaobeis_' )} )
        title=soup.findAll('tr',attrs={'class':'biaotou_bg'})
        td=title[-1].findAll('td')
        titlemsg=""
        for i in range(0,len(td)):
            titlemsg+=td[i].text+'\t'
        titlemsglist=titlemsg.strip().split('\t')
        if titlemsglist[0].encode('utf-8')=="序号":
            begin=1
        else:
            begin=0
        #取50条数据
        Datalist={}
        for x in tr[0:50]:
            datamsg=""
            datalist={}
            td=x.findAll('td')
            for i in range(0,len(td)):
                datamsg+=td[i].text+'\t'
            datamsglist=datamsg.strip().split('\t')
            for title,data in zip(titlemsglist[begin+1:],datamsglist[begin+1:]):
                datalist[title]=data
            for a,b in datalist.items():
                print 'key:%s,value:%s'%(a,b)
            Datalist[datamsglist[begin]]=datalist
        return Datalist
    
    def get_data(self,url):
        page = urlopen( url ).read().decode('gbk').encode('utf-8')
        soup = BeautifulSoup( page,from_encoding="utf-8")
        Result=self.__getdata(soup)
        return Result


          
if __name__ == "__main__":
    soup = Parsehtml()
     #b = soup.get_Fundsdata( 'http://data.10jqka.com.cn/funds/', '月资金' )
    c = soup.get_data('http://data.10jqka.com.cn//datacenter/Trade/jdtj/?stype=sort&high=new&yrqsort=DESC&page=0&click=number&period=5')
     
