#encoding=utf-8
'''
Created on 2014年4月11日

@author: zhaoanhua
'''

import os, string, shutil,re
import pefile ##记得import pefile

def atest():
    PEfile_Path = r"ccore.dll"
    
    pe = pefile.PE(PEfile_Path)
    print PEfile_Path
    print pe

def btest():
    PEfile_Path = r"ccore.dll"
    
    pe = pefile.PE(PEfile_Path)
    print PEfile_Path
    
    for section in pe.sections:
        print section.Name
        break

def ctest():
    PEfile_Path = r"ccore.dll"
    
    pe = pefile.PE(PEfile_Path)
    print PEfile_Path
    
    for importeddll in pe.DIRECTORY_ENTRY_IMPORT:
        print importeddll.dll
        ##or use
        #print pe.DIRECTORY_ENTRY_IMPORT[0].dll
        for importedapi in importeddll.imports:
            print importedapi.name
        ##or use
        #print pe.DIRECTORY_ENTRY_IMPORT[0].imports[0].name


def main():
    atest()
    pass

if __name__ == "__main__":
    print("------------------   begin   ------------------")
    
    print( u"【当前工作目录是：】\t" + os.getcwd() )
    print( u"【当前进程ID是：】\t" + str(os.getpid()) )
    print("\n")
    main()
    
    print("------------------    end    ------------------")
