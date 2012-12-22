#####################################
# use logging module as below
# from regressLogger import log
# then use log.debug to log message
#
######################################

import os
import logging
import logging.handlers

filepath=os.path.realpath(__file__).rstrip(__file__.split('/')[-1])
LOGPATH =os.path.join(filepath,'log')
if not os.path.exists(LOGPATH):
    os.makedirs(LOGPATH)
def create_log(logname):
    LOGFILE = os.path.join(LOGPATH,logname)
    log = logging.getLogger('project')
    if len(log.handlers) == 0:
        log.setLevel(logging.DEBUG)
        LOG_FILENAME = os.path.join(os.path.dirname(__file__),\
            LOGFILE.replace('\\','/'))
        handler = logging.handlers.RotatingFileHandler(LOG_FILENAME,maxBytes=10240000,encoding='utf-8')
        formatter = logging.Formatter('%(asctime)s\t%(levelname)s\t[%(module)s.%(funcName)s]\t%(message)s')
        handler.setFormatter(formatter)
        log.addHandler(handler)
    return log

