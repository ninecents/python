#encoding=utf-8
'''
Created on 2014年4月16日

@author: zhaoanhua
'''
import os
import pywinauto
import win32ui

def main():
    app = pywinauto.application.Application()
    
    app.connect_(title = "Select Target")
    #mainWnd = app.Window_(title_re=".*Properties")
    mainWnd = app.Window_(title_re="Select Target")
    print app.process
    print hex(mainWnd.handle)
    print mainWnd.PrintControlIdentifiers()
    aList = mainWnd.List1.WrapperObject()
    print aList.Texts()
    return
    aTabControl = mainWnd.SysTabControl32.WrapperObject()
    print aTabControl.TabCount()
    print aTabControl.RowCount()
    nSel = aTabControl.GetSelectedTab()
    aTabControl.Select(8)
    print aTabControl.GetTabText(nSel)
    print hex(aTabControl.handle)
    
    # 选择列表
    aList = mainWnd.SysListView32.WrapperObject()
    print hex(aList.handle)
    print aList.ColumnCount()
    print aList.ItemCount()
    print aList.Texts()
    print aList.GetItem(0)
    
    #print mainWnd.Tab1.PrintControlIdentifiers()
    pass

if __name__ == "__main__":
    print("------------------   begin   ------------------")
   
    print( u"【当前工作目录是：】\t" + os.getcwd() )
    print( u"【当前进程ID是：】\t" + str(os.getpid()) )
    print( "\n" )
    main()
   
    print("------------------    end    ------------------")

