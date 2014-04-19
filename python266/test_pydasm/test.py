#encoding=utf-8
'''
Created on 2014年4月13日

@author: zhaoanhua
'''
import os


def main():
    
    pass

if __name__ == "__main__":
    print("------------------   begin   ------------------")
   
    print( u"【当前工作目录是：】\t" + os.getcwd() )
    print( u"【当前进程ID是：】\t" + str(os.getpid()) )
    print( "\n" )
    main()
   
    print("------------------    end    ------------------")

