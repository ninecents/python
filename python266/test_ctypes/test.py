#encoding=utf-8
'''
Created on 2014-4-20

@author: khz
'''

import os

from ctypes import *


def testArrays():
    class POINT(Structure):
        _fields_ = ("x", c_int), ("y", c_int)
    
    class MyStruct(Structure):
        _fields_ = [("a", c_int),
                   ("b", c_float),
                   ("point_array", POINT * 5)]
    
    print len(MyStruct().point_array)
    
    TenPointsArrayType = POINT * 10
    print TenPointsArrayType
    arr = TenPointsArrayType()
    for pt in arr:
        print pt.x, pt.y


def main():
    testArrays()
    pass

if __name__ == "__main__":
    print("------------------   begin   ------------------")
   
    print( u"【当前工作目录是：】\t".encode("gb2312") + os.getcwd() )
    print( u"【当前进程ID是：】\t".encode("gb2312") + str(os.getpid()) )
    print( "\n" )
    main()
   
    print("------------------    end    ------------------")

