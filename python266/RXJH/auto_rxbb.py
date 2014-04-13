#encoding=utf-8
'''
Created on 2014-3-23

@author: khz
'''
#from pywinauto import application
import pywinauto
from pywinauto import findwindows
from pywinauto.controls import HwndWrapper
from pywinauto import win32functions
import win32con
import win32gui
import time
import os

def EnableWindow(handle):
    win32functions.EnableWindow(handle, True)
    pass

class CRxbbWindow:
    def __init__(self, strCharacter):
        self.app = pywinauto.application.Application()
        
        self.app.connect_(class_name="#32770", title = strCharacter)
        self.rxjh_dlg = self.app.Window_(class_name="#32770", title = strCharacter)
        rxjh_tab = self.rxjh_dlg["SysTabControl32"]#.WrapperObject()#TabControl      #["SysTabControl32"]
        #print type(rxjh_tab.handle)
        #print "%08x" % rxjh_dlg.handle
        #print "%08x" % rxjh_tab.handle
        #print rxjh_tab.Children()
        #(rxjh_dlg.print_control_identifiers())
        for i in range(rxjh_tab.TabCount()):
            print rxjh_tab.GetTabText(i)
        self.lstDlgHandle = findwindows.find_windows(class_name="#32770", parent=rxjh_tab.handle, \
                                       top_level_only = False, visible_only = False)
        print "len: ", len(self.lstDlgHandle)
        for handle in self.lstDlgHandle:
            print "%08x" % handle
            aHwndWrapper = HwndWrapper.HwndWrapper(handle)
            lstWrapper = aHwndWrapper.Children()
            strInfo = ""
            for aWrapper in lstWrapper:
                strInfo = strInfo + '\t' + (aWrapper.WindowText())
            print strInfo
        return
        pass
    
    def InitDao(self):
        strZiDongDaGuai = u"自动打怪"
        strKuaiSuGongJi = u"快速攻击"
        self.app.Window_(handle = self.lstDlgHandle[1])[strZiDongDaGuai].Click()
        unknownType = self.app.Window_(handle = self.lstDlgHandle[1])[strKuaiSuGongJi]#.Click()
        EnableWindow(unknownType.handle)
        print(type(unknownType.handle))
        unknownType.Click()
        pass
    
    def auto_guaji(self):
        hWnd = win32functions.GetWindow(self.rxjh_dlg.handle, win32con.GW_CHILD)
        '''
        while(hWnd):
            print hex(hWnd)
            print ( win32gui.GetWindowText(hWnd).decode("gb2312") )
            #print unicode( win32gui.GetWindowText(hWnd).decode()) .encode("gbk")
            hWnd = win32functions.GetWindow(hWnd, win32con.GW_HWNDNEXT)
            #win32functions.GetWindowText()
        '''
        hWnd = win32functions.GetWindow(hWnd, win32con.GW_HWNDNEXT)
        hWnd = win32functions.GetWindow(hWnd, win32con.GW_HWNDNEXT)
        while(1):
            strBtnInfo = win32gui.GetWindowText(hWnd).decode("gb2312")
            print ( strBtnInfo )
            HwndWrapper.HwndWrapper(hWnd).Click()
            time.sleep(1)
            if( strBtnInfo == "开始挂机" ):
                HwndWrapper.HwndWrapper(hWnd).Click()
            print ( strBtnInfo )
            time.sleep(60*2)
def main():
    strCharacter = u"九分刀不笑"
    rxbb = CRxbbWindow(strCharacter)
    
    #rxbb.InitDao()
    rxbb.auto_guaji()
    pass

if __name__ == "__main__":
    print("------------------   begin   ------------------")
    
    print( u"【当前工作目录是：】\t".encode("gb2312") + os.getcwd() )
    print( u"【当前进程ID是：】\t".encode("gb2312") + str(os.getpid()) )
    main()
    
    print("------------------    end    ------------------")
