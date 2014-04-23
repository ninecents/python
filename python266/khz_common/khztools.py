#encoding=utf-8
'''
Created on 2014年4月23日

@author: zhaoanhua
'''
import os
import time
import ctypes
import sys

def khzLog(strLog):
    '''
    
    :param strLog: unicode string
    '''
    #return
    atm = time.localtime()
    #strTime = u"%02d-%02d-%02d" % (atm.tm_year, atm.tm_mon, atm.tm_mday)
    strTime = u"%02d:%02d:%02d" % (atm.tm_hour, atm.tm_min, atm.tm_sec)
    
    strOut = u"[khz]\t" + strTime + u'\t' #+ unicode(__name__) + u'\t'
    strOut += strLog
    
    # 输出内容
    print(strOut.encode("gb2312"))
    ctypes.windll.Kernel32.OutputDebugStringW( strOut )
    '''
    ctypes.windll.Kernel32.OutputDebugStringW( strLog )
    '''
    pass

def getProcID(dbg, strProcName):
    # Quick and dirty process enumeration to find firefox.exe
    for (pid, name) in dbg.enumerate_processes():
        #print pid,name
        if name.lower() == strProcName:
            return pid
    
    print("[*]no process named %s, exit process." % strProcName)
    sys.exit()
    pass

class clsNone(object):
    def __init__(self):
        print sys._getframe().f_code.co_name
        pass
    
def get_cur_info():
    print sys._getframe().f_code.co_filename  #当前文件名，可以通过__file__获得
    print sys._getframe().f_code.co_name  #当前函数名
    print sys._getframe().f_lineno #当前行号

def main():
    get_cur_info()
    clsNone()
    pass

if __name__ == "__main__":
    print("------------------   begin   ------------------")
   
    print( u"【当前工作目录是：】\t" + os.getcwd() )
    print( u"【当前进程ID是：】\t" + str(os.getpid()) )
    print( "\n" )
    main()
   
    print("------------------    end    ------------------")

