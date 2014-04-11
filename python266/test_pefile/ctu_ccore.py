#encoding=utf-8
'''
Created on 2014年4月11日

@author: zhaoanhua
'''
import os
import pefile
import struct

class CPECrack(object):
    '''
    '''
    def __init__(self, strFilePath):
        self.strFilePath = strFilePath
        self.pe = pefile.PE(strFilePath)
        pass
    
    def RemoveAllSignature(self):
        # DOS_HEADER
        #print self.pe.DOS_HEADER
        self.e_lfanew = self.pe.DOS_HEADER.e_lfanew
        '''
        self.data = self.pe.__data__
        print hex(id(self.data))
        print hex(id(self.pe.__data__))
        self.data = list( self.pe.__data__ )
        print hex(id(self.data))
        print hex(id(self.pe.__data__))
        '''
        self.data = list( self.pe.__data__ )
        self.pe.__data__ = self.data
        #return
        #self.pe2 = pefile.PE(data = self.data, fast_load = True)
    
        for i in range(self.e_lfanew):
            self.data[i] = chr(0)
        
        self.pe.DOS_HEADER.e_magic = pefile.IMAGE_DOS_SIGNATURE
        self.pe.DOS_HEADER.e_lfanew = self.e_lfanew
        self.pe.DOS_HEADER.e_magic = 0
        
        # FILE_HEADER
        self.pe.NT_HEADERS.Signature = self.e_lfanew
        
        # SECTION
        for section in self.pe.sections:
            section.Name = ""
            
    def moveNT_HEADERS(self):
        self.nNTSize = 0x04 + 0x14 + self.pe.FILE_HEADER.SizeOfOptionalHeader + \
                self.pe.FILE_HEADER.NumberOfSections * 0x28   #len(self.pe.sections.SECTION_HEADER)
        print hex(self.nNTSize)
        
        '''
        nIndex = 0
        while(nIndex < self.nNTSize):
            self.data[nIndex] = self.data[nIndex + self.e_lfanew]
            nIndex = nIndex + 1
            #print hex(nIndex)
        print self.e_lfanew
        for i in range(4):
            self.data[self.nNTSize + i] = chr((self.e_lfanew >> (i*8)) & 0xff)
            print ord(self.data[self.nNTSize + i])
        '''
            
        #print self.data
        with open("Cracked_" + self.strFilePath, "rb") as arFile:
            arData = arFile.read( os.path.getsize("Cracked_" + self.strFilePath) )
            #return
            with open("fake.dll", "wb") as awFile:
                awFile.write(arData[self.e_lfanew : self.nNTSize+self.e_lfanew])
        #struct.pack()


        
    def on_final(self):
        self.pe.write("Cracked_" + self.strFilePath)
        pass
    
    def DoWork(self):
        self.RemoveAllSignature()
        self.on_final()
        
        self.moveNT_HEADERS()
        #return
        


def main():
    strFilePath = "ccore.dll"
    peCrack = CPECrack(strFilePath)
    peCrack.DoWork()
    pass

if __name__ == "__main__":
    print("------------------   begin   ------------------")
    
    print( u"【当前工作目录是：】\t".encode("gb2312") + os.getcwd() )
    print( u"【当前进程ID是：】\t".encode("gb2312") + str(os.getpid()) )
    print("\n")
    main()
    
    print("------------------    end    ------------------")
