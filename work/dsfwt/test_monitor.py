#-*-coding:utf-8-*
'''如果有LXML则用lxml，不然用python自己的模块'''
try:
	from lxml import etree
except ImportError:
	import xml.etree.ElementTree as etree
from urllib2 import urlopen
import datetime 
import time
import threading
import re
from JS_site import url_xpath


class xmlparse:
	z = 0
	def __init__( self, filename ):
		self.sFilename = filename
		'''判断文件是不是xml'''
		if filename.endswith( '.xml' ):
			try:
				self.oTree = etree.parse( filename )
			except Exception:
				print '对不起，XML文件无法正确读取，请确认XML名称和路径是否正确'
		else:
			print 'sorry,the file is not xml'
		#self.selenium = selenium("192.168.229.128", 4444, "*firefox", "http://search.10jqka.com.cn")
		
		
	def __Timestamp( self ):
		'''获取10位时间戳'''
		sNow = datetime.datetime.now()
		nTimestamp = int( time.mktime( sNow.timetuple() ) )
		return nTimestamp


	def ParserResult( self, elem ):
		'''把解析的XML结果先存起来'''
		dNodeResult = {}
		'''当对应的属性值不存在，则返回'''''
		for x in elem:
			sKey = x.attrib.values()[0].encode( 'utf-8' )
			if x.text:
				sValue = x.text.encode( 'utf-8' )
			else:
				sValue = '' 
			dNodeResult[sKey] = sValue
		return dNodeResult


	def __Edit( self ):
		'''用来编辑最后结果'''
		edit = self.oTree.find( 'edit' )
		sBy = edit.find( './/value[@name="by"]' )
		sTime = edit.find( './/value[@name="time"]' )
		#print sBy
		#sTime = edit.find('time')
		sBy.text = '1'
		sTime.text = str( self.__Timestamp() )


	def __Comparetime( self, sTime, Content, elem, dNodeResult ):
		'''比对时间,当时间存在并且在网页里面能找到，才不用把
		update置为1
		'''

		if sTime != '':
			print sTime
			sTime = sTime.strip()			
			if re.search( sTime, Content ):
				elem.find( './value[@name="update"]' ).text = '0'				
			else :
				elem.find( './value[@name="update"]' ).text = '1'
				xmlparse.z += 1
				print '券商%s需要更新了\n' % dNodeResult['name']
		else:
			elem.find( './value[@name="update"]' ).text = '0'

	def  __CompareMD5( self, sMD5, sTime, Content, elem, dNodeResult ):
			i = 0
			sMD5 = sMD5.strip()
			try:
				if sMD5 != ''and sMD5 in Content:
					self.__Comparetime( sTime, Content, elem, dNodeResult )
					print '在'
				elif sMD5 == '':
					self.__Comparetime( sTime, Content, elem, dNodeResult )
				else:
					elem.find( './value[@name="update"]' ).text = '1'
					print '券商%s需要更新了\n' % dNodeResult['name']
					xmlparse.z += 1
				print '券商%s比对成功\n' % dNodeResult['name']
				return 1
			except Exception, e:
				print e
				print '券商%s比对失败\n' % dNodeResult['name']



		
	
	def __Compare( self ):
		'''比对时间和md5
		'''
		oRoot = self.oTree.getroot()
		i = 0#统计成功数字
		sum = len( self.oTree.findall( 'item' ) )
		for elem in self.oTree.findall( 'item' ):
			'''打开URL地址，获取HTML'''
			sContent = ''
			dNodeResult = self.ParserResult( elem )
			sUrl = dNodeResult['url']
			# print '开始比对券商%s.......' % dNodeResult['name']
			sMD5 = dNodeResult['md5']
			sTime = dNodeResult['date']
			print sMD5, sTime
			try:
				'''判断是不是属于JS的集合里面'''
				if sUrl in url_xpath:
					sContent = urlopen( url_xpath[sUrl] ).read()
				else:
					sContent = urlopen( sUrl ).read()
		
				'''是否需要转码'''
				try:
					Content = sContent.decode( 'gb2312' ).encode( 'utf-8' )
				except Exception, e:
					if str( e ).startswith( "'gb2312'" ):
						Content = sContent
					else:
						Content = sContent
				#print Content
				'''
				调用比对函数
				'''			
				if self.__CompareMD5( sMD5, sTime, Content, elem, dNodeResult ) == 1:
					i = i + 1
			except Exception, e:
				print e
				continue
		print '一共有%s个券商，成功了比对了%s个,%s家需要更新' % ( sum, i, xmlparse.z )
		
		
	def SaveXML( self ):
		'''保存XML修改结果'''
		self.__Compare()
		self.__Edit()
		self.oTree.write( self.sFilename, encoding = 'utf-8' )
				
'''主函数,需要把这里的XML替换成实际需要操作的XML'''		
if __name__ == '__main__':
	xml = xmlparse( 'D:\\softs\\baiducloud\\mycode\\gitdir\\python\\work\\dsfwt\\versionCheck.xml' )
	print 'xx'
	a = time.time()
	xml.SaveXML()
	b = time.time()
	c = int( b - a )
	print '执行完毕一共用时%s秒' % c
		
