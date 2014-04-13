#encoding=utf-8
'''
Created on 2014-3-23
版本组成：
    1. 下载安装官网2.6.6版本（最新为2.6.9，可惜需要自己编译，暂时不会呢）
    2. 下载安装Pywinauto-0.4.2，只支持该版本及其以前版本（自带SendKeys）（python setup.py install）
    3. pywin32
@author: khz
'''
import os

def main():
    pass

if __name__ == "__main__":
    print("------------------   begin   ------------------")
    
    print( u"【当前工作目录是：】\t".encode("gb2312") + os.getcwd() )
    print( u"【当前进程ID是：】\t".encode("gb2312") + str(os.getpid()) )
    main()
    
    print("------------------    end    ------------------")
