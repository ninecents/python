#encoding=utf-8
'''
Created on 2014年4月23日

@author: zhaoanhua
'''
import os
from khz_common.CPacketHookBase import CPacketHookBase

class CPacketHooks(CPacketHookBase):
    def __init__(self, strGameExeName):
        CPacketHookBase.__init__(self, strGameExeName)
        pass
    pass


def main():
    aFC = CPacketHooks("FightersClub.exe")
    aFC.run()
    pass

if __name__ == "__main__":
    print("------------------   begin   ------------------")
    
    print( u"【当前工作目录是：】\t" + os.getcwd() )
    print( u"【当前进程ID是：】\t" + str(os.getpid()) )
    print( "\n" )
    main()
   
    print("------------------    end    ------------------")

