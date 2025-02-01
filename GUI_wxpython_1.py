# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 4.2.1-0-g80c4cb6)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import os
import subprocess
import wx
import wx.xrc
import wx.dataview
import wx.lib.scrolledpanel as scrolled

###########################################################################
## Class MyFormMain
###########################################################################

class MyFormMain ( wx.Frame ):

    def __init__( self, parent ):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"8comic Comic Downloader", pos = wx.DefaultPosition, size = wx.Size( 630,560 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

        self.SetSizeHints( wx.Size( 630,560 ), wx.DefaultSize )

        self.m_menubar3 = wx.MenuBar( 0 )
        self.m_menu2 = wx.Menu()
        self.Open = wx.MenuItem( self.m_menu2, wx.ID_ANY, u"Open", wx.EmptyString, wx.ITEM_NORMAL )
        self.m_menu2.Append( self.Open )

        self.Save = wx.MenuItem( self.m_menu2, wx.ID_ANY, u"Save", wx.EmptyString, wx.ITEM_NORMAL )
        self.m_menu2.Append( self.Save )

        self.m_menu2.AppendSeparator()

        self.Exit = wx.MenuItem( self.m_menu2, wx.ID_ANY, u"Exit", wx.EmptyString, wx.ITEM_NORMAL )
        self.m_menu2.Append( self.Exit )

        self.m_menubar3.Append( self.m_menu2, u"File" )

        self.Settings = wx.Menu()
        self.Set_Font_size = wx.MenuItem( self.Settings, wx.ID_ANY, u"Set Font size", wx.EmptyString, wx.ITEM_NORMAL )
        self.Settings.Append( self.Set_Font_size )

        self.Set_Background_Color = wx.MenuItem( self.Settings, wx.ID_ANY, u"Set Background Color", wx.EmptyString, wx.ITEM_NORMAL )
        self.Settings.Append( self.Set_Background_Color )

        self.Open_Theme_Creator = wx.MenuItem( self.Settings, wx.ID_ANY, u"Open Theme Creator", wx.EmptyString, wx.ITEM_NORMAL )
        self.Settings.Append( self.Open_Theme_Creator )

        self.Change_Theme = wx.MenuItem( self.Settings, wx.ID_ANY, u"Change Theme", wx.EmptyString, wx.ITEM_NORMAL )
        self.Settings.Append( self.Change_Theme )

        self.m_menubar3.Append( self.Settings, u"Settings" )

        self.Help = wx.Menu()
        self.m_menubar3.Append( self.Help, u"Help" )

        self.SetMenuBar( self.m_menubar3 )

        bSizer1 = wx.BoxSizer( wx.VERTICAL )

        fgSizer1 = wx.FlexGridSizer( 2, 4, 0, 0 )
        fgSizer1.AddGrowableCol( 1 )
        fgSizer1.SetFlexibleDirection( wx.HORIZONTAL )
        fgSizer1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

        self.COMIC_URL = wx.StaticText( self, wx.ID_ANY, u"COMIC URL", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.COMIC_URL.Wrap( -1 )

        fgSizer1.Add( self.COMIC_URL, 0, wx.ALL, 5 )

        self.URL = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.URL.SetMinSize( wx.Size( 300,-1 ) )

        fgSizer1.Add( self.URL, 1, wx.ALL|wx.EXPAND, 5 )

        self.Analyze = wx.Button( self, wx.ID_ANY, u"Analyze", wx.DefaultPosition, wx.DefaultSize, 0 )
        fgSizer1.Add( self.Analyze, 0, wx.ALL|wx.ALIGN_RIGHT, 5 )


        fgSizer1.Add( ( 0, 0), 1, wx.EXPAND, 5 )

        self.Save_Path = wx.StaticText( self, wx.ID_ANY, u"Save Path:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.Save_Path.Wrap( -1 )

        fgSizer1.Add( self.Save_Path, 1, wx.ALL, 5 )

        self.path_display = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.path_display.SetMinSize( wx.Size( 300,-1 ) )

        fgSizer1.Add( self.path_display, 1, wx.ALL|wx.EXPAND, 5 )

        self.Browse = wx.Button( self, wx.ID_ANY, u"Browse", wx.DefaultPosition, wx.DefaultSize, 0 )
        fgSizer1.Add( self.Browse, 0, wx.ALL, 5 )

        self.Open_Folder = wx.Button( self, wx.ID_ANY, u"Open Folder", wx.DefaultPosition, wx.DefaultSize, 0 )
        fgSizer1.Add( self.Open_Folder, 0, wx.ALL, 5 )


        bSizer1.Add( fgSizer1, 0, wx.EXPAND, 5 )

        Log_Output = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"Log Output" ), wx.VERTICAL )

        self.m_textCtrl3 = wx.TextCtrl( Log_Output.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_MULTILINE|wx.TE_RICH2|wx.VSCROLL )
        self.m_textCtrl3.SetMinSize( wx.Size( -1,150 ) )

        Log_Output.Add( self.m_textCtrl3, 0, wx.ALL|wx.EXPAND, 5 )

        self.Clear = wx.Button( Log_Output.GetStaticBox(), wx.ID_ANY, u"Clear", wx.DefaultPosition, wx.DefaultSize, 0 )
        Log_Output.Add( self.Clear, 0, wx.ALL, 5 )

        bSizer3 = wx.BoxSizer( wx.HORIZONTAL )

        self.Total_Process = wx.StaticText( Log_Output.GetStaticBox(), wx.ID_ANY, u"Total_Process", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.Total_Process.Wrap( -1 )

        self.Total_Process.SetMinSize( wx.Size( 90,-1 ) )

        bSizer3.Add( self.Total_Process, 0, wx.ALL, 5 )

        self.Total_Process = wx.Gauge( Log_Output.GetStaticBox(), wx.ID_ANY, 100, wx.DefaultPosition, wx.DefaultSize, wx.GA_HORIZONTAL )
        self.Total_Process.SetValue( 0 )
        bSizer3.Add( self.Total_Process, 0, wx.ALL, 5 )


        Log_Output.Add( bSizer3, 0, wx.EXPAND, 5 )

        bSizer31 = wx.BoxSizer( wx.HORIZONTAL )

        self.Image_Process = wx.StaticText( Log_Output.GetStaticBox(), wx.ID_ANY, u"Image_Process", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.Image_Process.Wrap( -1 )

        self.Image_Process.SetMinSize( wx.Size( 90,-1 ) )

        bSizer31.Add( self.Image_Process, 0, wx.ALL, 5 )

        self.Image_Process1 = wx.Gauge( Log_Output.GetStaticBox(), wx.ID_ANY, 100, wx.DefaultPosition, wx.DefaultSize, wx.GA_HORIZONTAL )
        self.Image_Process1.SetValue( 0 )
        bSizer31.Add( self.Image_Process1, 0, wx.ALL, 5 )


        Log_Output.Add( bSizer31, 1, wx.EXPAND, 5 )
        bSizer1.Add( Log_Output, 0, wx.EXPAND, 5 )

        Download_Queue = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"Download Queue" ), wx.VERTICAL )

        self.queue_table  = wx.dataview.DataViewListCtrl( Download_Queue.GetStaticBox(), wx.ID_ANY, style=wx.LC_REPORT | wx.SUNKEN_BORDER)
        self.queue_table.SetMinSize( wx.Size( 600,150 ) )

        Download_Queue.Add( self.queue_table , 0, wx.ALL, 5 )
        # Setup headers
        columns = [("Comic Name", 100), ("Chapter", 100), ("Save Path", 200), ("Status", 100), ("Progress", 100)]
        for idx, (col_name, col_width) in enumerate(columns):
            self.queue_table.AppendTextColumn(col_name, width=col_width)        
        

        bSizer5 = wx.BoxSizer( wx.HORIZONTAL )

        self.Add_to_queue = wx.Button( Download_Queue.GetStaticBox(), wx.ID_ANY, u"Add to queue", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer5.Add( self.Add_to_queue, 0, wx.ALL, 5 )

        self.Start_download = wx.Button( Download_Queue.GetStaticBox(), wx.ID_ANY, u"Start download", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer5.Add( self.Start_download, 0, wx.ALL, 5 )


        Download_Queue.Add( bSizer5, 1, wx.EXPAND, 5 )


        bSizer1.Add( Download_Queue, 0, wx.EXPAND, 5 )



        self.SetSizer( bSizer1 )
        self.Layout()

        self.Centre( wx.BOTH )

        # Connect Events
        self.Bind( wx.EVT_MENU, self.OnOpenFile, id = self.Open.GetId() )
        self.Bind( wx.EVT_MENU, self.OnSaveFile, id = self.Save.GetId() )
        self.Bind( wx.EVT_MENU, self.OnExit, id = self.Exit.GetId() )
        self.Bind( wx.EVT_MENU, self.OnAdjustFontSize, id = self.Set_Font_size.GetId() )
        self.Browse.Bind( wx.EVT_BUTTON, self.browse_save_path )
        self.Open_Folder.Bind( wx.EVT_BUTTON, self.open_download_folder )
        self.Clear.Bind( wx.EVT_BUTTON, self.clear_log )    
        self.queue_table.Bind(wx.EVT_CONTEXT_MENU, self.show_context_menu)# 右键菜单绑定
        self.Analyze.Bind( wx.EVT_BUTTON, self.start_analyze )
        self.Add_to_queue.Bind( wx.EVT_BUTTON, self.add_to_queue )
        self.Start_download.Bind( wx.EVT_BUTTON, self.Start_1 )

        self.chapters = [("1", "Chapter 1"), ("2", "Chapter 2"), ("3", "Chapter 3")]
        # self adjustment
        self.Fit()

    def __del__( self ):
        pass


    # Virtual event handlers, override them in your derived class
    def OnOpenFile(self, event):
        with wx.FileDialog(self, "Open file", wildcard="All files (*.*)|*.*",
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return  # 用戶取消了操作

            pathname = fileDialog.GetPath()
            try:
                with open(pathname, 'r') as file:
                    self.textCtrl.SetValue(file.read())  # 假設有一個名為 textCtrl 的文本控制項
            except IOError:
                wx.LogError(f"Cannot open file '{pathname}'.")
                self.log_message(f"Cannot open file '{pathname}'.")

    def OnSaveFile( self, event ):
        with wx.FileDialog(self, "Save file", wildcard="All files (*.*)|*.*",
                           style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return  # 用戶取消了操作

            pathname = fileDialog.GetPath()
            try:
                with open(pathname, 'w') as file:
                    file.write(self.textCtrl.GetValue())  # 假設有一個名為 textCtrl 的文本控制項
            except IOError:
                wx.LogError(f"Cannot save current data in file '{pathname}'.")
                self.log_message(f"Cannot save current data in file '{pathname}'.")
                
    def OnExit( self, event ):
        self.Close(True)

    def OnAdjustFontSize(self, event):
        # 显示字体选择对话框
        fontData = wx.FontData()
        fontData.EnableEffects(False)  # 禁用颜色等效果，仅调整字体大小
        dialog = wx.FontDialog(self, fontData)
        if dialog.ShowModal() == wx.ID_OK:
            newFont = dialog.GetFontData().GetChosenFont()
            self.SetGlobalFont(newFont)
        dialog.Destroy()

    def start_analyze( self, event ):
        self.log_message("Press analyze button conformed\n ")
        self.show_chapter_popup()

    def SetGlobalFont(self, font):
        # 遍历所有顶级窗口并设置字体
        for window in wx.GetTopLevelWindows():
            self.ApplyFontRecursively(window, font)

    def ApplyFontRecursively(self, window, font):
        window.SetFont(font)
        for child in window.GetChildren():
            self.ApplyFontRecursively(child, font)
        window.Layout()# 重新布局以适应新的字体大小
        self.Fit() #自適應視窗大小調整
        
    def browse_save_path(self, event):
        with wx.DirDialog(self, "选择保存路径", style=wx.DD_DEFAULT_STYLE) as dirDialog:
            if dirDialog.ShowModal() == wx.ID_OK:
                self.save_path = os.path.normpath(dirDialog.GetPath())  # 标准化路径
                self.set_save_path(self.save_path)  # 在文本框中显示选择的路径
                self.log_message("Set Path Successful\n")
            else:
                self.log_message("未选择路径")

    def set_save_path(self, path):
        self.path_display.SetValue(path)

    def log_message(self, message):
        """追加日志消息并自动滚动到底部"""
        self.m_textCtrl3.AppendText(message)  # 追加日志消息
        self.m_textCtrl3.ShowPosition(self.m_textCtrl3.GetLastPosition())  # 滚动到底部

    def open_download_folder(self, path):
        if self.save_path and os.path.exists(self.save_path):
            # Open the specified folder if it exists
            subprocess.Popen(f'explorer "{self.save_path}"' if os.name == 'nt' else ['open', self.save_path])
        else:
            # Open the default directory (e.g., home folder)
            default_path = os.path.dirname(os.path.abspath(__file__))# 將os.path.expanduser("~")改成當前py檔的路徑
            subprocess.Popen(f'explorer "{default_path}"' if os.name == 'nt' else ['open', default_path])

    def clear_log(self, event):
        self.m_textCtrl3.Clear()

    def show_context_menu(self, event):
        menu = wx.Menu()
        menu.Append(wx.ID_ANY, "Option 1")
        menu.Append(wx.ID_ANY, "Option 2")
        self.PopupMenu(menu)
        menu.Destroy()

    def add_to_queue( self, event ):
        self.log_message("Press add_to_queue button conformed\n")

    def Start_1( self, event ):
        self.log_message("Press Start_1 button conformed\n ")

    def show_chapter_popup(self):
#         chapters = [("1", "Chapter 1"), ("2", "Chapter 2"), ("3", "Chapter 3")]  # 示例章节列表

        # 创建弹出窗口
        self.chapter_window = wx.Frame(self, title="Select Chapters", size=(600, 350))
        panel = wx.Panel(self.chapter_window)
        panel_sizer = wx.BoxSizer(wx.VERTICAL)
        panel.SetSizer(panel_sizer)

        scrolled_panel = scrolled.ScrolledPanel(panel, -1, style=wx.TAB_TRAVERSAL | wx.SUNKEN_BORDER)
        scrolled_panel.SetupScrolling()
        scrolled_sizer = wx.BoxSizer(wx.VERTICAL)
        scrolled_panel.SetSizer(scrolled_sizer)

        # 添加复选框到滚动面板
        self.chapter_checks = []
        for chapter_id, chapter_text in self.chapters:
            chk = wx.CheckBox(scrolled_panel, label=chapter_text)
            scrolled_sizer.Add(chk, 0, wx.ALL, 5)
            self.chapter_checks.append((chk, chapter_text))

        # 确认按钮
        confirm_button = wx.Button(panel, label="Confirm Selection")
        confirm_button.Bind(wx.EVT_BUTTON, self.on_confirm_selection)

        # 将滚动面板和确认按钮添加到面板的 sizer
        panel_sizer.Add(scrolled_panel, 1, wx.EXPAND | wx.ALL, 5)
        panel_sizer.Add(confirm_button, 0, wx.ALL | wx.CENTER, 5)

        self.chapter_window.Show()

    def on_confirm_selection(self, event):
        selected_chapters = [text for chk, text in self.chapter_checks if chk.GetValue()]
        self.log_message(f"Selected Chapters:{selected_chapters}")
        self.chapter_window.Destroy()

if __name__ == '__main__':
    app = wx.App(False)
    frame = MyFormMain(None)
    frame.Fit()
    frame.Show()
    app.MainLoop()



