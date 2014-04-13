############################<Empty>
#encoding=utf-8
'''
Created on 2014-4-12

@author: khz
'''
import sqlite3
import os
import win32api
import pydbg
import pydasm

def example_pydasm():
    buffer = '\x90\x31\xc9\x31\xca\x31\xcb'

    offset = 0
    while offset < len(buffer):
       i = pydasm.get_instruction(buffer[offset:], pydasm.MODE_32)
       print pydasm.get_instruction_string(i, pydasm.FORMAT_INTEL, 0)
       if not i:
         break
       offset += i.length

def main():
    #win32api.MessageBox(0, "khz")
    #print dir(pydasm)
    print help(pydasm.get_operand_string)
    example_pydasm()
    pass

if __name__ == "__main__":
    print("------------------   begin   ------------------")
   
    print( u"【当前工作目录是：】\t".encode("gb2312") + os.getcwd() )
    print( u"【当前进程ID是：】\t".encode("gb2312") + str(os.getpid()) )
    print( "\n" )
    main()
   
    print("------------------    end    ------------------")

