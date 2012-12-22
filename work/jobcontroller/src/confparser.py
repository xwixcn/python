#!/usr/bin/env python
# -*- coding: utf-8 -*-


from ConfigParser import ConfigParser
from ConfigParser import NoOptionError,NoSectionError

class confparser(object):

    def __init__(self):
        self.cfg = ConfigParser()
        self.cfg.read('conf/setting.ini')

    def getjobprecedure(self,jobname):
        procedure = self.__get(jobname,'procedure')
        return procedure

    def getprecedureenv(self,procedure):
        options=self.getserviceconfig(procedure)
        env="http://"+options["url"]+":"+options["port"]
        return env

    def getalljobs(self):
        jobs = self.__get('jobs','jobs')
        return jobs

    def getserviceconfig(self,servicename):
        options = self.__getitems(servicename)
        options = dict(options)
        rlt = {}
        for key, value in options.items():
            rlt[key] = value
        return rlt

    def __get(self,section,param):
        try:
            rlt = eval(self.cfg.get(section,param))
        except NoOptionError,e:
            print e
            rlt = ''
        return rlt

    def __getitems(self,section):
        try:
            rlt = self.cfg.items(section)
        except NoSectionError,e:
            print e
            rlt = ''
        return rlt
if __name__=="__main__":
    a=confparser()
    print a.getalljobs()
    print a.getserviceconfig("sentences")
    print a.getprecedureenv("sentences")
