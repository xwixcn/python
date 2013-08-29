#-*-coding:utf-8
import logging

log=logging.getLogger(__name__)

class Assert(object):



	def __init__(self,dataA,dataB):
		self.dataA=dataA
		self.dataB=dataB

	def execute(self):
		return True

	def getFalseResult(self):
		pass




class IncludeAssert(Assert):

	def __init__(self,dataA,dataB):
		super(IncludeAssert,self).__init__(dataA,dataB)
		self.__assertlist()
		self.flag=True
		self.intersection=[]
		self.disintersection=[]

	def execute(self):
		self.flag=self.__Intersection()
		return self.flag


	def getFalseResult(self):
		if self.flag==True:
			return None
		else:
			if len(self.dataA)==0:
				return 'wencai data is zero!'
			else:
				return '{0} not in wencai data!'.format\
				(",".join(list(self.disintersection)).encode("utf-8"))


	def __Intersection(self):
		self.disintersection=self.setdataB.difference(self.setdataA)
		if self.disintersection:
			return False
		else:
			return True



	def __assertlist(self):
		if isinstance(self.dataA, list) and isinstance(self.dataB,list):
			self.setdataA=set(self.dataA)
			self.setdataB=set(self.dataB)
		else:
			raise AssertionError,"data must be list type"



