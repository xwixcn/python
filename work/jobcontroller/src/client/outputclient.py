#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

class outputclient(object):
    def __init__(self,basedir):
        self.basedir = basedir
        self.outputdir = os.path.join(self.basedir,'../output/')
        if not os.path.exists(self.outputdir):
            os.makedirs(self.outputdir)


    def flushoutputtofile(self,jobid,output):
        filename = self.__gen_filename(jobid)
        filename = os.path.join(self.outputdir,filename)
        outputfile = open(filename,'w')
        outputfile.write(output)
        outputfile.close()
    
    
    def __gen_filename(self,jobid):
        return 'jobid__' + str(jobid) + '__output'
    
    def getfinishedjoboutput(self,jobid):
        filename = self.__gen_filename(jobid)
        filename = os.path.join(self.outputdir,filename)
        print filename
        outputfile = open(filename,'r')
        output = outputfile.read()
        return 'output',output


if __name__ == '__main__':
    oclient = outputclient('/home/hudson/ymwu/jobcontroller/src/')
    oclient.flushoutputtofile(5,'aaa\nbbb\n')
    print oclient.getfinishedjoboutput(5)
