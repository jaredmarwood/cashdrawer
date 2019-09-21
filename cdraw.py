import os

import wx
from wx import Icon
from wx.adv import TaskBarIcon
from wx.lib.embeddedimage import PyEmbeddedImage


class CashDrawer:
  def OpenCashDrawer(self, printername='EPSON_TM_T88V'):
    """
    https://www.cups.org/doc/man-lpr.html
    """
    os.system('echo "\033p011" | lpr -P %s -l -h'%printername)

#material-ui print icon, white color
appicon = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYBAMAAAASWSDLAAAAKlBMVEUAAAD///////////////////////////////////////////////////+Gu8ovAAAADXRSTlMABQY8PkBChoeI4OTlUznvfAAAAAFiS0dEDfa0YfUAAAA/SURBVBjTY2AgGtwFA9I4SEBzLUTmViOQM/cuFFwHcs5C2WG34drv3jW5i8S5i43DAKdwc4A0nMDgEONqXAAAC/BjFK8CffcAAAAASUVORK5CYII=")

class CashDrawerBarIcon(TaskBarIcon):
  TBMENU_OPEN_CASHDRAWER = 101
  TBMENU_CLOSE   = 102
  HOTKEY_ID = 103
  
  def __init__(self, frame):
    TaskBarIcon.__init__(self)
    self.frame = frame
    # Set the image
    icon = self.MakeIcon(appicon.GetImage())
    self.SetIcon(icon, "Open Cash Drawer")
    
    # bind events
    self.Bind(wx.adv.EVT_TASKBAR_LEFT_DCLICK, self.OnTaskBarActivate)
    self.Bind(wx.EVT_MENU, self.OnTaskBarActivate, id=self.TBMENU_OPEN_CASHDRAWER)
    self.Bind(wx.EVT_MENU, self.OnTaskBarClose, id=self.TBMENU_CLOSE)

  def CreatePopupMenu(self):
      """
      Create Task Bar Menu
      """
      menu = wx.Menu()
      menu.Append(self.TBMENU_OPEN_CASHDRAWER, "Open Drawer")
      menu.AppendSeparator()
      menu.Append(self.TBMENU_CLOSE,   "Close")
      return menu

  def MakeIcon(self, img):
      """
      The various platforms have different requirements for the
      icon size...
      """
      if "wxMSW" in wx.PlatformInfo:
          img = img.Scale(16, 16)
      elif "wxGTK" in wx.PlatformInfo:
          img = img.Scale(22, 22)
      # wxMac can be any size upto 128x128, so leave the source img alone....
      icon = Icon(img.ConvertToBitmap() )
      return icon
  
  def OpenDrawer(self):
    cashDrawer = CashDrawer()
    cashDrawer.OpenCashDrawer()

  def OnTaskBarActivate(self, evt):
    self.OpenDrawer()
    evt.Skip()

  def OnTaskBarClose(self, evt):
      wx.CallAfter(self.frame.Close)

class MainFrame(wx.Frame):
  HOTKEY_ID = 103
  def __init__(self, parent):
    wx.Frame.__init__(self, parent, title="Epson TM-T88V Open Draw")
    #wx.Frame(None,-1,'')
    #create hotkey global
    self.CreateHotKey()
    self.tbicon = CashDrawerBarIcon(self)
    self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)
    self.Bind(wx.EVT_HOTKEY, self.HandleHotKey, id=self.HOTKEY_ID)

  def CreateHotKey(self):
    result = self.RegisterHotKey(self.HOTKEY_ID, wx.MOD_CONTROL|wx.MOD_SHIFT, ord('o'))
  
  def HandleHotKey(self, evt):
    self.tbicon.OpenDrawer()
    evt.Skip()

  def OnCloseWindow(self, evt):
      self.tbicon.Destroy()
      evt.Skip()
        

app = wx.App(redirect=False)
frame = MainFrame(None)
app.MainLoop()
