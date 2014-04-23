#encoding=utf8
'''
Created on 2014年3月6日

@author: zhaoanhua
'''
import struct
    
def mkStruct2Binary(pBuffer, nSize):
    '''
    #将从内存获得的pBuffer转化为2禁止输出
    :param pBuffer:struct类型
    :param nSize:字节数
    '''
    strFormat = "B" * nSize
    aList = struct.unpack(strFormat, pBuffer)
    #print(aList)
    
    strFormat = "%02X " * nSize
    strRet = strFormat % tuple(aList)
    #print strRet
    return strRet
    #return ""
 
def mkString2Binary(pszBuffer, nSize=None):
    '''
    将从内存获得的pszBuffer转化为2禁止输出
    :param pszBuffer:struct类型
    :param nSize:字节数
    '''
    #初始化nSize
    if nSize == None:
        nSize = len(pszBuffer)
    aList = list()
    for i in range(nSize):
        aList.append( ord(pszBuffer[i]) )
    #print(aList)
    
    strFormat = "%02X " * nSize
    strRet = strFormat % tuple(aList)
    #print strRet
    return strRet
    #return ""
    
def ODBin2String(strOrg):
    strRet = ""
    
    strOrg = strOrg.replace(" ", "")
    strOrg = strOrg.replace("\n", "")
    print len(strOrg), strOrg
    if len(strOrg) % 2 != 0:
        print("err...not odd binary")
        return None
    for cnt in range(len(strOrg) / 2):
        strTmp = strOrg[cnt*2:(cnt*2+2)]
        print strTmp
        strRet = strRet + r'0x%s, ' % strTmp
    return "unsigned char *szMem[] = {%s};" % strRet

def main():
    strOrg = '''
    D7 33 D0 D0 07 29 FF C6 E3 7A 08 4E 4A 5D 73 31 D8 72 F2 AF E3 2E E8 FC 0D 86 31 35 4F 7D 6C 7E 5D 51 32 25 00 F6 64 2F 3E 68 14 0E 06 96 C4 DD C1 39 D2 13 3E 0B A7 0F 59 4A 52 24 36 5A DD 0D 29 77 00 CF A3 A9 32 2A BE 35 66 D0 AD 24 36 29 13 64 68 9C 9C 2B 15 34 43 21 90 59 5D F2 96 63 B4 A5 C3 E1 10 8E 79 69 E9 16 32 C3 FE 13 53 D1 5D CD EE 97 E6 66 BB 1B 9E 52 C7 75 D5 52 CE 09 49 96 36 C2 23 70 48 92 68 95 D4 3B ED 65 93 3D 6B 03 1E D6 34 72 71 66 7D CF FD 64 BD BA 0B CD 4D 76 DC 72 11 15 7A F2 D8 C7 82 91 AC 75 60 2F A9 4E F5 9C 87 26 AA B4 90 9F 72 8A 60 92 8B EA BE 3E C3 66 6E D0 B8 62 67 54 43 81 29 CD 80 0A BB 5E 76 E8 F7 21 3D 44 DB FA 78 F0 16 73 3E 9E 83 AC E4 ED 3E 2B 53 B3 A0 50 1B 11 1D BA F2 BF C6 68 33 DF 95 76 73 35 B6 BC D4 7D 84 23 2C 3F  

    '''
    print (ODBin2String(strOrg))
    pass

if __name__ == '__main__':
    main()
    pass
