#encoding=utf-8
'''
Created on 2014年4月23日

@author: zhaoanhua
'''
import os
import sys
import struct
from pydbg.defines import DBG_CONTINUE

from khz_common.BinaryTools import mkString2Binary, ODBin2String2
from khz_common.khztools import khzLog
from khz_common.CPacketHookBase import CPacketHookBase

g_BufHexMap = {
               # 喊话（替换为敏感信息）
               "20 06 2A 40 00 02 00 00 00 37 00 37 00 00 00 00 00 ":
               "20 06 2A 40 00 02 00 00 00 16 59 02 63 00 00 00 00 ",
               # 任务（替换为之前的任务）
               "8A 05 C0 33 5A BE 98 00 00 ":
               "8A 05 C0 33 59 BE 98 00 00 ",
               # 购买物品
               "4E 05 61 2F 67 00 00 00 00 00 00 00 01 ":       # 红瓶（FC币子不够）
               "4E 05 61 2F 67 00 00 00 00 00 00 00 ff ",
               # 购买物品
               "4E 05 61 2F 77 00 00 00 00 00 00 00 01 ":       # 蓝瓶（不存在物品）
               "4E 05 61 2F ff 00 00 00 00 00 00 00 01 ",
               # 贩卖物品
               "8E 05 60 34 04 00 00 00 00 00 01 00 00 00 ":       # 装备包第一个物品（无法贩卖物品）
               "8E 05 60 34 04 00 00 00 ff 00 01 00 00 00 ",
               # 贩卖物品
               "8E 05 60 34 04 00 00 00 01 00 01 00 00 00 ":       # 装备包第一个物品（无法贩卖物品）
               "8E 05 60 34 ff 00 00 00 01 00 01 00 00 00 ",
               # 使用物品
               "09 09 18 87 E3 05 00 00 00 00 00 00 0B A3 E1 11 07 00 00 00 09 00 00 00 00 00 00 00 00 00 ":       # 血瓶level2(第九个物品)
               "09 09 18 87 E3 05 00 00 00 00 00 00 0B A3 E1 11 07 00 00 00 ff 00 00 00 00 00 00 00 00 00 ",        # 一样可以喝药，有唯一属性在里面
               # 装备物品
               "31 09 2E 8C 01 00 00 00 20 00 04 00 00 00 00 00 01 00 00 00 00 ":       # 脱下第一个物品
               "31 09 2E 8C 01 00 00 00 20 00 04 00 00 00 ff 00 ff 00 00 00 00 ",      # 物品放到第ff个位置（无法移动物品）
               "31 09 2E 8C 04 00 00 00 00 00 01 00 00 00 20 00 01 00 00 00 00":       # 装备第一个物品
               "31 09 2E 8C 04 00 00 00 00 00 01 00 00 00 20 00 ff 00 00 00 00",      # 正常装备
               # 天赋加点
               "2A 07 FB 54 D3 6D 6C 00 00 01 00 00 00 00 00 00 00 00 ":               # 学习技能夺命剪刀脚（可以正常学习技能）
               "2A 07 FB 54 D3 6D 6C 00 00 03 00 00 00 00 00 00 00 00 ",
               "2A 07 FB 54 D5 6D 6C 00 00 01 00 00 00 00 00 00 00 00 ":                # 正常学习技能
               "2A 07 FB 54 D5 6D 6C 00 00 ff 00 00 00 00 00 00 00 00 ",
               "2A 07 FB 54 D2 6D 6C 00 00 01 00 00 00 00 00 00 00 00 ":                # 未定义错误
               "2A 07 FB 54 D4 6D 6C 00 00 ff 00 00 00 00 00 00 00 00 ",
               # 强化物品（手）
               "A7 06 A1 4B 7B 08 00 00 00 00 00 00 3A A5 E1 11 00 00 00 00 05 ":
               "A7 06 A1 4B 7B 08 00 00 00 00 00 00 3A A5 E1 11 00 00 00 00 ff ",
               # 切换地图
               "FE 08 C7 8B BA C3 00 00 05 00 00 00 ":              # 0-1 -> 1-2
               "FE 08 C7 8B BB C3 00 00 06 00 00 00 ",
               "FE 08 C7 8B B9 C3 00 00 06 00 00 00 ":              # 1-0 -> 1-2
               "FE 08 C7 8B BB C3 00 00 06 00 00 00 ",
               "FE 08 C7 8B BB C3 00 00 06 00 00 00 ":              # 1-2 -> 1-3
               "FE 08 C7 8B BD C3 00 00 06 00 00 00 ",
               # 付费移动
               "B1 05 BA 35 05 00 00 00 07 00 00 00 ":              # 2-0 -> 2--1（猜测）            村庄移动信息错误
               "B1 05 BA 35 04 00 00 00 07 00 00 00 ",
               "B1 05 BA 35 07 00 00 00 05 00 00 00 ":              # 0-2 -> 0-ff（猜测）            移动村庄费用信息错误
               "B1 05 BA 35 ff 00 00 00 05 00 00 00 ",
               "B1 05 BA 35 07 00 00 00 05 00 00 00 ":              # 0-2 -> 0-3（猜测）
               "B1 05 BA 35 14 00 00 00 05 00 00 00 ",
               "B1 05 BA 35 07 00 00 00 06 00 00 00 ":              # 1-2 -> x-x（猜测）
               "B1 05 BA 35 08 00 00 00 06 00 00 00 ",
               "B1 05 BA 35 07 00 00 00 11 00 00 00 ":              # 1-2 -> x-x（猜测）
               "B1 05 BA 35 05 00 00 00 06 00 00 00 ",
               # 进入高级别副本
               "3A 07 9F 55 01 00 01 00 00 00 07 00 00 00 0A 00 00 00 07 00 00 00 08 00 00 00 09 00 00 00 0A 00 00 00 28 00 00 00 2A 00 00 00 2D 00 00 00 2E 00 00 00 30 00 00 00 29 00 00 00 ":
               "3A 07 9F 55 01 00 01 00 00 00 09 00 00 00 0A 00 00 00 07 00 00 00 08 00 00 00 09 00 00 00 0A 00 00 00 28 00 00 00 2A 00 00 00 2D 00 00 00 2E 00 00 00 30 00 00 00 29 00 00 00 ",
               "C5 06 AC 4D 08 00 07 00 00 00 01 05 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 ":
               "C5 06 AC 4D 08 00 09 00 00 00 01 05 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 ",
               }
g_BufMap = dict()

class CPacketHooks(CPacketHookBase):
    '''
    
    '''
    def __init__(self, strGameExeName):
        CPacketHookBase.__init__(self, strGameExeName)
        pass
    pass

    @staticmethod
    def fnHook_Encrypt( dbg, args ):
        if not CPacketHookBase.isActiveDbg():
            dbg.debugger_active = False
            return DBG_CONTINUE
         
        hSocket = 0
        pBuf = args[1]
        nLen = args[2]
        # 获得函数返回地址
        strBuf = dbg.read_process_memory(dbg.context.Esp, 4)
        addrRetFun = struct.unpack("I", strBuf)[0]
        
        # 获得buffer内容
        lstMemory   = dbg.read_process_memory(pBuf, nLen)
        strBinary   = mkString2Binary(lstMemory, nLen)
        
        # 过滤心跳包
        if addrRetFun == 0x008C550C:
            return DBG_CONTINUE
        if (nLen == 0x0010) or (strBinary == "61 08 4C 75 03 00 00 00 02 15 FD 41 D3 FC AE 43 "):
            return DBG_CONTINUE
        if (nLen == 0x0004) or (strBinary == "7E 04 EB 23 "):
            return DBG_CONTINUE
        
        if g_BufMap.has_key(lstMemory):
            dbg.write_process_memory(pBuf, g_BufMap[lstMemory])

        
        strFunName  = sys._getframe().f_code.co_name

        # 组合strLog
        strLog = CPacketHookBase.m_strLogFormat % (dbg.h_thread, strFunName, addrRetFun,
                           hSocket, nLen, pBuf, strBinary)
        khzLog(strLog)
        return DBG_CONTINUE
        pass
    
    def FCHook(self):
        '''
        008C425C    51              push ecx                                     ; ？？？
        008C425D    8D43 04         lea eax,dword ptr ds:[ebx+0x4]
        008C4260 >  57              push edi                                     ; 长度(总长度-8)
        008C4261 >  50              push eax                                     ; 输入buffer
        008C4262    50              push eax                                     ; 输出buffer
        008C4263 >  E8 98370D00     call 00997A00                                ; 加密函数
        '''
        addrEncrypt = 0x00997A00
        '''加密前封包：edi为封包大小，eax为buffer地址'''
        self.hooks.add( self.dbg, addrEncrypt, 4, CPacketHooks.fnHook_Encrypt, None)


def main():
    for strSrc in g_BufHexMap.items():
        print strSrc[0]
        strKey = ODBin2String2(strSrc[0])
        print strKey
        print strSrc[1]
        strVal = ODBin2String2(strSrc[1])
        print strVal
        g_BufMap[strKey]=strVal

    aFC = CPacketHooks("FightersClub.exe")
    #aFC.SetDefaultHook()
    aFC.FCHook()
    aFC.run()
    pass

if __name__ == "__main__":
    print("------------------   begin   ------------------")
    
    print( u"【当前工作目录是：】\t" + os.getcwd() )
    print( u"【当前进程ID是：】\t" + str(os.getpid()) )
    print( "\n" )
    main()
   
    print("------------------    end    ------------------")

