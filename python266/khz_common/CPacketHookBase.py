#encoding=utf-8
'''
Created on 2014年4月23日

@author: zhaoanhua
'''
import os
import utils
from pydbg import *
from pydbg.defines import *

from khz_common import khztools
from khz_common.khztools import khzLog
import struct
from khz_common.BinaryTools import *
import sys
import ctypes


class CPacketHookBase(object):
    '''
    # 包结构：        （时间）    h_thread    函数名称    函数返回地址    hSocket    包大小    包地址    包内容        

    '''
    m_strLogFormat = u"\t".join( list([u"%08X", u"%s", u"%08X",       # h_thread    函数名称    函数返回地址 
                                      u"%04X", u"%08X", u"%08X", u"%s"]) )   # hSocket    包大小    包地址    包内容   
    
    def __init__(self, strGameExeName):
        self.dbg    = pydbg()
        dbg         = self.dbg
        # 设置断点容器
        self.hooks       = utils.hook_container()

        # 获得进程ID
        #nPID = khztools.getProcID(self.dbg, strGameExeName)             #"FightersClub.exe"
        nPID = None
        for pid, name in dbg.enumerate_processes():
            #print pid,name
            if name.lower() == strGameExeName.lower():
                nPID = pid
        if not nPID:
            khztools.khzLog(u"[*]目标进程ID为空，退出程序")
            exit(-1)
        else:
            khztools.khzLog(u"[*]目标进程ID为:%d" % nPID)
            
        self.dbg.attach(nPID)
        pass
    
    def myPacketLog(self):
        self.dbg.h_thread
        pass
    

    #查看是否应该退出程序了
    @staticmethod
    def isActiveDbg():
        strPath = r"E:\__STUDY__\__SVN__\github\ninecents\python\trunk\python266\__cfg__" '\\'
        try:
            with open(strPath + "isActiveDbg", "r") as aFile:
                return aFile.readline() == "True"
        except:
            return False
        
        return False        #读取失败则返回False，退出调试
    
    def checkActiveDbg(self):
        self.dbg.debugger_active = CPacketHookBase.isActiveDbg()
        
        return self.dbg.debugger_active

    @staticmethod
    def fnAPI_send( dbg, args ):
        '''
        int send(
          __in  SOCKET s,
          __in  const char* buf,
          __in  int len,
          __in  int flags
        );

        '''
        print(args)
        hSocket = args[0]
        pBuf = args[1]
        nLen = args[2]
        
        lstMemory = dbg.read_process_memory(pBuf, nLen)
        strFunName = sys._getframe().f_code.co_name
        strBuf = dbg.read_process_memory(dbg.context.Esp, 4)
        addrRetFun = struct.unpack("I", strBuf)[0]
        strLog = CPacketHookBase.m_strLogFormat % (dbg.h_thread, strFunName, addrRetFun,
                           hSocket, nLen, pBuf, mkString2Binary(lstMemory, nLen))
        khzLog(strLog)
        return DBG_CONTINUE
        pass
    
    @staticmethod
    def fnAPI_WSASend( dbg, args ):
        '''
        int WSASend(
          __in   SOCKET s,
          __in   LPWSABUF lpBuffers,
          __in   DWORD dwBufferCount,
          __out  LPDWORD lpNumberOfBytesSent,
          __in   DWORD dwFlags,
          __in   LPWSAOVERLAPPED lpOverlapped,
          __in   LPWSAOVERLAPPED_COMPLETION_ROUTINE lpCompletionRoutine
        );
        '''
        '''判断是否退出调试状态'''
        '''
        dbg.debugger_active = GeneralTools.isActiveDbg()
        if not dbg.debugger_active:
            return DBG_CONTINUE
        '''
        if args[2] > 1:
            khzLog(u"------------------   WARNNING - (args[2] > 1)   ------------------")
        
        strWSABUF = dbg.read_process_memory( args[1], 0x08 )
        lstParams = struct.unpack("LL", strWSABUF)
        nLen = lstParams[0]
        pBuf = lstParams[1]
        '''获得发送的WSABUF.buf'''
        lstMemory = dbg.read_process_memory( pBuf, nLen )
        
        # mkString2Binary
        strFunName = sys._getframe().f_code.co_name
        #strBuf = ctypes.string_at(dbg.context.Esp, 4)
        strBuf = dbg.read_process_memory(dbg.context.Esp, 4)
        addrRetFun = struct.unpack("I", strBuf)[0]
        strLog = CPacketHookBase.m_strLogFormat % (dbg.h_thread, strFunName, addrRetFun,
                           args[0], nLen, pBuf, mkString2Binary(lstMemory, nLen))
        khzLog(strLog)
        return DBG_CONTINUE
        pass
    
    def SetDefaultHook(self):
        '''WSASend的API断点'''                     # (u"fnAPI_WSASend_address addr is 0x%08X" % fnAPI_WSASend_address)
        fnAPI_address = self.dbg.func_resolve_debuggee("Ws2_32", "WSASend")
        self.hooks.add( self.dbg, fnAPI_address, 7, CPacketHookBase.fnAPI_WSASend, None)

        '''send的API断点'''                     # (u"fnAPI_WSASend_address addr is 0x%08X" % fnAPI_WSASend_address)
        fnAPI_address = self.dbg.func_resolve_debuggee("Ws2_32", "send")
        self.hooks.add( self.dbg, fnAPI_address, 4, CPacketHookBase.fnAPI_send, None)

    def run(self):
        # 循环执行调试过程
        self.dbg.run()
        pass
    
    pass 

def main():
    aHookTest = CPacketHookBase("Evernote.exe")
    aHookTest.SetDefaultHook()
    aHookTest.run()
    pass

if __name__ == "__main__":
    print("------------------   begin   ------------------")
   
    print( u"【当前工作目录是：】\t" + os.getcwd() )
    print( u"【当前进程ID是：】\t" + str(os.getpid()) )
    print( "\n" )
    main()
   
    print("------------------    end    ------------------")

