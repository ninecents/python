############################<Empty>
#encoding=utf-8
'''
Created on 2014年4月15日

@author: zhaoanhua
'''
import os
import struct
import ctypes
import time

def khzLog(strLog):
    #return
    atm = time.localtime()
    strTime = u"%02d-%02d-%02d" % (atm.tm_year, atm.tm_mon, atm.tm_mday)
    strOut = u"[khz]\t" + strTime + u'\t' + unicode(__name__) + u'\t'
    strOut += strLog
    print(strOut.encode("gb2312"))
    ctypes.windll.Kernel32.OutputDebugStringW( strOut )
    '''
    ctypes.windll.Kernel32.OutputDebugStringW( strLog )
    '''
    pass

class CharacterState():
    pass

def getCharacterState(): 
    '''
    血值 基址         0x02F7C020
       +4: 魔力值
       +8: 持久力 
       +C:血值上限
       +10:魔力值上限
       +14:持久力上限 1000
       +1C：善恶度
       +18：当前经验值
       +20：升级到下一级所需经验值
       +24: 灵兽 持有数量 上限2
       +2C：历练值
       +30：心
       +34：力
       +38：体
       +3C：身
       +40：__end__

    '''
    addrBase = 0x02F7C020
    buf = ctypes.create_string_buffer("123412341234123412345", 40 + 4)
    addrBase = id(buf)
    '''
    # 方法一：ctypes winapi 访问自己进程空间的内存
    print type(id(buf)), hex(id(buf))
    # WINBASEAPI BOOL WINAPI ReadProcessMemory( __in HANDLE hProcess, __in LPCVOID lpBaseAddress, __out_bcount_part(nSize, *lpNumberOfBytesRead) LPVOID lpBuffer, __in SIZE_T nSize, __out_opt SIZE_T * lpNumberOfBytesRead )
    ctypes.windll.Kernel32.ReadProcessMemory( None, addrBase, buf, 20, None )
    astruct = struct.unpack("IIIII", buf[:20])
    khzLog("%08x,%08x" % (astruct[0], astruct[1]))
    #khzLog("%d" % len(buf))
    '''
    # 方法二：ctype string_at 访问自己进程空间的内存
    strStat = ctypes.string_at(addrBase, 0x40)
    lstStat = struct.unpack("II", strStat[:8])
    strLog = u"血值：%d, 魔力值: %d" % (lstStat[0], lstStat[1])

    khzLog(strLog)

def test():
    khzLog(u"------------------    test    ------------------")

def main():
    print("[khz]    2014-04-23    __main__    血值：1, 魔力值: 40587536")
    khzLog(u"------------------   begin   ------------------")
    getCharacterState()
    #test()
    khzLog(u"------------------    end    ------------------")
    pass

if __name__ == "__main__":
    print("------------------   begin   ------------------")
   
    print( u"【当前工作目录是：】\t" + os.getcwd() )
    print( u"【当前进程ID是：】\t" + str(os.getpid()) )
    print( u"\n" )
    main()
   
    print("------------------    end    ------------------")
else:
    pass
    #test()
    #main()
