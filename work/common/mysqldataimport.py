#-*-coding:utf-8
'''
用来从excel导入数据到mysql
'''
import MySQLdb
import xlrd
import hashlib
class DataImport:
	def __init__(self,host,user,passwd,db):
		self.host=host
		self.user=user
		self.passwd=passwd
		self.db=db

	def conn(self):
		try:
			self.conn=MySQLdb.connect(self.host,self.user,self.passwd,self.db,charset='utf8')
		except MySQLdb.Error,e:
			print e.message
			sys.exit(1)

	def closeconn(self):
		self.conn.close()

	def importdata(self,xlsfile):
		if xlsfile.split(".")[-1] not in ["xls","csv"]:
			print 'sorry,the fileformat is not correct'
			sys.exit(1)
		print xlsfile
		data=self.parsexls(xlsfile)
 		self.conn()
 		cursor=self.conn.cursor()
 		i=0
 		for k,v in data.iteritems():
 			tagid=int(k)
 			for case,standcase in v.iteritems():
 				casemd5 = hashlib.md5(case).hexdigest()
 				try:
 					cursor.execute("insert into backend_case_info(name,md5,samecase) values(%s,%s,%s)",(case,casemd5,standcase) )
 					cursor.execute("select id from backend_case_info order by id desc limit 1")
 					caseid=int(cursor.fetchone()[0])
 					cursor.execute("insert into backend_case_taginfo(caseId_id,tagId_id) values(%s,%s)",(caseid,tagid))
 					print caseid
 					i+=1
 				except Exception, e:
 					print case+"failed!"
 					continue
 		print i
 		self.closeconn()

		

	def parsexls(self,xlsfile):
		if xlsfile.split(".")[-1] not in ["xls","csv"]:
			print 'sorry,the fileformat is not correct'
			sys.exit(1)
		excel=xlrd.open_workbook(xlsfile)
		case={}
		print excel.nsheets
		for nsheet in range(0,excel.nsheets):
			sheet=excel.sheet_by_index(nsheet)
			tagid=int(sheet.name)
			casedic={}
			print sheet.nrows
			a=[]
			for i in range(1,sheet.nrows):
				case1=sheet.cell(i,0).value.encode("utf-8")
				standcase=sheet.cell(i,1).value.encode("utf-8")
				if case1 not in a:
					a.append(case1)
				else:
					print i
				casedic[sheet.cell(i,0).value.encode("utf-8")]=sheet.cell(i,1).value.encode("utf-8")
			case[tagid]=casedic
		return case

				


if __name__ == '__main__':
	db=DataImport("172.20.23.75","root","123456","ontology")
	db.importdata("C:\\Users\\RINA\\Desktop\\Book1.xls")
	#db.parsexls("case4.xls")
