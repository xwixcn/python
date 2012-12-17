#-*-coding:utf-8-*-
#!/usr/bin/python
from urllib2 import urlopen
from bs4 import BeautifulSoup
import re
from lxml import etree

class GetFunds():
  def __init__(self):
      page=urlopen('http://data.10jqka.com.cn/funds/').read()
      self.soup=BeautifulSoup(page)
      self.page=etree.HTML(page)

  def get_Detaildata(self):
      d=self.page.xpath("//div[@class='tabletys_or']")[0]
      c=d.xpath(".//div[@class='tabletys_otop']")
      print dir(c)
      
          


if __name__=="__main__":
    soup=GetFunds()
    soup.get_Detaildata()

