################################################################################
# NAME 
#   CM_Log.py
#
# DESCRIPTION
#   This file maintains handling logging mechanism
# 
# HISTORY
#   dd-mm-yyyy - author - comment
#   23-12-2013 - Gatot Susilo - Creation
################################################################################
from __future__ import print_function
import sys
import os
from datetime import datetime
import traceback

###################
# Global Variables
###################
class CM_Log:
    def __init__(self,empty=True):
        self.logFh = dict()
        self.startTime = dict()
        self.errorWarningList = []
        if (empty == False):
            self.logFh['sys.stdout'] = sys.stdout

        self.consolePrompt              = "CONSOLE"
        self.enableConsoleLog           = True
        self.debugModeOnConsole         = True

    def console(self, msg):
        logFhList = self.logFh.values()

        for fh in logFhList:
            print("[%s] %s" %(self.consolePrompt, msg), file=fh)

    def info(self, msg, fh=None):
        if (fh != None):
            logFhList = [fh]
        else:
            logFhList = self.logFh.values()

        for fh in logFhList:
            if fh == sys.stdout and self.enableConsoleLog == False:
                continue
            print("[INFO] %s" %msg, file=fh)
    
    def warning(self, msg, fh=None):
        if (fh != None):
            logFhList = [fh]
        else:
            logFhList = self.logFh.values()
        self.errorWarningList.append(('WARNING', msg))

        for fh in logFhList:
            if fh == sys.stdout and self.enableConsoleLog == False:
                continue
            print("[WARNING] %s" %msg, file=fh )
    
    def error(self, msg, fh=None):
        if (fh != None):
            logFhList = [fh]
        else:
            logFhList = self.logFh.values()
            
        self.errorWarningList.append(('ERROR', msg))

        if self.enableConsoleLog == False:
            return

        for fh in logFhList:
            if fh == sys.stdout and self.enableConsoleLog == False:
                continue

            print("[ERROR] %s" %msg, file=fh)
            if fh != sys.stdout:
                traceback.print_stack(limit=5,file=fh)

    def debug(self, msg, fh=None):
        if (fh != None):
            logFhList = [fh]
        else:
            logFhList = self.logFh.values()

        for fh in logFhList:
            if fh == sys.stdout:
                if self.enableConsoleLog == False or self.debugModeOnConsole == False:
                    continue
            print("[DEBUG] %s" %msg, file=fh)
    
    def startLog(self, filename):
        fh = None
        filename = os.path.abspath(filename)
        if (filename in self.logFh):
            self.warning("Logfile >>%s<< was openned" %filename)
            return fh
        else:
            # prepare directory just in case does not exist
            dirname = os.path.dirname(filename)
            if dirname != '' and not os.path.exists(dirname):
                os.makedirs(dirname)
            
            fh = open(filename,"a+")
            self.startTime[filename] = datetime.now()
            now = str(self.startTime[filename])
            self.logFh[filename] = fh
            self.info("*** LOG Started: %s ***\n       >>%s<<" %(now,filename))
        # print (self.logFh, file=sys.stdout)
        return fh
    
    def stopLog(self,filename):
        filename = os.path.abspath(filename)
        if (filename in self.logFh):
            now = datetime.now()
            duration = now - self.startTime[filename]
            self.info("*** LOG Stopped: %s - Duration: %s ***\n       >>%s<<" %(now, duration, filename))
            del self.logFh[filename]
            return True
    
        return False
    
    def stopAllLog(self):
        rc = True
        for key in self.logFh.keys():
            if (key == 'sys.stdout'):
                continue
            if (self.stopLog(key) == False):
                rc = False
                
        return rc

###################
# Global Variables
###################
gCM_Log   = CM_Log(False)

######################
# Global Subroutines
######################
def console(msg):
    gCM_Log.console(msg)

def info(msg,fh=None):
    gCM_Log.info(msg,fh)

def warning(msg,fh=None):
    gCM_Log.warning(msg,fh)

def error(msg,fh=None):
    gCM_Log.error(msg,fh)

def debug(msg,fh=None):
    gCM_Log.debug(msg,fh)

def setConsolePrompt(prompt):
    gCM_Log.consolePrompt = prompt

def enableDebugModeOnConsole():
    gCM_Log.debugModeOnConsole = True

def disableDebugModeOnConsole():
    gCM_Log.debugModeOnConsole = False

def enableConsoleLog():
    gCM_Log.enableConsoleLog = True

def disableConsoleLog():
    gCM_Log.enableConsoleLog = False

def startLog(filename):
    return gCM_Log.startLog(filename)

def stopLog(filename):
    return gCM_Log.stopLog(filename)

def stopAllLog():
    return gCM_Log.stopAllLog()

def getErrorWarningList():
    return gCM_Log.errorWarningList

def header(msg = None):
    msg1 = traceback.extract_stack(None,2)[0][2]
    if (msg == None):
        info(msg1)
    else:
        info("%s - %s" %(msg1, msg))
    

