#!/usr/bin/env python
import wx
import icon
import base64
import cStringIO




def kill_it_with_fire():
    app.Exit()

def create_menu_item(menu, label, func):
    item = wx.MenuItem(menu, -1, label)
    menu.Bind(wx.EVT_MENU, func, id=item.GetId())
    menu.AppendItem(item)
    return item


class TaskBarIcon(wx.TaskBarIcon):
    TRAY_ICON = base64.b64decode(icon.icon)
    Money = 0

    def __init__(self):
        super(TaskBarIcon, self).__init__()
        self.set_icon(self.TRAY_ICON)

    def set_icon(self, icon_bytes):
        icon_stream = cStringIO.StringIO(icon_bytes)
        icon_image = wx.ImageFromStream(icon_stream)
        icon_bitmap = wx.BitmapFromImage(icon_image)
        icon_pic = wx.IconFromBitmap(icon_bitmap)

        tt = "Won $" + str(self.Money) + " so far!"
        self.SetIcon(icon_pic, tt)

    def update(self, money):
        self.Money = money
        self.set_icon(self.TRAY_ICON)

    def exit(self, anything=None):
        wx.CallAfter(kill_it_with_fire)


class TaskBarFrame(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, -1, title, size=(0, 0),
                          style=wx.FRAME_NO_TASKBAR | wx.NO_FULL_REPAINT_ON_RESIZE)

        self.tbicon = TaskBarIcon()
        self.tbmenu = self.create_popup_menu()
        self.Show(False)

    def create_popup_menu(self):
        menu = wx.Menu()
        menu.AppendSeparator()
        create_menu_item(menu, 'Exit', kill_it_with_fire)
        return menu

    def click_menu(self, event):
        self.tbicon.PopupMenu(self.tbmenu)
        print("Hello, click again!")
        pass


class WidgetRunner(wx.App):
    frame = None

    def OnInit(self):
        self.frame = TaskBarFrame(None, -1, ' ')
        self.frame.Center(wx.BOTH)
        self.frame.Show(False)
        return True


app = WidgetRunner(0)


def main():
    app.MainLoop()


def update(money):
    app.frame.tbicon.update(money)


def register_on_click(function):
    icon = app.frame.tbicon
    icon.Bind(wx.EVT_TASKBAR_LEFT_DOWN, function)
