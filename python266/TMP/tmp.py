#encoding=utf-8
'''
Created on 2014-3-23
版本组成：
    1. 下载安装官网2.6.6版本（最新为2.6.9，可惜需要自己编译，暂时不会呢）
    2. 下载安装Pywinauto-0.4.2，只支持该版本及其以前版本（自带SendKeys）（python setup.py install）
    3. pywin32
@author: khz
'''
import ctypes
import os
#import pydbg
#import sqlite3
#import win32api

def khzLog(strLog):
    ctypes.windll.Kernel32.OutputDebugStringA( "[khz]" + strLog)
    pass

def main():
    #win32api.MessageBox(0, "khz")
    pass

if __name__ == "__main__":
    khzLog("------------------   begin   ------------------")
    
    #khzLog( str(os.getpid()) )
    #sys.path.append(r'E:\__STUDY__\__SVN__\svn999\study\python266')
    main()
    
    khzLog("------------------    end    ------------------")
