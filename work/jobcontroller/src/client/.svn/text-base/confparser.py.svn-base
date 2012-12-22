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

    def getalljobs(self):
        jobs = self.__get('jobs','jobs')
        return jobs

    def getserviceconfig(self,servicename):
        options = self.__getitems(servicename)
        options = dict(options)
        rlt = {}
        for key, value in options.items():
            rlt[key] = eval(value)
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

