#encoding=utf-8
'''
Created on 2014年4月11日

@author: zhaoanhua
'''
import os
import pefile
import struct
import sys
from random import random
import hashlib

class CPECrack(object):
    '''
    '''
    def __init__(self, strFilePath):
        self.strFilePath = strFilePath
        self.strFileTarget = "fake.dll"
        self.strFileRemovedSig = "RemovedSig_" + strFilePath
        self.pe = pefile.PE(strFilePath)
                
        self.uKey = 0x1D7A03FC
        pass
    
    def RemoveAllSignature(self):
        '''
        #去除PE文件信息 非关键信息（DOS头只保留e_lfanew，PE去除PE标志和区块信息的块名Name）
        '''
        # DOS_HEADER
        self.e_lfanew = self.pe.DOS_HEADER.e_lfanew
        self.pe.DOS_HEADER.e_magic = 0
        #self.data = list( self.pe.__data__ )
        #self.pe.__data__ = self.data
        
        # FILE_HEADER
        self.pe.NT_HEADERS.Signature = 0
        
        # SECTION
        for section in self.pe.sections:
            section.Name = ""
           
        # saved
        self.pe.write("RemovedSig_" + self.strFilePath)
        
    def writeWithEncrypto(self, aFile, strData):
        self.strPEAll = strData + self.strPEAll
        return
        aFile.write(strData)
        return
        #uKey = 0x1D7A03FC
        uLen = len(strData)
        if uLen % 4:
            print "the len(%d) of strData is invalidate..." % uLen
            sys.exit()
            
        for i in range( uLen / 4 ):
            strInt = strData[i*4:(i+1)*4]
            uInt = struct.unpack("I", strInt)[0]
            uInt = uInt ^ self.uKey
            strInt = struct.pack("I", uInt)
            aFile.write(strInt)
            
    def moveNT_HEADERS(self):
        self.nFileAndOption = 0x04 + 0x14 + self.pe.FILE_HEADER.SizeOfOptionalHeader
        self.nMySections = self.pe.FILE_HEADER.NumberOfSections * 0x20   #len(self.pe.sections.SECTION_HEADER)
        self.nNTSize = 0x08 + self.nFileAndOption + self.nMySections
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
        self.uFileSize = os.path.getsize("RemovedSig_" + self.strFilePath)
        with open("RemovedSig_" + self.strFilePath, "rb") as arFile:
            arData = arFile.read( self.uFileSize )
            
            with open("fake.dll", "wb") as awFile:
                # 新建的PE信息的字节流，清空。
                self.strPEAll = ""
                                
                # 写e_lfanew(4字节处理)
                print hex(self.pe.DOS_HEADER.e_lfanew)
                strlfanew = struct.pack("I", self.e_lfanew)
                #awFile.write(strlfanew)
                self.writeWithEncrypto(awFile, strlfanew)
                
                # 写文件NT大小 (unsigned int)
                strNTSize = struct.pack("I", (self.nNTSize + 0x10) - (self.nNTSize + 0x10)%0x10)
                '''
                #awFile.write(strNTSize)
                self.writeWithEncrypto(awFile, strNTSize)
                '''
                self.writeWithEncrypto(awFile, strNTSize)          # 占位
                
                # 写文件NT
                strFileAndOption = arData[self.e_lfanew : self.nFileAndOption + self.e_lfanew]
                #awFile.write(strNTData)
                self.writeWithEncrypto(awFile, strFileAndOption)
                
                # 写SECTIONS
                strSections = ""
                self.uFirstSecAlign = 0x7fffffff
                for sec in self.pe.sections:
                    self.uFirstSecAlign = min(self.uFirstSecAlign, sec.PointerToRawData)
                    print hex(self.uFirstSecAlign)
                    strSec = struct.pack("IIIIIIHHI", sec.Misc, sec.VirtualAddress, sec.SizeOfRawData, sec.PointerToRawData,
                                         sec.PointerToRelocations, sec.PointerToLinenumbers, sec.NumberOfRelocations,
                                         sec.NumberOfLinenumbers, sec.Characteristics)
                    strSections = strSec + strSections
                self.writeWithEncrypto(awFile, strSections)
                
                awFile.write(self.strPEAll)
                
                '''
                # 填充buffer大小
                uLeftLen = uFirstSecAlign - self.nNTSize - 4
                awFile.write(uLeftLen * chr(0))
                '''
                
                # 写入其它内容
                
 
                #awFile.write( arData[uFirstSecAlign:] )

    def UnDoWork(self):
        with open(self.strFileTarget, "rb") as arFile:
            with open("UnDoWork.dll", "wb") as awFile:
                pass
        pass
        
    def on_final(self):
        '''
        # 随机填充PE信息头部所有字节、填充hash; 填充原始文件中间部分; 填充加密的结尾self.strPEAll
        '''
        strHash = hashlib.md5(self.pe.sections[0].get_data()).digest()
        # 16字节对齐strPEAll,加密
        if len(self.strPEAll) % 0x10:
            self.strPEAll = ( " " * (0x10 - len(self.strPEAll) / 0x10) ) + self.strPEAll
            
        strPEAll_Encrypt = ""
        for i in range( len(self.strPEAll) / 0x10 ):
            for j in range(4):
                iKey = struct.unpack("I", strHash[j*4:(j+1)*4])[0]
                iData = struct.unpack("I", self.strPEAll[(i*0x10+j*4):(i*0x10+j*4)+4])[0]
                strPEAll_Encrypt += struct.pack("I", iKey ^ iData)
        # 随机填充PE信息头部所有字节
        lenFakePE = self.uFirstSecAlign
        lenBeginHash = 0x19
        strFakePE = ""
        
        for i in range(lenBeginHash):
            strFakePE += chr( int(random()*0xff) )
            
        strFakePE += strHash
        
        while len(strFakePE) < lenFakePE:
            strFakePE += chr( int(random()*0xff) )
        
        # 拷贝所有的节块
        self.strSections = ""
        with open(self.strFilePath, "rb") as aFile:
            nFileLen = os.path.getsize(self.strFilePath)
            print (nFileLen)
            strFileAll = aFile.read(nFileLen)
            self.strSections = strFileAll[self.uFirstSecAlign:nFileLen-len(self.strPEAll)]
            
        with open("final_" + self.strFilePath, "wb") as aFile:
            # 随机填充PE信息头部所有字节
            print len(strFakePE)
            print len(self.strSections)
            print len(strPEAll_Encrypt)
            aFile.write(strFakePE)
            aFile.write(self.strSections)
            aFile.write(strPEAll_Encrypt)
            pass
        pass
    
    def DoWork(self):
        self.RemoveAllSignature()
        
        self.moveNT_HEADERS()

        self.on_final()
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
