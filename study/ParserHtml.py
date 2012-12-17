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

    '''def get_longhu(self,marketname):
        Stockmarket=self.soup.findAll('div',attrs={'class':'lhb_list'})
        longhuDic={}
        for market in Stockmarket:
            markettitle=market.findAll('div',attrs={'class':'lhb_hd'})[0].text.encode('utf-8')
            longhuDic[markettitle]=self.__getdata(market)
        try:
            print '%s的数据如下:\n%s'%(marketname,longhuDic[marketname])
            return longhuDic[marketname]
        except KeyError,e:
            print '没有这个板块,请输入股市名字:1.沪市,2.深市,3.中小企业板,4.创业板'''

            
if __name__ == "__main__":
    soup = Parsehtml()
     #b = soup.get_Fundsdata( 'http://data.10jqka.com.cn/funds/', '月资金' )
    c = soup.get_data('http://data.10jqka.com.cn//datacenter/Trade/jdtj/?stype=sort&high=new&yrqsort=DESC&page=0&click=number&period=5')
     
