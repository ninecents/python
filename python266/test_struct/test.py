############################<Empty>
#encoding=utf-8
'''
Created on 2014年4月13日

@author: zhaoanhua
'''

import os
import struct


def main():
    astr = struct.pack('B4sII', 0x04, 'aaaa', 0x01, 0x0e)
    print astr
    # 'B4sII'  ------   有一个unsigned short、char[4], 2个unsigned int。其中s之前的数字说明了字符串的大小 。
    type, tag, version, length = struct.unpack('B4sll', str)
    print struct.unpack('B4sll', str)
    pass

if __name__ == "__main__":
    print("------------------   begin   ------------------")
   
    print( u"【当前工作目录是：】\t".encode("gb2312") + os.getcwd() )
    print( u"【当前进程ID是：】\t".encode("gb2312") + str(os.getpid()) )
    print( "\n" )
    main()
   
    print("------------------    end    ------------------")

'''
最近一段时间在看有关Python相关的知识，特别是其中关于网络通信的内容。在大部分的书本示例中，客户端和服务器端通信的内容都是文本信息，例如“hello world！”之类的信息。但是在实际应用中，我们看到的大部分数据时二进制数据，如“0x12345678”。所以这时候，就需要使用到Python中的struct来处理一下了。
         一、struct简介
       看到struct这么英文单词，大家应该并不陌生，因为c/c++中就有struct，在那里struct叫做结构体。在Python中也使用struct，这充分说明了这个struct应该和c/c++中的struct有很深的渊源。Python正是使用struct模块执行Python值和C结构体之间的转换，从而形成Python字节对象。它使用格式字符串作为底层C结构体的紧凑描述，进而根据这个格式字符串转换成Python值。
     二、主要函数
        struct模块中最主要的三个函数式pack()、unpack()、calcsize()。
     pack(fmt, v1, v2, ...)  ------ 根据所给的fmt描述的格式将值v1，v2，...转换为一个字符串。
     unpack(fmt, bytes)    ------ 根据所给的fmt描述的格式将bytes反向解析出来，返回一个元组。
     calcsize(fmt)             ------ 根据所给的fmt描述的格式返回该结构的大小。
     三、格式字符
    格式字符有下面的定义：
 Format              C Type                  Python        字节数
         x        pad byte        no value             1
         c        char    bytes of length 1             1
         b        signed char        integer             1
         B       unsigned char        integer             1
         ？       _Bool        bool             1
         h    
   short
    integer             2
         H       unsigned short        integer             2
         i       int        integer             4
         I       unsigned int        integer             4
         l       long        integer             4
         L       unsigned long        integer             4
        q       long long        integer             8
        Q       unsigned long long        integer             8
        f       float        float             4
        d       double        float             8
        s       char[]        bytes             1
        p       char[]        bytes             1
       P       void *        integer     
 注意： 1. c,s和p按照bytes对象执行转码操作，但是在使用UTF-8编码时，也支持str对象。
             2. ‘？’按照C99中定义的_Bool类型转码。如果该类型不可用，可使用一个char冒充。
             3. ‘q'和’Q‘仅在64位系统上有用。
         四.示例
     现在我们有了格式字符串，也知道了封装函数，那现在先通过一两个例子看一看。
      例一：比如有一个报文头部在C语言中是这样定义的
      struct header
      {
          unsigned short  usType;
          char[4]               acTag;
          unsigned int      uiVersion;
          unsigned int      uiLength;
      };
      在C语言对将该结构体封装到一块缓存中是很简单的，可以使用memcpy()实现。在Python中，使用struct就需要这样：
              str = struct.pack('B4sII', 0x04, 'aaaa', 0x01, 0x0e)
      'B4sII'  ------   有一个unsigned short、char[4], 2个unsigned int。其中s之前的数字说明了字符串的大小 。
              type, tag, version, length = struct.unpack('B4sll', str)
 
 
 
       未完待续......
 
       2013年第一篇，一切贵在坚持。
'''