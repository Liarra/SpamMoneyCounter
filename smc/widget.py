#!/usr/bin/env python
import wx
import icon
import base64
import cStringIO


class TaskBarIcon(wx.TaskBarIcon):
    TRAY_ICON = base64.b64decode(icon.icon)
    Money = 0

    def __init__(self, frame):
        self.frame = frame
        super(TaskBarIcon, self).__init__()
        self.set_icon()

    def set_icon(self):
        icon_bytes = self.TRAY_ICON
        icon_stream = cStringIO.StringIO(icon_bytes)
        icon_image = wx.ImageFromStream(icon_stream)
        icon_bitmap = wx.BitmapFromImage(icon_image)
        icon_pic = wx.IconFromBitmap(icon_bitmap)

        tt = "Got $" + str(self.Money) + " so far!"
        self.SetIcon(icon_pic, tt)

    def CreatePopupMenu(self):
        menu = wx.Menu()
        self.create_menu_item(menu, 'Exit', self.exit)
        return menu

    def create_menu_item(self, menu, label, func):
        item = wx.MenuItem(menu, -1, label)
        menu.Bind(wx.EVT_MENU, func, id=item.GetId())
        menu.AppendItem(item)
        return item

    def update(self, money):
        self.Money = money
        self.set_icon()

    def exit(self, anything=None):
        wx.CallAfter(self.Destroy)
        self.frame.Close()


class App(wx.App):
    def __init__(self):
        self.frame = None
        self.icon = None
        super(App, self).__init__()

    def OnInit(self):
        self.frame = wx.Frame(None)
        self.icon = TaskBarIcon(self.frame)
        self.SetTopWindow(self.frame)
        return True


class SMCWidget:
    def __init__(self):
        self.app = App()

    def run(self):
        self.app.MainLoop()

    def update(self, money):
        self.app.icon.update(money)

